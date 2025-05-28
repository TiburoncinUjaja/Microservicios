from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum

class EstadoVuelo(str, Enum):
    PROGRAMADO = "PROGRAMADO"
    EN_VUELO = "EN_VUELO"
    COMPLETADO = "COMPLETADO"
    CANCELADO = "CANCELADO"
    RETRASADO = "RETRASADO"

class VueloBase(BaseModel):
    numero_vuelo: str = Field(..., min_length=1, max_length=10)
    fecha_hora_salida: datetime
    fecha_hora_llegada: datetime
    aeropuerto_origen_id: int
    aeropuerto_destino_id: int
    avion_id: int
    estado: EstadoVuelo = EstadoVuelo.PROGRAMADO

class VueloCreate(VueloBase):
    pass

class VueloUpdate(BaseModel):
    numero_vuelo: Optional[str] = Field(None, min_length=1, max_length=10)
    fecha_hora_salida: Optional[datetime] = None
    fecha_hora_llegada: Optional[datetime] = None
    aeropuerto_origen_id: Optional[int] = None
    aeropuerto_destino_id: Optional[int] = None
    avion_id: Optional[int] = None
    estado: Optional[EstadoVuelo] = None

class VueloInDB(VueloBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Vuelo(VueloInDB):
    pass 