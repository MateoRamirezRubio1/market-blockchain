from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.offer import OfferCreate, OfferResponse, OfferStatus
from app.services.offer_service import OfferService
from app.infrastructure.database.repositories.offer_repository import OfferRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.database.db_connection import db_dependency

router = APIRouter()


def get_offer_service(db: AsyncSession = Depends(db_dependency)) -> OfferService:
    offer_repository = OfferRepository(db)
    return OfferService(offer_repository)


@router.post(
    "/",
    response_model=OfferResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "Offer created successfully"},
    },
)
async def create_offer(
    offer_create: OfferCreate, offer_service: OfferService = Depends(get_offer_service)
):
    try:
        offer = await offer_service.create_offer(offer_create)
        return offer
    except Exception as e:
        raise HTTPException(status_code=400, detail="Error creating offer")


@router.put("/{offer_id}/activate")
async def activate_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await offer_service.update_offer_status(offer_id, OfferStatus.active)


@router.put("/{offer_id}/cancel")
async def cancel_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await offer_service.update_offer_status(offer_id, OfferStatus.cancelled)


@router.put("/{offer_id}/accept")
async def accept_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await offer_service.update_offer_status(offer_id, OfferStatus.accepted)


@router.put("/{offer_id}/complete")
async def complete_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await offer_service.update_offer_status(offer_id, OfferStatus.completed)
