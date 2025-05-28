from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    numero_vuelo = Column(String(10), unique=True, nullable=False)
    fecha_hora_salida = Column(DateTime, nullable=False)
    fecha_hora_llegada = Column(DateTime, nullable=False)
    # Estos campos son referencias a IDs en otros servicios, no son claves foráneas
    aeropuerto_origen_id = Column(Integer, nullable=False)  # Referencia al servicio de aeropuertos
    aeropuerto_destino_id = Column(Integer, nullable=False)  # Referencia al servicio de aeropuertos
    avion_id = Column(Integer, nullable=False)  # Referencia al servicio de aviones
    estado = Column(
        Enum("PROGRAMADO", "EN_VUELO", "COMPLETADO", "CANCELADO", "RETRASADO"),
        nullable=False,
        default="PROGRAMADO"
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    tripulacion = relationship("TripulacionVuelo", back_populates="vuelo") 