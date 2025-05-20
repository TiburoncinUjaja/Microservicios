from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.reserva import EstadoReserva

class ReservaBase(BaseModel):
    pasajero_id: int
    vuelo_id: int
    asiento: str
    precio: int
    clase: str

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    estado: Optional[EstadoReserva] = None
    asiento: Optional[str] = None
    precio: Optional[int] = None
    clase: Optional[str] = None

class ReservaInDB(ReservaBase):
    id: int
    estado: EstadoReserva
    codigo_reserva: str
    fecha_reserva: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True

class Reserva(ReservaInDB):
    pass 