from sqlalchemy.orm import Session
from app.domain.models.sale import Sale
from app.domain.schemas.sale import SaleCreate, SaleStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import datetime
import logging
from sqlalchemy.orm import selectinload


class SaleNotFoundError(Exception):
    pass


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_sale(self, sale_data: SaleCreate) -> Sale:
        try:
            sale = Sale(
                offer_id=sale_data.offer_id,
                status=sale_data.status,
                penalty_reason=sale_data.penalty_reason,
                confirmation_date=datetime.datetime.utcnow(),
                last_updated=datetime.datetime.utcnow(),
            )
            self.session.add(sale)
            await self.session.flush()
            await self.session.refresh(sale, ["offer"])
            return sale
        except SQLAlchemyError as e:
            logging.error(f"Error creating sale: {e}")
            await self.session.rollback()
            raise e

    async def get_all_sales(self):
        result = await self.session.execute(
            select(Sale).options(selectinload(Sale.offer))
        )
        sales = result.scalars().all()
        if not sales:
            raise SaleNotFoundError("No offers available at the moment.")
        return sales

    async def get_sale_by_id(self, sale_id: int) -> Sale:
        query = select(Sale).options(selectinload(Sale.offer)).where(Sale.id == sale_id)
        result = await self.session.execute(query)
        sale = result.scalars().first()
        if not sale:
            raise SaleNotFoundError(f"Offer with ID {sale_id} not found.")
        return sale

    async def get_sale_by_offer_id(self, offer_id: int) -> Sale:
        try:
            query = (
                select(Sale)
                .options(selectinload(Sale.offer))
                .where(Sale.offer_id == offer_id)
            )
            result = await self.session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            # Puedes loguear el error o manejarlo como quieras
            print(f"Error al obtener la venta con offer_id={offer_id}: {e}")

            raise ValueError("Error al obtener la venta") from e

    async def delete_sale(self, sale_id: int) -> None:
        try:
            query = select(Sale).where(Sale.id == sale_id)
            result = await self.session.execute(query)
            sale = result.scalars().first()
            if sale:
                await self.session.delete(sale)
                await self.session.commit()
                await self.session.refresh(sale, ["offer"])
                logging.info(f"Sale with ID {sale_id} has been deleted successfully.")
        except SQLAlchemyError as e:
            logging.error(f"Error deleting sale with ID {sale_id}: {e}")
            await self.session.rollback()
            raise e

    async def save_with_flush(self, sale: Sale):
        await self.session.flush()
        await self.session.refresh(sale)
        return sale
