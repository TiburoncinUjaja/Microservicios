from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from datetime import datetime
import requests
import logging
from app.models.escala import Escala
from app.schemas.escala import EscalaCreate, EscalaUpdate
from app.core.config import settings

logger = logging.getLogger(__name__)

class EscalaService:
    def __init__(self, db: Session):
        self.db = db
        logger.info(f"Configuración del servicio de escalas:")
        logger.info(f"VUELOS_SERVICE_URL: {settings.VUELOS_SERVICE_URL}")
        logger.info(f"AEROPUERTOS_SERVICE_URL: {settings.AEROPUERTOS_SERVICE_URL}")

    def create_escala(self, escala: EscalaCreate) -> Escala:
        try:
            logger.info(f"Intentando crear escala para vuelo {escala.vuelo_id}")
            logger.info(f"Datos recibidos: {escala.model_dump()}")
            
            # Verificar que el vuelo existe
            vuelos_url = f"{settings.VUELOS_SERVICE_URL}/vuelos/{escala.vuelo_id}"
            logger.info(f"Verificando vuelo en URL: {vuelos_url}")
            logger.info("Realizando petición GET al servicio de vuelos...")
            
            try:
                # Intentar primero con la URL completa
                logger.info("Intento 1: URL completa")
                vuelo_response = requests.get(
                    vuelos_url,
                    timeout=5
                )
                logger.info(f"Respuesta del servicio de vuelos - Status Code: {vuelo_response.status_code}")
                logger.info(f"Respuesta del servicio de vuelos - Headers: {vuelo_response.headers}")
                logger.info(f"Respuesta del servicio de vuelos - Content: {vuelo_response.text}")
                
                if vuelo_response.status_code != 200:
                    # Intentar con la URL alternativa
                    logger.info("Intento 2: URL alternativa")
                    alt_url = f"http://vuelos-service:8003/api/v1/vuelos/{escala.vuelo_id}"
                    logger.info(f"Probando URL alternativa: {alt_url}")
                    vuelo_response = requests.get(
                        alt_url,
                        timeout=5
                    )
                    logger.info(f"Respuesta alternativa - Status Code: {vuelo_response.status_code}")
                    logger.info(f"Respuesta alternativa - Headers: {vuelo_response.headers}")
                    logger.info(f"Respuesta alternativa - Content: {vuelo_response.text}")
                
                if vuelo_response.status_code != 200:
                    logger.error(f"Error al verificar vuelo: {vuelo_response.status_code} - {vuelo_response.text}")
                    raise ValueError(f"El vuelo {escala.vuelo_id} no existe")
                
                vuelo_data = vuelo_response.json()
                logger.info(f"Datos del vuelo obtenidos: {vuelo_data}")
            except requests.RequestException as e:
                logger.error(f"Error al conectar con el servicio de vuelos: {str(e)}")
                logger.error(f"URL que falló: {vuelos_url}")
                raise ValueError("No se pudo verificar el vuelo. Servicio no disponible")

            # Verificar que el aeropuerto existe
            aeropuerto_url = f"{settings.AEROPUERTOS_SERVICE_URL}/api/v1/aeropuertos/{escala.aeropuerto_id}"
            logger.info(f"Verificando aeropuerto en URL: {aeropuerto_url}")
            
            try:
                aeropuerto_response = requests.get(
                    aeropuerto_url,
                    timeout=5
                )
                logger.info(f"Respuesta del servicio de aeropuertos: {aeropuerto_response.status_code} - {aeropuerto_response.text}")
                
                if aeropuerto_response.status_code != 200:
                    logger.error(f"Error al verificar aeropuerto: {aeropuerto_response.status_code} - {aeropuerto_response.text}")
                    raise ValueError(f"El aeropuerto {escala.aeropuerto_id} no existe")
            except requests.RequestException as e:
                logger.error(f"Error al conectar con el servicio de aeropuertos: {str(e)}")
                raise ValueError("No se pudo verificar el aeropuerto. Servicio no disponible")

            logger.info("Validaciones exitosas, creando escala en la base de datos")
            
            # Crear diccionario con los datos de la escala
            escala_data = escala.model_dump()
            logger.info(f"Datos a insertar en la base de datos: {escala_data}")
            
            # Crear la instancia de Escala
            db_escala = Escala(**escala_data)
            logger.info(f"Instancia de Escala creada: {db_escala.__dict__}")
            
            self.db.add(db_escala)
            self.db.commit()
            self.db.refresh(db_escala)
            logger.info(f"Escala creada exitosamente con ID: {db_escala.id}")
            return db_escala
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Error de base de datos al crear escala: {str(e)}")
            raise ValueError(f"Error al crear la escala en la base de datos: {str(e)}")
        except Exception as e:
            logger.error(f"Error inesperado al crear escala: {str(e)}")
            raise

    def get_escala(self, escala_id: int) -> Optional[Escala]:
        return self.db.query(Escala).filter(Escala.id == escala_id).first()

    def get_escalas_by_vuelo(self, vuelo_id: int) -> List[Escala]:
        return self.db.query(Escala).filter(Escala.vuelo_id == vuelo_id).all()

    def update_escala(self, escala_id: int, escala: EscalaUpdate) -> Optional[Escala]:
        try:
            db_escala = self.get_escala(escala_id)
            if not db_escala:
                return None

            update_data = escala.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_escala, key, value)

            self.db.commit()
            self.db.refresh(db_escala)
            return db_escala
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def delete_escala(self, escala_id: int) -> bool:
        try:
            db_escala = self.get_escala(escala_id)
            if not db_escala:
                return False

            self.db.delete(db_escala)
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def update_estado_escala(self, escala_id: int, nuevo_estado: str) -> Optional[Escala]:
        try:
            db_escala = self.get_escala(escala_id)
            if not db_escala:
                return None

            db_escala.estado = nuevo_estado
            self.db.commit()
            self.db.refresh(db_escala)
            return db_escala
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e 