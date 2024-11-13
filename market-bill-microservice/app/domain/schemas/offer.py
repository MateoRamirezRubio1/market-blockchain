from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class OfferType(str, Enum):
    buy = "buy"
    sell = "sell"


class OfferStatus(str, Enum):
    draft = "draft"
    active = "active"
    reserved = "reserved"
    expired = "expired"
    cancelled = "cancelled"
    accepted = "accepted"
    completed = "completed"


# Esquema de entrada (para crear o actualizar una oferta)
class OfferCreate(BaseModel):
    seller_id: str
    energy_amount: float  # Cantidad de energía ofrecida (en kWh)
    price_per_unit: float  # Precio por unidad de energía
    offer_type: OfferType  # Tipo de oferta (compra o venta)
    expiration_time: datetime  # Fecha de expiración de la oferta
    transfer_datetime: datetime  # Fecha y hora del traspaso de energía
    terms_conditions: str  # Términos y condiciones


# Esquema de salida (cuando se obtiene la oferta desde la API)
class OfferResponse(OfferCreate):
    id: int
    status: OfferStatus  # Estado actual de la oferta
    created_at: datetime  # Fecha de creación
    last_updated: Optional[datetime] = None  # Última actualización (opcional)
    buyer_id: Optional[str] = None

    class Config:
        orm_mode = True
        from_attributes = True
