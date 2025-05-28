from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AvionBase(BaseModel):
    matricula: str = Field(..., min_length=5, max_length=10)
    modelo: str = Field(..., min_length=2, max_length=50)
    capacidad_pasajeros: int = Field(..., gt=0)
    capacidad_carga: int = Field(..., gt=0)
    estado: str = Field(..., pattern="^(ACTIVO|MANTENIMIENTO|INACTIVO)$")
    ultima_revision: Optional[datetime] = None
    proxima_revision: Optional[datetime] = None

class AvionCreate(AvionBase):
    pass

class AvionUpdate(BaseModel):
    matricula: Optional[str] = Field(None, min_length=5, max_length=10)
    modelo: Optional[str] = Field(None, min_length=2, max_length=50)
    capacidad_pasajeros: Optional[int] = Field(None, gt=0)
    capacidad_carga: Optional[int] = Field(None, gt=0)
    estado: Optional[str] = Field(None, pattern="^(ACTIVO|MANTENIMIENTO|INACTIVO)$")
    ultima_revision: Optional[datetime] = None
    proxima_revision: Optional[datetime] = None

class Avion(AvionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 