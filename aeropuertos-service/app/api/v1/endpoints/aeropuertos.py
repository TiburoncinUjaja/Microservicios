from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ....database import get_db
from ....models import aeropuerto as models
from ....schemas import aeropuerto as schemas

router = APIRouter()

# Endpoints para Aeropuertos
@router.post("/aeropuertos", response_model=schemas.Aeropuerto)
def create_aeropuerto(aeropuerto: schemas.AeropuertoCreate, db: Session = Depends(get_db)):
    # Verificar si ya existe un aeropuerto con el mismo código IATA
    existing_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.codigo_iata == aeropuerto.codigo_iata).first()
    if existing_aeropuerto:
        raise HTTPException(
            status_code=400,
            detail=f"Ya existe un aeropuerto con el código IATA {aeropuerto.codigo_iata}"
        )
    
    db_aeropuerto = models.Aeropuerto(**aeropuerto.model_dump())
    db.add(db_aeropuerto)
    db.commit()
    db.refresh(db_aeropuerto)
    return db_aeropuerto

@router.get("/aeropuertos", response_model=List[schemas.Aeropuerto])
def read_aeropuertos(
    skip: int = 0,
    limit: int = 100,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Aeropuerto)
    if estado:
        query = query.filter(models.Aeropuerto.estado == estado)
    return query.offset(skip).limit(limit).all()

@router.get("/aeropuertos/{aeropuerto_id}", response_model=schemas.Aeropuerto)
def read_aeropuerto(aeropuerto_id: int, db: Session = Depends(get_db)):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    return db_aeropuerto

@router.get("/aeropuertos/codigo/{codigo_iata}", response_model=schemas.Aeropuerto)
def read_aeropuerto_by_iata(codigo_iata: str, db: Session = Depends(get_db)):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.codigo_iata == codigo_iata).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    return db_aeropuerto

@router.put("/aeropuertos/{aeropuerto_id}", response_model=schemas.Aeropuerto)
def update_aeropuerto(
    aeropuerto_id: int,
    aeropuerto: schemas.AeropuertoUpdate,
    db: Session = Depends(get_db)
):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    for key, value in aeropuerto.model_dump(exclude_unset=True).items():
        setattr(db_aeropuerto, key, value)
    
    db.commit()
    db.refresh(db_aeropuerto)
    return db_aeropuerto

@router.delete("/aeropuertos/{aeropuerto_id}")
def delete_aeropuerto(aeropuerto_id: int, db: Session = Depends(get_db)):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    db.delete(db_aeropuerto)
    db.commit()
    return {"message": "Aeropuerto eliminado"}

# Endpoints para Terminales
@router.post("/aeropuertos/{aeropuerto_id}/terminales", response_model=schemas.Terminal)
def create_terminal(
    aeropuerto_id: int,
    terminal: schemas.TerminalCreate,
    db: Session = Depends(get_db)
):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    db_terminal = models.Terminal(**terminal.model_dump(), aeropuerto_id=aeropuerto_id)
    db.add(db_terminal)
    db.commit()
    db.refresh(db_terminal)
    return db_terminal

@router.get("/aeropuertos/{aeropuerto_id}/terminales", response_model=List[schemas.Terminal])
def read_terminales(
    aeropuerto_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    return db.query(models.Terminal).filter(
        models.Terminal.aeropuerto_id == aeropuerto_id
    ).offset(skip).limit(limit).all()

# Endpoints para Pistas
@router.post("/aeropuertos/{aeropuerto_id}/pistas", response_model=schemas.Pista)
def create_pista(
    aeropuerto_id: int,
    pista: schemas.PistaCreate,
    db: Session = Depends(get_db)
):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    db_pista = models.Pista(**pista.model_dump(), aeropuerto_id=aeropuerto_id)
    db.add(db_pista)
    db.commit()
    db.refresh(db_pista)
    return db_pista

@router.get("/aeropuertos/{aeropuerto_id}/pistas", response_model=List[schemas.Pista])
def read_pistas(
    aeropuerto_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    db_aeropuerto = db.query(models.Aeropuerto).filter(models.Aeropuerto.id == aeropuerto_id).first()
    if db_aeropuerto is None:
        raise HTTPException(status_code=404, detail="Aeropuerto no encontrado")
    
    return db.query(models.Pista).filter(
        models.Pista.aeropuerto_id == aeropuerto_id
    ).offset(skip).limit(limit).all() 