from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.sale import SaleCreate, SaleRead
from app.services.sale_service import SaleService
from app.infrastructure.database.repositories.sale_repository import SaleRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency

router = APIRouter()


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Sale created successfully"},
    },
)
async def create_sale(
    sale_data: SaleCreate, user_id: int, db: AsyncSession = Depends(db_dependency)
):
    sale_repository = SaleRepository(db)
    sale_service = SaleService(sale_repository)
    try:
        result = await sale_service.create_sale_with_blockchain(sale_data, user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create sale: {e}")
