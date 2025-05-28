import httpx
import logging
from typing import Optional, Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class ExternalServiceError(Exception):
    pass

class ExternalService:
    def __init__(self):
        self.aeropuertos_url = settings.AEROPUERTOS_SERVICE_URL
        self.aviones_url = settings.AVIONES_SERVICE_URL
        self.personal_url = "http://personal-service:8006/api/v1"
        self.escalas_url = settings.ESCALAS_SERVICE_URL

    async def verify_aeropuerto(self, aeropuerto_id: int) -> bool:
        """Verifica si un aeropuerto existe en el servicio de aeropuertos."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.aeropuertos_url}/aeropuertos/{aeropuerto_id}")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error verificando aeropuerto {aeropuerto_id}: {str(e)}")
            raise ExternalServiceError(f"Error verificando aeropuerto: {str(e)}")

    async def verify_avion(self, avion_id: int) -> bool:
        """Verifica si un avión existe en el servicio de aviones."""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.aviones_url}/aviones/{avion_id}")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error verificando avión {avion_id}: {str(e)}")
            raise ExternalServiceError(f"Error verificando avión: {str(e)}")

    async def verify_personal(self, personal_id: int) -> bool:
        """Verifica si un miembro del personal existe en el servicio de personal."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.personal_url}/personal/{personal_id}")
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Error verificando personal {personal_id}: {str(e)}")
            raise ExternalServiceError(f"Error verificando personal: {str(e)}")

    async def create_escala(self, escala_data: Dict[str, Any]) -> Dict[str, Any]:
        """Crea una escala en el servicio de escalas."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{self.escalas_url}/escalas/", json=escala_data)
                if response.status_code != 201:
                    raise ExternalServiceError(f"Error creando escala: {response.text}")
                return response.json()
        except Exception as e:
            logger.error(f"Error creando escala: {str(e)}")
            raise ExternalServiceError(f"Error creando escala: {str(e)}")

external_service = ExternalService() 