from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.tripulacion import TripulacionVuelo
from app.schemas.tripulacion import TripulacionCreate, TripulacionUpdate, Tripulacion as TripulacionSchema

router = APIRouter()

@router.post("/", response_model=TripulacionSchema, status_code=status.HTTP_201_CREATED)
def create_tripulacion(tripulacion: TripulacionCreate, db: Session = Depends(get_db)):
    db_tripulacion = TripulacionVuelo(**tripulacion.dict())
    db.add(db_tripulacion)
    db.commit()
    db.refresh(db_tripulacion)
    return db_tripulacion

@router.get("/", response_model=List[TripulacionSchema])
def read_tripulacion(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tripulacion = db.query(TripulacionVuelo).offset(skip).limit(limit).all()
    return tripulacion

@router.get("/{tripulacion_id}", response_model=TripulacionSchema)
def read_tripulacion_by_id(tripulacion_id: int, db: Session = Depends(get_db)):
    db_tripulacion = db.query(TripulacionVuelo).filter(TripulacionVuelo.id == tripulacion_id).first()
    if db_tripulacion is None:
        raise HTTPException(status_code=404, detail="Tripulación no encontrada")
    return db_tripulacion

@router.get("/vuelo/{vuelo_id}", response_model=List[TripulacionSchema])
def read_tripulacion_by_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    tripulacion = db.query(TripulacionVuelo).filter(TripulacionVuelo.vuelo_id == vuelo_id).all()
    return tripulacion

@router.put("/{tripulacion_id}", response_model=TripulacionSchema)
def update_tripulacion(tripulacion_id: int, tripulacion: TripulacionUpdate, db: Session = Depends(get_db)):
    db_tripulacion = db.query(TripulacionVuelo).filter(TripulacionVuelo.id == tripulacion_id).first()
    if db_tripulacion is None:
        raise HTTPException(status_code=404, detail="Tripulación no encontrada")
    
    update_data = tripulacion.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tripulacion, field, value)
    
    db.commit()
    db.refresh(db_tripulacion)
    return db_tripulacion

@router.delete("/{tripulacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tripulacion(tripulacion_id: int, db: Session = Depends(get_db)):
    db_tripulacion = db.query(TripulacionVuelo).filter(TripulacionVuelo.id == tripulacion_id).first()
    if db_tripulacion is None:
        raise HTTPException(status_code=404, detail="Tripulación no encontrada")
    
    db.delete(db_tripulacion)
    db.commit()
    return None 