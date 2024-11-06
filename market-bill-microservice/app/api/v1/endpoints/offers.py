from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.offer import OfferCreate, OfferResponse
from app.services.offer_service import OfferService
from app.infrastructure.database.repositories.offer_repository import OfferRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency

router = APIRouter()


@router.post(
    "/",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Offer created successfully"},
    },
)
async def create_offer(
    offer_create: OfferCreate, db: AsyncSession = Depends(db_dependency)
):
    offer_repository = OfferRepository(db)
    offer_service = OfferService(offer_repository)
    try:
        offer = await offer_service.create_offer(offer_create)
        return offer
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating offer")
