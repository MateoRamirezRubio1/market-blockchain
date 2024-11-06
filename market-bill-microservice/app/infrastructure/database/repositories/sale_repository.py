from sqlalchemy.orm import Session
from app.domain.models.sale import Sale
from app.domain.schemas.sale import SaleCreate, SaleStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
import datetime
import logging


class SaleRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_sale(self, sale_data: SaleCreate) -> Sale:
        try:
            sale = Sale(
                offer_id=sale_data.offer_id,
                status=sale_data.status,
                pdf_document_path=sale_data.pdf_document_path,
                penalty_reason=sale_data.penalty_reason,
                confirmation_date=datetime.datetime.utcnow(),
                last_updated=datetime.datetime.utcnow(),
            )
            self.session.add(sale)
            await self.session.commit()
            await self.session.refresh(sale)
            return sale
        except SQLAlchemyError as e:
            logging.error(f"Error creating sale: {e}")
            await self.session.rollback()
            raise e

    async def get_sale_by_offer_id(self, offer_id: int) -> Sale:
        try:
            query = select(Sale).where(Sale.offer_id == offer_id)
            result = await self.session.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            # Puedes loguear el error o manejarlo como quieras
            print(f"Error al obtener la venta con offer_id={offer_id}: {e}")
            # Opcionalmente, puedes lanzar una excepción personalizada o devolver None si no deseas interrumpir la ejecución.
            raise ValueError("Error al obtener la venta") from e
