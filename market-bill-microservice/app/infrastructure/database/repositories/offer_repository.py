from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from app.domain.models.offer import Offer
from app.domain.schemas.offer import OfferCreate
from sqlalchemy.exc import SQLAlchemyError
import logging


def convert_to_naive(dt):
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


class OfferRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_offer(self, offer_data: OfferCreate) -> Offer:
        try:
            offer = Offer(
                seller_id=offer_data.seller_id,
                energy_amount=offer_data.energy_amount,
                price_per_unit=offer_data.price_per_unit,
                offer_type=offer_data.offer_type.value.lower(),
                expiration_time=convert_to_naive(offer_data.expiration_time),
                transfer_datetime=convert_to_naive(offer_data.transfer_datetime),
                terms_conditions=offer_data.terms_conditions,
            )
            self.session.add(offer)
            await self.session.commit()
            await self.session.refresh(offer)
            return offer
        except SQLAlchemyError as e:
            logging.error(f"Error creating offer: {e}")
            await self.session.rollback()
            raise e
