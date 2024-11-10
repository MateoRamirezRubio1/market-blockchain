from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from app.domain.schemas.offer import OfferResponse


# Definición del enumerador de estado de venta
class SaleStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    penalized = "penalized"


# Esquema base para Sale (común para todos los esquemas de venta)
class SaleBase(BaseModel):
    offer_id: int = Field(..., description="Referencia única a la oferta confirmada")
    status: SaleStatus = Field(
        default=SaleStatus.pending, description="Estado de la venta"
    )
    penalty_reason: Optional[str] = Field(
        None, description="Razón o descripción de la penalización (si aplica)"
    )


# Esquema para crear una venta (sin campos autogenerados)
class SaleCreate(SaleBase):
    buyer_id: Optional[int] = None


# Esquema para leer una venta (incluye todos los campos)
class SaleRead(SaleBase):
    id: int
    confirmation_date: datetime
    last_updated: Optional[datetime] = None
    offer: OfferResponse
    pdf_document_path: Optional[str] = None

    class Config:
        orm_mode = True  # Permite convertir objetos ORM en datos JSON
        from_attributes = True
