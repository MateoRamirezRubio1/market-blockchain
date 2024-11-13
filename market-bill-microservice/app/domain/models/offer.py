from sqlalchemy import Column, Integer, String, Numeric, DateTime, Enum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.infrastructure.database.base import Base
import datetime
import enum


class OfferType(str, enum.Enum):
    buy = "buy"  # Oferta de compra de energía
    sell = "sell"  # Oferta de venta de energía


class OfferStatus(str, enum.Enum):
    draft = "draft"  # Oferta en borrador
    active = "active"  # Oferta activa
    reserved = "reserved"  # Oferta reservada por un comprador
    expired = "expired"  # Oferta caducada
    cancelled = "cancelled"  # Oferta cancelada
    accepted = "accepted"  # Oferta aceptada (promesa de transacción)
    completed = "completed"  # Transacción completada


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    seller_id: Mapped[str] = mapped_column(
        String, nullable=False
    )  # ID del vendedor (usuario)
    buyer_id: Mapped[str] = mapped_column(
        String, nullable=True
    )  # ID del comprador (si aplica)
    energy_amount: Mapped[float] = mapped_column(
        Numeric, nullable=False
    )  # Cantidad de energía ofrecida (en kWh)
    price_per_unit: Mapped[float] = mapped_column(
        Numeric, nullable=False
    )  # Precio por unidad de energía
    offer_type: Mapped[OfferType] = mapped_column(
        Enum(OfferType), nullable=False
    )  # Tipo de oferta (compra o venta)
    status: Mapped[OfferStatus] = mapped_column(
        Enum(OfferStatus), default=OfferStatus.draft
    )  # Estado de la oferta
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow
    )  # Fecha de creación
    expiration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # Fecha de expiración de la oferta
    transfer_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )  # Fecha y hora del traspaso de energía
    terms_conditions: Mapped[str] = mapped_column(
        String, nullable=False
    )  # Términos y condiciones
    last_updated: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow
    )  # Última actualización

    sale = relationship("Sale", back_populates="offer", uselist=False)
