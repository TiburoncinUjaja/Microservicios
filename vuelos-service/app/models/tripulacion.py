from sqlalchemy import Column, Integer, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class TripulacionVuelo(Base):
    __tablename__ = "tripulacion_vuelo"

    id = Column(Integer, primary_key=True, index=True)
    vuelo_id = Column(Integer, ForeignKey("vuelos.id"), nullable=False)
    personal_id = Column(Integer, ForeignKey("personal.id"), nullable=False)
    rol = Column(
        Enum("PILOTO", "COPILOTO", "ASISTENTE"),
        nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relaciones
    vuelo = relationship("Vuelo", back_populates="tripulacion") 