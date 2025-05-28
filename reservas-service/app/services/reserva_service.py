from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.reserva import Reserva, EstadoReserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate
import httpx
from app.core.config import settings

class ReservaService:
    def __init__(self, db: Session):
        self.db = db

    async def verificar_pasajero(self, pasajero_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.PASAJEROS_SERVICE_URL}/api/v1/pasajeros/{pasajero_id}")
                return response.status_code == 200
            except Exception:
                return False

    async def verificar_vuelo(self, vuelo_id: int) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{settings.VUELOS_SERVICE_URL}/api/v1/vuelos/{vuelo_id}")
                return response.status_code == 200
            except Exception:
                return False

    async def verificar_asiento_disponible(self, vuelo_id: int, asiento: str) -> bool:
        # Verificar si el asiento ya está reservado
        reserva_existente = self.db.query(Reserva).filter(
            Reserva.vuelo_id == vuelo_id,
            Reserva.asiento == asiento,
            Reserva.estado != EstadoReserva.CANCELADA
        ).first()
        
        return reserva_existente is None

    async def crear_reserva(self, reserva: ReservaCreate) -> Reserva:
        # Verificar que el pasajero existe
        if not await self.verificar_pasajero(reserva.pasajero_id):
            raise HTTPException(status_code=404, detail="Pasajero no encontrado")

        # Verificar que el vuelo existe
        if not await self.verificar_vuelo(reserva.vuelo_id):
            raise HTTPException(status_code=404, detail="Vuelo no encontrado")

        # Verificar disponibilidad del asiento
        if not await self.verificar_asiento_disponible(reserva.vuelo_id, reserva.asiento):
            raise HTTPException(status_code=400, detail="Asiento no disponible")

        # Crear la reserva
        db_reserva = Reserva(**reserva.model_dump())
        self.db.add(db_reserva)
        self.db.commit()
        self.db.refresh(db_reserva)
        return db_reserva

    def obtener_reserva(self, reserva_id: int) -> Reserva:
        reserva = self.db.query(Reserva).filter(Reserva.id == reserva_id).first()
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva

    def actualizar_reserva(self, reserva_id: int, reserva: ReservaUpdate) -> Reserva:
        db_reserva = self.obtener_reserva(reserva_id)
        
        # Si se está actualizando el asiento, verificar disponibilidad
        if reserva.asiento and reserva.asiento != db_reserva.asiento:
            if not self.verificar_asiento_disponible(db_reserva.vuelo_id, reserva.asiento):
                raise HTTPException(status_code=400, detail="Asiento no disponible")

        # Actualizar campos
        for field, value in reserva.model_dump(exclude_unset=True).items():
            setattr(db_reserva, field, value)

        self.db.commit()
        self.db.refresh(db_reserva)
        return db_reserva

    def eliminar_reserva(self, reserva_id: int) -> None:
        reserva = self.obtener_reserva(reserva_id)
        self.db.delete(reserva)
        self.db.commit() 