from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.sale import SaleCreate, SaleRead
from app.services.sale_service import SaleService
from app.infrastructure.database.repositories.sale_repository import SaleRepository
from app.infrastructure.database.repositories.offer_repository import OfferRepository
from app.services.offer_service import OfferService
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency
from app.infrastructure.blockchain.blockchain_client import BlockchainClient
import logging
import httpx
import os
from fastapi.responses import FileResponse

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={201: {"description": "Sale created successfully"}},
)
async def create_sale(sale_data: SaleCreate, db: AsyncSession = Depends(db_dependency)):
    offer_service = OfferService(OfferRepository(db))
    sale_service = SaleService(SaleRepository(db), offer_service, db)

    try:
        # Llama al servicio para crear la venta con integración en el blockchain
        sale_result = await sale_service.create_sale_with_blockchain(sale_data)
        return sale_result
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
        raise HTTPException(
            status_code=e.response.status_code, detail="Blockchain service error"
        )
    except httpx.RequestError as e:
        logging.error(f"Connection error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Blockchain service unavailable",
        )
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create sale {e}")


@router.get("/contracts/{filename}")
async def download_pdf(filename: str):
    # Ruta a la carpeta pdf en la raíz del proyecto
    pdf_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../../../../pdfs", filename)
    )

    # Verificar si el archivo existe
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")

    # Servir el archivo PDF como respuesta
    return FileResponse(path=pdf_path, filename=filename, media_type="application/pdf")
