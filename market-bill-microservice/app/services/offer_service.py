from app.infrastructure.database.repositories.offer_repository import OfferRepository
from app.domain.schemas.offer import OfferCreate
from app.domain.models.offer import Offer


class OfferService:
    def __init__(self, offer_repository: OfferRepository):
        self.offer_repository = offer_repository

    async def create_offer(self, offer_create: OfferCreate) -> Offer:
        return await self.offer_repository.create_offer(offer_create)
