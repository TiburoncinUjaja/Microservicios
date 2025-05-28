from sqlalchemy import Column, Integer, String, DateTime, Enum
from datetime import datetime
from app.db.base_class import Base

class Escala(Base):
    __tablename__ = "escalas"

    id = Column(Integer, primary_key=True, index=True)
    vuelo_id = Column(Integer, nullable=False)  # Referencia al servicio de vuelos
    aeropuerto_id = Column(Integer, nullable=False)  # Referencia al servicio de aeropuertos
    numero_escala = Column(Integer, nullable=False)
    orden = Column(Integer, nullable=False)
    fecha_hora_llegada = Column(DateTime, nullable=False)
    fecha_hora_salida = Column(DateTime, nullable=False)
    estado = Column(Enum('PROGRAMADA', 'EN_PROGRESO', 'COMPLETADA', 'CANCELADA'), 
                   default='PROGRAMADA', nullable=False)
    tipo_escala = Column(Enum('TECNICA', 'COMERCIAL'), nullable=False)
    duracion_minutos = Column(Integer, nullable=False)
    terminal = Column(String(50))
    puerta = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 