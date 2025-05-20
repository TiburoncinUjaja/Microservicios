from sqlalchemy.orm import Session
from ..models.pasajero import Pasajero
from ..schemas.pasajero import PasajeroCreate, PasajeroUpdate
from typing import List, Optional
from ..core.exceptions import (
    PasajeroNotFoundException,
    PasajeroDuplicadoException,
    DatabaseException
)
from ..core.logger import logger
from ..core.events import EventTypes, publish_pasajero_event
from sqlalchemy.exc import SQLAlchemyError

class PasajeroService:
    @staticmethod
    def get_pasajero(db: Session, pasajero_id: int) -> Optional[Pasajero]:
        try:
            pasajero = db.query(Pasajero).filter(Pasajero.id == pasajero_id).first()
            if not pasajero:
                logger.warning(f"Pasajero no encontrado con ID: {pasajero_id}")
                raise PasajeroNotFoundException(pasajero_id)
            return pasajero
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos al obtener pasajero {pasajero_id}: {str(e)}")
            raise DatabaseException(str(e))

    @staticmethod
    def get_pasajero_by_pasaporte(db: Session, numero_pasaporte: str) -> Optional[Pasajero]:
        try:
            return db.query(Pasajero).filter(Pasajero.numero_pasaporte == numero_pasaporte).first()
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos al buscar pasajero con pasaporte {numero_pasaporte}: {str(e)}")
            raise DatabaseException(str(e))

    @staticmethod
    def get_pasajeros(db: Session, skip: int = 0, limit: int = 100) -> List[Pasajero]:
        try:
            pasajeros = db.query(Pasajero).offset(skip).limit(limit).all()
            logger.info(f"Obtenidos {len(pasajeros)} pasajeros (skip={skip}, limit={limit})")
            return pasajeros
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos al listar pasajeros: {str(e)}")
            raise DatabaseException(str(e))

    @staticmethod
    async def create_pasajero(db: Session, pasajero: PasajeroCreate) -> Pasajero:
        try:
            # Verificar si ya existe un pasajero con el mismo número de pasaporte
            db_pasajero = PasajeroService.get_pasajero_by_pasaporte(db, pasajero.numero_pasaporte)
            if db_pasajero:
                logger.warning(f"Intento de crear pasajero con pasaporte duplicado: {pasajero.numero_pasaporte}")
                raise PasajeroDuplicadoException(pasajero.numero_pasaporte)
            
            # Crear nuevo pasajero
            db_pasajero = Pasajero(**pasajero.model_dump())
            db.add(db_pasajero)
            db.commit()
            db.refresh(db_pasajero)
            
            # Publicar evento de pasajero creado
            await publish_pasajero_event(
                EventTypes.PASAJERO_CREADO,
                {
                    "id": db_pasajero.id,
                    "nombre": db_pasajero.nombre,
                    "apellido": db_pasajero.apellido,
                    "numero_pasaporte": db_pasajero.numero_pasaporte,
                    "email": db_pasajero.email
                }
            )
            
            logger.info(f"Pasajero creado exitosamente con ID: {db_pasajero.id}")
            return db_pasajero
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error de base de datos al crear pasajero: {str(e)}")
            raise DatabaseException(str(e))

    @staticmethod
    async def update_pasajero(db: Session, pasajero_id: int, pasajero: PasajeroUpdate) -> Optional[Pasajero]:
        try:
            db_pasajero = PasajeroService.get_pasajero(db, pasajero_id)

            # Verificar si el nuevo número de pasaporte ya existe
            if pasajero.numero_pasaporte and pasajero.numero_pasaporte != db_pasajero.numero_pasaporte:
                existing_pasajero = PasajeroService.get_pasajero_by_pasaporte(db, pasajero.numero_pasaporte)
                if existing_pasajero:
                    logger.warning(f"Intento de actualizar pasajero {pasajero_id} con pasaporte duplicado: {pasajero.numero_pasaporte}")
                    raise PasajeroDuplicadoException(pasajero.numero_pasaporte)

            # Guardar datos antiguos para el evento
            old_data = {
                "id": db_pasajero.id,
                "nombre": db_pasajero.nombre,
                "apellido": db_pasajero.apellido,
                "numero_pasaporte": db_pasajero.numero_pasaporte,
                "email": db_pasajero.email
            }

            # Actualizar campos
            update_data = pasajero.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_pasajero, field, value)

            db.commit()
            db.refresh(db_pasajero)

            # Publicar evento de pasajero actualizado
            await publish_pasajero_event(
                EventTypes.PASAJERO_ACTUALIZADO,
                {
                    "id": db_pasajero.id,
                    "old_data": old_data,
                    "new_data": {
                        "nombre": db_pasajero.nombre,
                        "apellido": db_pasajero.apellido,
                        "numero_pasaporte": db_pasajero.numero_pasaporte,
                        "email": db_pasajero.email
                    }
                }
            )
            
            logger.info(f"Pasajero {pasajero_id} actualizado exitosamente")
            return db_pasajero
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error de base de datos al actualizar pasajero {pasajero_id}: {str(e)}")
            raise DatabaseException(str(e))

    @staticmethod
    async def delete_pasajero(db: Session, pasajero_id: int) -> bool:
        try:
            db_pasajero = PasajeroService.get_pasajero(db, pasajero_id)
            
            # Guardar datos para el evento
            pasajero_data = {
                "id": db_pasajero.id,
                "nombre": db_pasajero.nombre,
                "apellido": db_pasajero.apellido,
                "numero_pasaporte": db_pasajero.numero_pasaporte,
                "email": db_pasajero.email
            }
            
            db.delete(db_pasajero)
            db.commit()

            # Publicar evento de pasajero eliminado
            await publish_pasajero_event(
                EventTypes.PASAJERO_ELIMINADO,
                pasajero_data
            )
            
            logger.info(f"Pasajero {pasajero_id} eliminado exitosamente")
            return True
        except SQLAlchemyError as e:
            db.rollback()
            logger.error(f"Error de base de datos al eliminar pasajero {pasajero_id}: {str(e)}")
            raise DatabaseException(str(e)) 