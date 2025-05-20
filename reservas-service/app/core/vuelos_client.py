from typing import Optional, Dict, Any
import httpx
from fastapi import HTTPException
from ..core.config import settings

class VuelosServiceClient:
    def __init__(self):
        self.base_url = settings.VUELOS_SERVICE_URL
        self.client = httpx.AsyncClient(timeout=30.0)

    async def verificar_cupo(self, vuelo_id: str) -> bool:
        """
        Simula la verificación de cupos disponibles en un vuelo.
        Por ahora, siempre retorna True para permitir la creación de reservas.
        """
        return True

    async def verificar_fecha_vuelo(self, vuelo_id: str) -> bool:
        """
        Simula la verificación de fecha del vuelo.
        Por ahora, siempre retorna True para permitir la creación de reservas.
        """
        return True

    async def verificar_asiento_disponible(self, vuelo_id: str, numero_asiento: str) -> bool:
        """
        Simula la verificación de disponibilidad de asientos.
        Por ahora, siempre retorna True para permitir la creación de reservas.
        """
        return True

    async def obtener_info_vuelo(self, vuelo_id: str) -> Dict[str, Any]:
        """
        Simula la obtención de información del vuelo.
        Retorna datos de ejemplo para permitir la creación de reservas.
        """
        return {
            "id": vuelo_id,
            "origen": "Ciudad de Origen",
            "destino": "Ciudad de Destino",
            "fecha": "2025-05-20T10:00:00",
            "estado": "PROGRAMADO"
        }

    async def close(self):
        """Cierra el cliente HTTP."""
        await self.client.aclose() 