from sqlalchemy.orm import Session
from app.models.vuelo import Vuelo
from app.schemas.vuelo import VueloCreate, VueloUpdate
from app.services.external_service import external_service, ExternalServiceError
from app.services.rabbitmq_service import rabbitmq_service
import logging
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

class VueloService:
    def __init__(self, db: Session):
        self.db = db

    async def create_vuelo(self, vuelo: VueloCreate) -> Vuelo:
        """Crea un nuevo vuelo verificando las referencias externas."""
        try:
            # Verificar aeropuertos
            if not await external_service.verify_aeropuerto(vuelo.aeropuerto_origen_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Aeropuerto origen {vuelo.aeropuerto_origen_id} no encontrado"
                )
            
            if not await external_service.verify_aeropuerto(vuelo.aeropuerto_destino_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Aeropuerto destino {vuelo.aeropuerto_destino_id} no encontrado"
                )

            # Verificar avión
            if not await external_service.verify_avion(vuelo.avion_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Avion {vuelo.avion_id} no encontrado"
                )

            # Crear el vuelo
            db_vuelo = Vuelo(**vuelo.dict())
            self.db.add(db_vuelo)
            self.db.commit()
            self.db.refresh(db_vuelo)

            # Publicar evento
            await rabbitmq_service.publish_event(
                "created",
                {
                    "id": db_vuelo.id,
                    "numero_vuelo": db_vuelo.numero_vuelo,
                    "estado": db_vuelo.estado
                }
            )

            return db_vuelo

        except ExternalServiceError as e:
            self.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(e)
            )
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creando vuelo: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )

    def get_vuelo(self, vuelo_id: int) -> Vuelo:
        """Obtiene un vuelo por su ID."""
        logger.info(f"Intentando obtener vuelo con ID: {vuelo_id}")
        vuelo = self.db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
        if not vuelo:
            logger.error(f"Vuelo con ID {vuelo_id} no encontrado en la base de datos")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vuelo no encontrado"
            )
        logger.info(f"Vuelo encontrado: {vuelo.__dict__}")
        return vuelo

    def get_vuelos(self, skip: int = 0, limit: int = 100) -> list[Vuelo]:
        """Obtiene una lista de vuelos."""
        return self.db.query(Vuelo).offset(skip).limit(limit).all()

    async def update_vuelo(self, vuelo_id: int, vuelo: VueloUpdate) -> Vuelo:
        """Actualiza un vuelo existente."""
        db_vuelo = self.get_vuelo(vuelo_id)

        # Verificar aeropuertos si se están actualizando
        if vuelo.aeropuerto_origen_id:
            if not await external_service.verify_aeropuerto(vuelo.aeropuerto_origen_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Aeropuerto origen {vuelo.aeropuerto_origen_id} no encontrado"
                )

        if vuelo.aeropuerto_destino_id:
            if not await external_service.verify_aeropuerto(vuelo.aeropuerto_destino_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Aeropuerto destino {vuelo.aeropuerto_destino_id} no encontrado"
                )

        # Verificar avión si se está actualizando
        if vuelo.avion_id:
            if not await external_service.verify_avion(vuelo.avion_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Avion {vuelo.avion_id} no encontrado"
                )

        # Actualizar el vuelo
        update_data = vuelo.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_vuelo, field, value)

        self.db.commit()
        self.db.refresh(db_vuelo)

        # Publicar evento
        await rabbitmq_service.publish_event(
            "updated",
            {
                "id": db_vuelo.id,
                "numero_vuelo": db_vuelo.numero_vuelo,
                "estado": db_vuelo.estado
            }
        )

        return db_vuelo

    async def delete_vuelo(self, vuelo_id: int) -> None:
        """Elimina un vuelo."""
        db_vuelo = self.get_vuelo(vuelo_id)
        self.db.delete(db_vuelo)
        self.db.commit()

        # Publicar evento
        await rabbitmq_service.publish_event(
            "deleted",
            {
                "id": vuelo_id,
                "numero_vuelo": db_vuelo.numero_vuelo
            }
        ) 