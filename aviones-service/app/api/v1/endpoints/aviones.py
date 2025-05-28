from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.avion import AvionCreate, AvionUpdate, Avion as AvionSchema
from app.services.avion_service import AvionService

router = APIRouter()

@router.post("/", response_model=AvionSchema, status_code=status.HTTP_201_CREATED)
async def create_avion(avion: AvionCreate, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return await avion_service.create_avion(avion)

@router.get("/", response_model=List[AvionSchema])
def read_aviones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return avion_service.get_aviones(skip, limit)

@router.get("/{avion_id}", response_model=AvionSchema)
def read_avion(avion_id: int, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return avion_service.get_avion(avion_id)

@router.get("/matricula/{matricula}", response_model=AvionSchema)
def read_avion_by_matricula(matricula: str, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return avion_service.get_avion_by_matricula(matricula)

@router.get("/estado/{estado}", response_model=List[AvionSchema])
def read_aviones_by_estado(estado: str, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return avion_service.get_aviones_by_estado(estado)

@router.put("/{avion_id}", response_model=AvionSchema)
async def update_avion(avion_id: int, avion: AvionUpdate, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return await avion_service.update_avion(avion_id, avion)

@router.delete("/{avion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_avion(avion_id: int, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    await avion_service.delete_avion(avion_id)
    return None

@router.put("/{avion_id}/mantenimiento", response_model=AvionSchema)
async def update_mantenimiento(avion_id: int, estado: str, db: Session = Depends(get_db)):
    avion_service = AvionService(db)
    return await avion_service.actualizar_estado_mantenimiento(avion_id, estado) 