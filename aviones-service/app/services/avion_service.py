from sqlalchemy.orm import Session
from app.models.avion import Avion
from app.schemas.avion import AvionCreate, AvionUpdate
from app.services.rabbitmq_service import rabbitmq_service
import logging
from fastapi import HTTPException, status
from datetime import datetime

logger = logging.getLogger(__name__)

class AvionService:
    def __init__(self, db: Session):
        self.db = db

    async def create_avion(self, avion: AvionCreate) -> Avion:
        """Crea un nuevo avión."""
        try:
            # Verificar si ya existe un avión con la misma matrícula
            if self.db.query(Avion).filter(Avion.matricula == avion.matricula).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un avión con esta matrícula"
                )

            # Crear el avión
            db_avion = Avion(**avion.dict())
            self.db.add(db_avion)
            self.db.commit()
            self.db.refresh(db_avion)

            # Publicar evento
            await rabbitmq_service.publish_event(
                "created",
                {
                    "id": db_avion.id,
                    "matricula": db_avion.matricula,
                    "estado": db_avion.estado
                }
            )

            return db_avion

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando avión: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    def get_avion(self, avion_id: int) -> Avion:
        """Obtiene un avión por su ID."""
        avion = self.db.query(Avion).filter(Avion.id == avion_id).first()
        if not avion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avión no encontrado"
            )
        return avion

    def get_avion_by_matricula(self, matricula: str) -> Avion:
        """Obtiene un avión por su matrícula."""
        avion = self.db.query(Avion).filter(Avion.matricula == matricula).first()
        if not avion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Avión no encontrado"
            )
        return avion

    def get_aviones(self, skip: int = 0, limit: int = 100) -> list[Avion]:
        """Obtiene una lista de aviones."""
        return self.db.query(Avion).offset(skip).limit(limit).all()

    def get_aviones_by_estado(self, estado: str) -> list[Avion]:
        """Obtiene una lista de aviones por estado."""
        return self.db.query(Avion).filter(Avion.estado == estado).all()

    async def update_avion(self, avion_id: int, avion: AvionUpdate) -> Avion:
        """Actualiza un avión existente."""
        db_avion = self.get_avion(avion_id)

        # Verificar matrícula única si se está actualizando
        if avion.matricula and avion.matricula != db_avion.matricula:
            if self.db.query(Avion).filter(Avion.matricula == avion.matricula).first():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe un avión con esta matrícula"
                )

        # Actualizar el avión
        update_data = avion.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_avion, field, value)

        self.db.commit()
        self.db.refresh(db_avion)

        # Publicar evento
        await rabbitmq_service.publish_event(
            "updated",
            {
                "id": db_avion.id,
                "matricula": db_avion.matricula,
                "estado": db_avion.estado
            }
        )

        return db_avion

    async def delete_avion(self, avion_id: int) -> None:
        """Elimina un avión."""
        db_avion = self.get_avion(avion_id)
        self.db.delete(db_avion)
        self.db.commit()

        # Publicar evento
        await rabbitmq_service.publish_event(
            "deleted",
            {
                "id": avion_id,
                "matricula": db_avion.matricula
            }
        )

    async def actualizar_estado_mantenimiento(self, avion_id: int, estado: str) -> Avion:
        """Actualiza el estado de mantenimiento de un avión."""
        if estado not in ["ACTIVO", "MANTENIMIENTO", "INACTIVO"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Estado no válido"
            )

        db_avion = self.get_avion(avion_id)
        db_avion.estado = estado
        
        if estado == "MANTENIMIENTO":
            db_avion.ultima_revision = datetime.utcnow()
            # Establecer próxima revisión en 6 meses
            db_avion.proxima_revision = datetime.utcnow().replace(month=datetime.utcnow().month + 6)

        self.db.commit()
        self.db.refresh(db_avion)

        # Publicar evento
        await rabbitmq_service.publish_event(
            "maintenance_updated",
            {
                "id": db_avion.id,
                "matricula": db_avion.matricula,
                "estado": db_avion.estado,
                "ultima_revision": db_avion.ultima_revision.isoformat() if db_avion.ultima_revision else None,
                "proxima_revision": db_avion.proxima_revision.isoformat() if db_avion.proxima_revision else None
            }
        )

        return db_avion 