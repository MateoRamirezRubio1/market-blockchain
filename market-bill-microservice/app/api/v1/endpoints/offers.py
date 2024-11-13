from fastapi import APIRouter, Depends, HTTPException, status
from app.domain.schemas.offer import OfferCreate, OfferResponse, OfferStatus
from app.services.offer_service import OfferService, InvalidStateTransitionError
from app.infrastructure.database.repositories.offer_repository import (
    OfferRepository,
    OfferNotFoundError,
)
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
        raise HTTPException(status_code=400, detail="Error creating offer") from e


@router.get(
    "/offers", status_code=status.HTTP_200_OK, response_model=list[OfferResponse]
)
async def list_offers(offer_service: OfferService = Depends(get_offer_service)):
    try:
        offers = await offer_service.get_all_offers()
        return offers
    except OfferNotFoundError as e:
        # Si no hay ofertas, devolvemos un 404 con el mensaje adecuado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.get(
    "/offers/{offer_id}", status_code=status.HTTP_200_OK, response_model=OfferResponse
)
async def get_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    try:
        offer = await offer_service.get_offer_by_id(offer_id)
        return offer
    except OfferNotFoundError as e:
        # Si la oferta no se encuentra, devolvemos un 404 con el mensaje adecuado
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


async def change_offer_status_with_error_handling(offer_service, offer_id, new_status):
    try:
        return await offer_service.update_offer_status(offer_id, new_status)
    except InvalidStateTransitionError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid state transition: {e.message}",
        ) from e


@router.put("/{offer_id}/activate", status_code=status.HTTP_200_OK)
async def activate_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await change_offer_status_with_error_handling(
        offer_service, offer_id, OfferStatus.active
    )


@router.put("/{offer_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await change_offer_status_with_error_handling(
        offer_service, offer_id, OfferStatus.cancelled
    )


@router.put("/{offer_id}/accept", status_code=status.HTTP_200_OK)
async def accept_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await change_offer_status_with_error_handling(
        offer_service, offer_id, OfferStatus.accepted
    )


@router.put("/{offer_id}/complete", status_code=status.HTTP_200_OK)
async def complete_offer(
    offer_id: int, offer_service: OfferService = Depends(get_offer_service)
):
    return await change_offer_status_with_error_handling(
        offer_service, offer_id, OfferStatus.completed
    )
