from app.infrastructure.database.repositories.offer_repository import OfferRepository
from app.domain.schemas.offer import OfferCreate, OfferResponse, OfferStatus
from app.domain.models.offer import Offer


# Exceptions
class OfferNotFoundError(Exception):
    pass


class InvalidStateTransitionError(Exception):
    pass


class OfferService:
    def __init__(self, offer_repository: OfferRepository):
        self.offer_repository = offer_repository

    async def create_offer(self, offer_create: OfferCreate) -> Offer:
        return await self.offer_repository.create_offer(offer_create)

    async def update_offer_status(
        self, offer_id: int, new_status: OfferStatus, comes_from_sale: bool = False
    ) -> OfferResponse:
        offer = await self.offer_repository.get_offer_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError("Offer not found")

        # Validaciones de estado: solo ciertos cambios de estado estén permitidos
        if offer.status == OfferStatus.draft and new_status == OfferStatus.active:
            offer.status = new_status
        elif offer.status == OfferStatus.active and new_status in [
            OfferStatus.accepted,
            OfferStatus.cancelled,
        ]:
            offer.status = new_status
        elif (
            offer.status == OfferStatus.accepted and new_status == OfferStatus.completed
        ):
            offer.status = new_status
        else:
            raise InvalidStateTransitionError("Invalid state transition")

        (
            await self.offer_repository.save_with_commit(offer)
            if not comes_from_sale
            else await self.offer_repository.save_with_flush(offer)
        )

        return offer

    async def update_buyer_offer(self, offer_id: int, buyer_id: int) -> OfferResponse:
        offer = await self.offer_repository.get_offer_by_id(offer_id)
        if not offer:
            raise OfferNotFoundError("Offer not found")

        if offer.buyer_id:
            raise ValueError("Already buyer exists")

        offer.buyer_id = buyer_id

        await self.offer_repository.save_with_flush(offer)
        return offer
