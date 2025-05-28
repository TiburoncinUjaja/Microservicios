from sqlalchemy import Column, Integer, String, Date, ForeignKey, Enum, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..core.database import Base

class Pasajero(Base):
    __tablename__ = "pasajeros"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_documento = Column(Enum('DNI', 'PASAPORTE', 'CE', name='tipo_documento_enum'), nullable=False)
    numero_documento = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    nacionalidad = Column(String(100), nullable=False)
    telefono = Column(String(20))
    direccion = Column(Text)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con Usuario
    usuario = relationship("Usuario", back_populates="pasajero") 