from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class Aeropuerto(Base):
    __tablename__ = "aeropuertos"

    id = Column(Integer, primary_key=True, index=True)
    codigo_iata = Column(String(3), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    ciudad = Column(String(100), nullable=False)
    pais = Column(String(100), nullable=False)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    zona_horaria = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    terminales = relationship("Terminal", back_populates="aeropuerto", cascade="all, delete-orphan")
    pistas = relationship("Pista", back_populates="aeropuerto", cascade="all, delete-orphan")

class Terminal(Base):
    __tablename__ = "terminales"

    id = Column(Integer, primary_key=True, index=True)
    aeropuerto_id = Column(Integer, ForeignKey("aeropuertos.id"))
    nombre = Column(String(50), nullable=False)
    capacidad_pasajeros = Column(Integer, nullable=False)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    aeropuerto = relationship("Aeropuerto", back_populates="terminales")

class Pista(Base):
    __tablename__ = "pistas"

    id = Column(Integer, primary_key=True, index=True)
    aeropuerto_id = Column(Integer, ForeignKey("aeropuertos.id"))
    numero = Column(String(10), nullable=False)
    longitud_metros = Column(Integer, nullable=False)
    ancho_metros = Column(Integer, nullable=False)
    superficie = Column(String(50), nullable=False)
    estado = Column(String(20), nullable=False, default="ACTIVO")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    aeropuerto = relationship("Aeropuerto", back_populates="pistas") 