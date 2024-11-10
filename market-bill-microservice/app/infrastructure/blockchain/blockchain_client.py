import httpx
from typing import Dict, Any
from app.domain.schemas.sale import SaleCreate, SaleRead
import logging


class BlockchainClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            base_url=self.base_url, timeout=20.0
        )  # Configura un timeout apropiado

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.aclose()

    async def create_trade(self, trade_data: SaleRead) -> Dict[str, Any]:
        """
        Crea una oferta de trade en el blockchain.
        user_id: ID del usuario que hace la oferta
        trade_data: Datos de la oferta, incluyen `buyer`, `energyAmount`, `pricePerEnergyUnit`, `contractTermsHash`
        """
        user_id = trade_data.offer.seller_id
        url = f"{self.base_url}/trades"
        print(user_id, trade_data.offer.buyer_id)
        payload = {
            "userId": str(user_id),
            "sellerId": str(trade_data.offer.buyer_id),
            "energyAmount": trade_data.offer.energy_amount,
            "pricePerEnergyUnit": trade_data.offer.price_per_unit,
            "contractTermsHash": str(trade_data.pdf_document_path),
        }

        # Log de datos de la operación
        logging.info(
            f"Creando transaccion en el blockchain para el usuario {user_id} en la URL: {url}"
        )

        try:
            response = await self.client.post(url, json=payload)
            response.raise_for_status()
            logging.info(f"Oferta creada exitosamente para el usuario {user_id}")
            return response.json()

        except httpx.HTTPStatusError as e:
            logging.error(
                f"Error HTTP al crear trade para el usuario {user_id}: {e.response.status_code} - {e.response.text}"
            )
            raise Exception(
                f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
            )

        except httpx.RequestError as e:
            logging.error(
                f"Error de conexión al crear trade para el usuario {user_id}: {e}"
            )
            raise Exception(f"An error occurred while requesting: {e}")

        except Exception as e:
            logging.exception(
                f"Error inesperado al crear trade en blockchain para el usuario {user_id}"
            )
            raise Exception(f"Failed to create trade on blockchain: {e}")
