from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid
from datetime import datetime

from app.core.database import get_db
from app.models.reserva import Reserva, EstadoReserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate, Reserva as ReservaSchema
from app.services.reserva_service import ReservaService

router = APIRouter()

@router.get("/", response_model=List[ReservaSchema])
def get_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las reservas con paginación
    """
    return db.query(Reserva).offset(skip).limit(limit).all()

@router.post("/", response_model=ReservaSchema, status_code=status.HTTP_201_CREATED)
def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    # Generar código de reserva único
    codigo_reserva = str(uuid.uuid4())[:8].upper()
    
    # Crear nueva reserva
    db_reserva = Reserva(
        **reserva.model_dump(),
        codigo_reserva=codigo_reserva,
        estado=EstadoReserva.PENDIENTE
    )
    
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@router.get("/{reserva_id}", response_model=ReservaSchema)
def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.get("/codigo/{codigo_reserva}", response_model=ReservaSchema)
def get_reserva_by_codigo(codigo_reserva: str, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.codigo_reserva == codigo_reserva).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.get("/pasajero/{pasajero_id}", response_model=List[ReservaSchema])
def get_reservas_by_pasajero(pasajero_id: int, db: Session = Depends(get_db)):
    return db.query(Reserva).filter(Reserva.pasajero_id == pasajero_id).all()

@router.get("/vuelo/{vuelo_id}", response_model=List[ReservaSchema])
def get_reservas_by_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    return db.query(Reserva).filter(Reserva.vuelo_id == vuelo_id).all()

@router.put("/{reserva_id}", response_model=ReservaSchema)
def update_reserva(reserva_id: int, reserva: ReservaUpdate, db: Session = Depends(get_db)):
    db_reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Actualizar solo los campos proporcionados
    update_data = reserva.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_reserva, field, value)
    
    db_reserva.fecha_actualizacion = datetime.utcnow()
    db.commit()
    db.refresh(db_reserva)
    return db_reserva

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reserva(reserva_id: int, db: Session = Depends(get_db)):
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    db.delete(reserva)
    db.commit()
    return None 