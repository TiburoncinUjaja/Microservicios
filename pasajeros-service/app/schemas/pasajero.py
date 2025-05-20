from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class PasajeroBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)
    apellidos: str = Field(..., min_length=1, max_length=100)
    nacionalidad: str = Field(..., min_length=1, max_length=50)
    numero_pasaporte: str = Field(..., min_length=1, max_length=20)
    fecha_nacimiento: date

class PasajeroCreate(PasajeroBase):
    pass

class PasajeroUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=50)
    apellidos: Optional[str] = Field(None, min_length=1, max_length=100)
    nacionalidad: Optional[str] = Field(None, min_length=1, max_length=50)
    numero_pasaporte: Optional[str] = Field(None, min_length=1, max_length=20)
    fecha_nacimiento: Optional[date] = None

class PasajeroInDB(PasajeroBase):
    id: int

    class Config:
        from_attributes = True

class PasajeroResponse(PasajeroInDB):
    pass 