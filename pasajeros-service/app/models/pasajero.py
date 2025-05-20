from sqlalchemy import Column, Integer, String, Date
from ..core.database import Base

class Pasajero(Base):
    __tablename__ = "pasajeros"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellidos = Column(String(100), nullable=False)
    nacionalidad = Column(String(50), nullable=False)
    numero_pasaporte = Column(String(20), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False) 