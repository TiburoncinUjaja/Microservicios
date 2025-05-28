from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import logging

from app.db.session import get_db
from app.models.escala import Escala
from app.schemas.escala import EscalaCreate, EscalaUpdate, Escala as EscalaSchema
from app.services.escala_service import EscalaService

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=List[EscalaSchema])
def get_escalas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener todas las escalas con paginación
    """
    return db.query(Escala).offset(skip).limit(limit).all()

@router.post("/", response_model=EscalaSchema, status_code=status.HTTP_201_CREATED)
def create_escala(escala: EscalaCreate, db: Session = Depends(get_db)):
    """
    Crear una nueva escala
    """
    db_escala = Escala(**escala.model_dump())
    db.add(db_escala)
    db.commit()
    db.refresh(db_escala)
    return db_escala

@router.get("/{escala_id}", response_model=EscalaSchema)
def get_escala(escala_id: int, db: Session = Depends(get_db)):
    """
    Obtener una escala por su ID
    """
    escala = db.query(Escala).filter(Escala.id == escala_id).first()
    if not escala:
        raise HTTPException(status_code=404, detail="Escala no encontrada")
    return escala

@router.get("/vuelo/{vuelo_id}", response_model=List[EscalaSchema])
def get_escalas_by_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las escalas de un vuelo específico
    """
    return db.query(Escala).filter(Escala.vuelo_id == vuelo_id).order_by(Escala.orden).all()

@router.get("/aeropuerto/{aeropuerto_id}", response_model=List[EscalaSchema])
def get_escalas_by_aeropuerto(aeropuerto_id: int, db: Session = Depends(get_db)):
    """
    Obtener todas las escalas de un aeropuerto específico
    """
    return db.query(Escala).filter(Escala.aeropuerto_id == aeropuerto_id).all()

@router.put("/{escala_id}", response_model=EscalaSchema)
def update_escala(escala_id: int, escala: EscalaUpdate, db: Session = Depends(get_db)):
    """
    Actualizar una escala existente
    """
    db_escala = db.query(Escala).filter(Escala.id == escala_id).first()
    if not db_escala:
        raise HTTPException(status_code=404, detail="Escala no encontrada")
    
    # Actualizar solo los campos proporcionados
    update_data = escala.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_escala, field, value)
    
    db_escala.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_escala)
    return db_escala

@router.delete("/{escala_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_escala(escala_id: int, db: Session = Depends(get_db)):
    """
    Eliminar una escala
    """
    escala = db.query(Escala).filter(Escala.id == escala_id).first()
    if not escala:
        raise HTTPException(status_code=404, detail="Escala no encontrada")
    
    db.delete(escala)
    db.commit()
    return None

@router.patch("/{escala_id}/estado", response_model=EscalaSchema)
def update_estado_escala(escala_id: int, estado: str, db: Session = Depends(get_db)):
    escala_service = EscalaService(db)
    updated_escala = escala_service.update_estado_escala(escala_id, estado)
    if not updated_escala:
        raise HTTPException(status_code=404, detail="Escala no encontrada")
    return updated_escala 