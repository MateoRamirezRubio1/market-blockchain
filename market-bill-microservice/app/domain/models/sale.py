import enum
import datetime
from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey, Boolean, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.infrastructure.database.base import Base
import random


class SaleStatus(str, enum.Enum):
    pending = "pending"  # Venta pendiente de confirmación final
    completed = "completed"  # Venta completada sin penalización
    penalized = "penalized"  # Venta completada con penalización


class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    offer_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("offers.id"), nullable=False, unique=True
    )  # Referencia única a la oferta confirmada
    status: Mapped[SaleStatus] = mapped_column(
        Enum(SaleStatus, name="sale_status"), default=SaleStatus.pending
    )  # Estado de la venta
    confirmation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )  # Fecha de confirmación de la venta
    pdf_document_path: Mapped[str] = mapped_column(
        String, nullable=True
    )  # Ruta al archivo PDF generado para la venta
    penalty_reason: Mapped[str] = mapped_column(
        String, nullable=True
    )  # Razón o descripción de la penalización (si aplica)
    last_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, onupdate=datetime.datetime.utcnow
    )  # Última actualización de la venta

    # Relación con la oferta asociada
    offer = relationship("Offer", back_populates="sale")

    async def verify_sales_compliance(self):
        transfer_datetime_naive = self.offer.transfer_datetime.replace(tzinfo=None)
        random_bool = random.choice([True, False])

        if datetime.datetime.utcnow() >= transfer_datetime_naive:

            print("Making Verification")
            self.status = SaleStatus.penalized if random_bool else SaleStatus.completed
            print("Verification maked")
