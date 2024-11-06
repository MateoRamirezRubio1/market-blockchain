from sqlalchemy.orm import Session
from app.infrastructure.database.repositories.sale_repository import SaleRepository
from app.domain.schemas.sale import SaleCreate, SaleStatus
from fastapi import HTTPException, status
from app.infrastructure.blockchain.blockchain_client import BlockchainClient


class SaleService:

    def __init__(self, sale_repository: SaleRepository):
        self.sale_repository = sale_repository

    async def create_sale_with_blockchain(self, sale_data: SaleCreate, user_id: int):
        try:
            # Validación: Verificar si ya existe una venta para la misma oferta
            existing_sale = await self.sale_repository.get_sale_by_offer_id(
                sale_data.offer_id
            )
            if existing_sale:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe una venta para esta oferta.",
                )

            # Crear la venta
            sale = await self.sale_repository.create_sale(sale_data)
            offer = sale.offer

            trade_data = {
                "buyer": "0x1234567890abcdef1234567890abcdef12345678",
                "energyAmount": offer.energy_amount,
                "pricePerEnergyUnit": offer.price_per_unit,
                "contractTermsHash": sale.pdf_document_path,
            }

            blockchain_client = BlockchainClient(base_url="http://backend:3000/api/v1")
            # Crear trade en blockchain
            blockchain_response = await blockchain_client.create_trade(
                user_id, trade_data
            )

            # Retornar información de la venta y la respuesta del blockchain
            return {"sale": sale, "blockchain_response": blockchain_response}

        except Exception as e:
            # Manejar errores al crear el trade
            return {"error": str(e)}
