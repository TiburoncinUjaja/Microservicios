from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class EstadoReserva(str, enum.Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    pasajero_id = Column(Integer, nullable=False)
    vuelo_id = Column(Integer, nullable=False)
    asiento = Column(String(10), nullable=False)
    estado = Column(Enum(EstadoReserva), default=EstadoReserva.PENDIENTE)
    fecha_reserva = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Campos adicionales
    codigo_reserva = Column(String(10), unique=True, index=True)
    precio = Column(Integer, nullable=False)
    clase = Column(String(20), nullable=False)  # Primera clase, Económica, etc. 