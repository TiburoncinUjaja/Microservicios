from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...schemas.pasajero import PasajeroCreate, PasajeroUpdate, PasajeroResponse
from ...services.pasajero_service import PasajeroService
from ...core.exceptions import (
    PasajeroNotFoundException,
    PasajeroDuplicadoException,
    DatabaseException,
    ValidationException
)
from ...core.logger import logger

router = APIRouter()

@router.post("/", response_model=PasajeroResponse, status_code=status.HTTP_201_CREATED)
async def create_pasajero(pasajero: PasajeroCreate, db: Session = Depends(get_db)):
    """
    Crear un nuevo pasajero.
    """
    try:
        return await PasajeroService.create_pasajero(db=db, pasajero=pasajero)
    except PasajeroDuplicadoException as e:
        logger.warning(f"Intento de crear pasajero duplicado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationException as e:
        logger.warning(f"Error de validación al crear pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseException as e:
        logger.error(f"Error de base de datos al crear pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/{pasajero_id}", response_model=PasajeroResponse)
def read_pasajero(pasajero_id: int, db: Session = Depends(get_db)):
    """
    Obtener un pasajero por su ID.
    """
    try:
        db_pasajero = PasajeroService.get_pasajero(db, pasajero_id)
        if db_pasajero is None:
            raise HTTPException(status_code=404, detail="Pasajero no encontrado")
        return db_pasajero
    except PasajeroNotFoundException as e:
        logger.warning(f"Pasajero no encontrado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseException as e:
        logger.error(f"Error de base de datos al obtener pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.get("/", response_model=List[PasajeroResponse])
def read_pasajeros(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Obtener lista de pasajeros.
    """
    try:
        return PasajeroService.get_pasajeros(db=db, skip=skip, limit=limit)
    except DatabaseException as e:
        logger.error(f"Error de base de datos al obtener pasajeros: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.put("/{pasajero_id}", response_model=PasajeroResponse)
async def update_pasajero(
    pasajero_id: int,
    pasajero: PasajeroUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un pasajero existente.
    """
    try:
        return await PasajeroService.update_pasajero(
            db=db,
            pasajero_id=pasajero_id,
            pasajero=pasajero
        )
    except PasajeroNotFoundException as e:
        logger.warning(f"Pasajero no encontrado para actualizar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except PasajeroDuplicadoException as e:
        logger.warning(f"Intento de actualizar pasajero con pasaporte duplicado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except ValidationException as e:
        logger.warning(f"Error de validación al actualizar pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except DatabaseException as e:
        logger.error(f"Error de base de datos al actualizar pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.delete("/{pasajero_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pasajero(pasajero_id: int, db: Session = Depends(get_db)):
    """
    Eliminar un pasajero.
    """
    try:
        await PasajeroService.delete_pasajero(db=db, pasajero_id=pasajero_id)
    except PasajeroNotFoundException as e:
        logger.warning(f"Pasajero no encontrado para eliminar: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DatabaseException as e:
        logger.error(f"Error de base de datos al eliminar pasajero: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        ) 