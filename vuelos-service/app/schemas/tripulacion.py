from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class RolTripulacion(str, Enum):
    PILOTO = "PILOTO"
    COPILOTO = "COPILOTO"
    ASISTENTE = "ASISTENTE"

class TripulacionBase(BaseModel):
    vuelo_id: int
    personal_id: int
    rol: RolTripulacion

class TripulacionCreate(TripulacionBase):
    pass

class TripulacionUpdate(BaseModel):
    vuelo_id: Optional[int] = None
    personal_id: Optional[int] = None
    rol: Optional[RolTripulacion] = None

class TripulacionInDB(TripulacionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Tripulacion(TripulacionInDB):
    pass 