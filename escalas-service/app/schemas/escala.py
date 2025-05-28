from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class TipoEscala(str, Enum):
    TECNICA = "TECNICA"
    COMERCIAL = "COMERCIAL"

class EstadoEscala(str, Enum):
    PROGRAMADA = "PROGRAMADA"
    EN_PROGRESO = "EN_PROGRESO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"

class EscalaBase(BaseModel):
    vuelo_id: int
    aeropuerto_id: int
    numero_escala: int
    orden: int
    fecha_hora_llegada: datetime
    fecha_hora_salida: datetime
    estado: EstadoEscala = EstadoEscala.PROGRAMADA
    tipo_escala: TipoEscala
    duracion_minutos: int
    terminal: Optional[str] = None
    puerta: Optional[str] = None

class EscalaCreate(EscalaBase):
    pass

class EscalaUpdate(BaseModel):
    numero_escala: Optional[int] = None
    orden: Optional[int] = None
    fecha_hora_llegada: Optional[datetime] = None
    fecha_hora_salida: Optional[datetime] = None
    estado: Optional[EstadoEscala] = None
    tipo_escala: Optional[TipoEscala] = None
    duracion_minutos: Optional[int] = None
    terminal: Optional[str] = None
    puerta: Optional[str] = None

class EscalaInDB(EscalaBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Escala(EscalaInDB):
    pass 