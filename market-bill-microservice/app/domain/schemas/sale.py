from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# Definición del enumerador de estado de venta
class SaleStatus(str, Enum):
    pending = "pending"
    completed = "completed"
    penalized = "penalized"


# Esquema base para Sale (común para todos los esquemas de venta)
class SaleBase(BaseModel):
    offer_id: int = Field(..., description="Referencia única a la oferta confirmada")
    buyer: str
    status: SaleStatus = Field(
        default=SaleStatus.pending, description="Estado de la venta"
    )
    pdf_document_path: str = Field(
        ..., description="Ruta al archivo PDF generado para la venta"
    )
    penalty_reason: Optional[str] = Field(
        None, description="Razón o descripción de la penalización (si aplica)"
    )


# Esquema para crear una venta (sin campos autogenerados)
class SaleCreate(SaleBase):
    pass


# Esquema para leer una venta (incluye todos los campos)
class SaleRead(SaleBase):
    id: int
    confirmation_date: datetime
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True  # Permite convertir objetos ORM en datos JSON


class TradeData(BaseModel):
    buyer: str
    contractTermsHash: str
