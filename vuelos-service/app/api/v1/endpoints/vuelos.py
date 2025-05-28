from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.vuelo import VueloCreate, VueloUpdate, Vuelo as VueloSchema
from app.services.vuelo_service import VueloService

router = APIRouter()

@router.post("/", response_model=VueloSchema, status_code=status.HTTP_201_CREATED)
async def create_vuelo(vuelo: VueloCreate, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    return await vuelo_service.create_vuelo(vuelo)

@router.get("/", response_model=List[VueloSchema])
def read_vuelos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    return vuelo_service.get_vuelos(skip, limit)

@router.get("/{vuelo_id}", response_model=VueloSchema)
def read_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    return vuelo_service.get_vuelo(vuelo_id)

@router.put("/{vuelo_id}", response_model=VueloSchema)
async def update_vuelo(vuelo_id: int, vuelo: VueloUpdate, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    return await vuelo_service.update_vuelo(vuelo_id, vuelo)

@router.delete("/{vuelo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    await vuelo_service.delete_vuelo(vuelo_id)
    return None

@router.get("/numero/{numero_vuelo}", response_model=VueloSchema)
def read_vuelo_by_numero(numero_vuelo: str, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    db_vuelo = vuelo_service.get_vuelo_by_numero(numero_vuelo)
    if db_vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return db_vuelo

@router.get("/estado/{estado}", response_model=List[VueloSchema])
def read_vuelos_by_estado(estado: str, db: Session = Depends(get_db)):
    vuelo_service = VueloService(db)
    vuelos = vuelo_service.get_vuelos_by_estado(estado)
    return vuelos 