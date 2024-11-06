import httpx
from typing import Dict, Any
from app.domain.schemas.sale import TradeData


class BlockchainClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def create_trade(self, user_id: int, trade_data: TradeData) -> Dict[str, Any]:
        url = f"{self.base_url}/offers"

        payload = {
            "userId": "11",
            "buyer": "0x1234567890abcdef1234567890abcdef12345678",
            "energyAmount": 1000,
            "pricePerEnergyUnit": 50,
            "contractTermsHash": "0x5d41402abc4b2a76b9719d911017c59200000000000000000000000000000000",
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return response.json()  # Retornar la respuesta JSON
            except httpx.HTTPStatusError as e:
                # Manejar errores HTTP específicos
                raise Exception(
                    f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
                )
            except httpx.RequestError as e:
                # Manejar errores de conexión
                raise Exception(f"An error occurred while requesting: {e}")
            except Exception as e:
                # Otros errores
                raise Exception(f"Failed to create trade on blockchain: {e}")
