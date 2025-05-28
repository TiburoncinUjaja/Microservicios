from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional
from enum import Enum

class TipoDocumento(str, Enum):
    DNI = "DNI"
    PASAPORTE = "PASAPORTE"
    CE = "CE"

class PasajeroBase(BaseModel):
    tipo_documento: TipoDocumento
    numero_documento: str = Field(..., min_length=1, max_length=20)
    fecha_nacimiento: date
    nacionalidad: str = Field(..., min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, min_length=1, max_length=20)
    direccion: Optional[str] = None

class PasajeroCreate(PasajeroBase):
    usuario_id: int

class PasajeroUpdate(BaseModel):
    tipo_documento: Optional[TipoDocumento] = None
    numero_documento: Optional[str] = Field(None, min_length=1, max_length=20)
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, min_length=1, max_length=20)
    direccion: Optional[str] = None

class PasajeroInDB(PasajeroBase):
    id: int
    usuario_id: int
    fecha_creacion: datetime
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True

class PasajeroResponse(PasajeroInDB):
    pass 