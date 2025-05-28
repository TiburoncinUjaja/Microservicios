from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.database import Base

class Personal(Base):
    __tablename__ = "personal"

    id = Column(Integer, primary_key=True, index=True)
    numero_empleado = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    tipo = Column(
        Enum("PILOTO", "COPILOTO", "ASISTENTE"),
        nullable=False
    )
    estado = Column(
        Enum("ACTIVO", "INACTIVO", "VACACIONES"),
        nullable=False,
        default="ACTIVO"
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 