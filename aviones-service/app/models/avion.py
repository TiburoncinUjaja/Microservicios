from sqlalchemy import Column, Integer, String, Enum, DateTime
from datetime import datetime
from app.database import Base

class Avion(Base):
    __tablename__ = "aviones"

    id = Column(Integer, primary_key=True, index=True)
    matricula = Column(String(10), unique=True, nullable=False)
    modelo = Column(String(50), nullable=False)
    capacidad_pasajeros = Column(Integer, nullable=False)
    capacidad_carga = Column(Integer, nullable=False)  # en kg
    estado = Column(
        Enum("ACTIVO", "MANTENIMIENTO", "INACTIVO"),
        nullable=False,
        default="ACTIVO"
    )
    ultima_revision = Column(DateTime, nullable=True)
    proxima_revision = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 