from sqlalchemy.orm import Session
from ..models.pasajero import Pasajero
from ..models.usuario import Usuario
from ..schemas.pasajero import PasajeroCreate, PasajeroUpdate
from typing import List, Optional
from ..core.exceptions import (
    PasajeroNotFoundException,
    PasajeroDuplicadoException,
    DatabaseException,
    UsuarioNotFoundException
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
    def get_pasajero_by_documento(db: Session, numero_documento: str) -> Optional[Pasajero]:
        try:
            return db.query(Pasajero).filter(Pasajero.numero_documento == numero_documento).first()
        except SQLAlchemyError as e:
            logger.error(f"Error de base de datos al buscar pasajero con documento {numero_documento}: {str(e)}")
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
            # Verificar si el usuario existe
            usuario = db.query(Usuario).filter(Usuario.id == pasajero.usuario_id).first()
            if not usuario:
                logger.warning(f"Usuario no encontrado con ID: {pasajero.usuario_id}")
                raise UsuarioNotFoundException(pasajero.usuario_id)

            # Verificar si ya existe un pasajero con el mismo número de documento
            db_pasajero = PasajeroService.get_pasajero_by_documento(db, pasajero.numero_documento)
            if db_pasajero:
                logger.warning(f"Intento de crear pasajero con documento duplicado: {pasajero.numero_documento}")
                raise PasajeroDuplicadoException(pasajero.numero_documento)
            
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
                    "tipo_documento": db_pasajero.tipo_documento,
                    "numero_documento": db_pasajero.numero_documento,
                    "nacionalidad": db_pasajero.nacionalidad,
                    "usuario_id": db_pasajero.usuario_id
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

            # Verificar si el nuevo número de documento ya existe
            if pasajero.numero_documento and pasajero.numero_documento != db_pasajero.numero_documento:
                existing_pasajero = PasajeroService.get_pasajero_by_documento(db, pasajero.numero_documento)
                if existing_pasajero:
                    logger.warning(f"Intento de actualizar pasajero {pasajero_id} con documento duplicado: {pasajero.numero_documento}")
                    raise PasajeroDuplicadoException(pasajero.numero_documento)

            # Guardar datos antiguos para el evento
            old_data = {
                "id": db_pasajero.id,
                "tipo_documento": db_pasajero.tipo_documento,
                "numero_documento": db_pasajero.numero_documento,
                "nacionalidad": db_pasajero.nacionalidad,
                "usuario_id": db_pasajero.usuario_id
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
                        "tipo_documento": db_pasajero.tipo_documento,
                        "numero_documento": db_pasajero.numero_documento,
                        "nacionalidad": db_pasajero.nacionalidad,
                        "usuario_id": db_pasajero.usuario_id
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
                "tipo_documento": db_pasajero.tipo_documento,
                "numero_documento": db_pasajero.numero_documento,
                "nacionalidad": db_pasajero.nacionalidad,
                "usuario_id": db_pasajero.usuario_id
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