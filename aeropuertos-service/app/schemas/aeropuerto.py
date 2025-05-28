from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Esquemas base
class TerminalBase(BaseModel):
    nombre: str
    capacidad_pasajeros: int
    estado: str = "ACTIVO"

class PistaBase(BaseModel):
    numero: str
    longitud_metros: int
    ancho_metros: int
    superficie: str
    estado: str = "ACTIVO"

class AeropuertoBase(BaseModel):
    codigo_iata: str = Field(..., min_length=3, max_length=3)
    nombre: str
    ciudad: str
    pais: str
    latitud: float
    longitud: float
    zona_horaria: str
    estado: str = "ACTIVO"

# Esquemas para crear
class TerminalCreate(TerminalBase):
    pass

class PistaCreate(PistaBase):
    pass

class AeropuertoCreate(AeropuertoBase):
    pass

# Esquemas para actualizar
class TerminalUpdate(TerminalBase):
    nombre: Optional[str] = None
    capacidad_pasajeros: Optional[int] = None
    estado: Optional[str] = None

class PistaUpdate(PistaBase):
    numero: Optional[str] = None
    longitud_metros: Optional[int] = None
    ancho_metros: Optional[int] = None
    superficie: Optional[str] = None
    estado: Optional[str] = None

class AeropuertoUpdate(AeropuertoBase):
    codigo_iata: Optional[str] = None
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    zona_horaria: Optional[str] = None
    estado: Optional[str] = None

# Esquemas para respuesta
class Terminal(TerminalBase):
    id: int
    aeropuerto_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Pista(PistaBase):
    id: int
    aeropuerto_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Aeropuerto(AeropuertoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    terminales: List[Terminal] = []
    pistas: List[Pista] = []

    class Config:
        from_attributes = True 