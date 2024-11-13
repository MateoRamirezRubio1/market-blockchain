from sqlalchemy.orm import Session
from app.infrastructure.database.repositories.sale_repository import (
    SaleRepository,
    SaleNotFoundError,
)
from app.domain.schemas.sale import SaleCreate, SaleStatus, SaleRead
from app.domain.schemas.offer import OfferResponse
from fastapi import HTTPException, status
from app.infrastructure.blockchain.blockchain_client import BlockchainClient
from app.services.offer_service import OfferService
from app.domain.schemas.offer import OfferStatus
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import httpx
import asyncio
from app.infrastructure.pdf.contract_generator import create_contract_pdf
from concurrent.futures import ThreadPoolExecutor
import hashlib


class SaleService:

    def __init__(
        self,
        sale_repository: SaleRepository,
        session: AsyncSession,
        offer_service: OfferService | None = None,
    ):
        self.sale_repository = sale_repository
        self.offer_service = offer_service
        self.session = session  # Inyectar la sesión para manejar la transacción

    async def create_sale_with_blockchain(self, sale_data: SaleCreate) -> dict:
        # Validación: Verificar si ya existe una venta para la misma oferta
        existing_sale = await self.sale_repository.get_sale_by_offer_id(
            sale_data.offer_id
        )
        if existing_sale:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una venta para esta oferta.",
            )

            # Crear la venta en la base de datos
        sale = await self.sale_repository.create_sale(sale_data)

        unique_pdf_document_path = await self.generate_unique_name(
            sale.id, sale.offer.seller_id, sale.offer.buyer_id
        )

        sale.pdf_document_path = str(unique_pdf_document_path)
        sale = await self.sale_repository.save_with_flush(sale)

        # Actualizar el estado de la oferta a "accepted"
        offer_status_updated = await self.offer_service.update_offer_status(
            sale_data.offer_id, OfferStatus.accepted, True
        )

        offer_buyer_updated = await self.offer_service.update_buyer_offer(
            sale_data.offer_id, sale_data.buyer_id
        )

        # Llamada al servicio de blockchain
        async with BlockchainClient(base_url="http://backend:3000/api/v1") as client:
            try:
                sale_data_dict = sale.__dict__.copy()
                sale_data_dict["offer"] = OfferResponse.from_orm(sale.offer)
                sale_read_data = SaleRead(**sale_data_dict)

                blockchain_result = await client.create_trade(sale_read_data)

                contract_data = {
                    "confirmation_date": sale_read_data.offer.transfer_datetime,
                    "seller_name": sale_read_data.offer.seller_id,
                    "buyer_name": sale_read_data.offer.buyer_id,
                    "offer_hash": blockchain_result["receipt"]["hash"],
                    "energy_amount": sale_read_data.offer.energy_amount,
                    "price_per_unit": sale_read_data.offer.price_per_unit,
                    "offer_type": sale_read_data.offer.offer_type,
                    "status": sale_read_data.status,
                    "transfer_datetime": sale_read_data.offer.transfer_datetime,
                    "penalty_reason": sale_read_data.penalty_reason,
                    "terms_conditions": sale_read_data.offer.terms_conditions,
                }

                loop = asyncio.get_event_loop()
                with ThreadPoolExecutor() as pool:
                    await loop.run_in_executor(
                        pool,
                        create_contract_pdf,
                        f"{sale_read_data.pdf_document_path}.pdf",
                        contract_data,
                    )

                return sale_read_data
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                # Revertir la venta y el estado de la oferta si hay error en el blockchain
                await self.sale_repository.delete_sale(sale.id)
                raise e

    async def generate_unique_name(self, sale_id: int, buyer_id: str, seller_id: str):
        # Concatenar los valores de los identificadores para que sean únicos
        unique_string = f"{sale_id}-{buyer_id}-{seller_id}"

        # Crear un hash SHA-256 de la cadena única
        sha256_hash = hashlib.sha256(unique_string.encode()).hexdigest()
        restante = 1 if (64 - len(sha256_hash)) == 0 else (64 - len(sha256_hash))

        # Tomar los primeros 32 caracteres del hash y agregar ceros al final para ajustarlo a 64 caracteres
        unique_id = "0x" + sha256_hash[:32] + "0" * 32

        return f"{unique_id}"

    async def get_all_sales(self):
        try:
            sales = await self.sale_repository.get_all_sales()
            return sales
        except SaleNotFoundError as e:
            raise SaleNotFoundError(str(e)) from e

    async def get_sale_by_id(self, sale_id: int):
        try:
            sale = await self.sale_repository.get_sale_by_id(sale_id)
            return sale
        except SaleNotFoundError as e:
            raise SaleNotFoundError(str(e)) from e
