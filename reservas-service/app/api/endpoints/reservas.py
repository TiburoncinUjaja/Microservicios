from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import httpx
import random
import string
from datetime import datetime

from app.core.database import get_db
from app.core.config import settings
from app.models.reserva import Reserva, EstadoReserva
from app.schemas.reserva import ReservaCreate, ReservaUpdate, Reserva as ReservaSchema
from app.core.vuelos_client import VuelosServiceClient
from app.core.auth import get_current_user

router = APIRouter(prefix="/reservas", tags=["reservas"])
vuelos_client = VuelosServiceClient()

# Cliente HTTP para comunicación con otros microservicios
async def get_http_client():
    async with httpx.AsyncClient() as client:
        yield client

# Función para generar código de reserva único
def generar_codigo_reserva():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# Validar existencia del pasajero
async def validar_pasajero(pasajero_id: int, client: httpx.AsyncClient):
    try:
        response = await client.get(f"{settings.PASAJEROS_SERVICE_URL}/api/v1/pasajeros/{pasajero_id}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pasajero no encontrado"
            )
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de pasajeros no disponible"
        )

# Validar disponibilidad del vuelo
async def validar_vuelo(vuelo_id: int, client: httpx.AsyncClient):
    try:
        response = await client.get(f"{settings.VUELOS_SERVICE_URL}/api/v1/vuelos/{vuelo_id}")
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vuelo no encontrado"
            )
        return response.json()
    except httpx.RequestError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de vuelos no disponible"
        )

@router.post("", response_model=ReservaSchema, status_code=status.HTTP_201_CREATED)
async def crear_reserva(
    reserva: ReservaCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Crea una nueva reserva con validaciones de vuelo.
    """
    # Verificar si el pasajero ya tiene una reserva para este vuelo
    reserva_existente = db.query(Reserva).filter(
        Reserva.pasajero_id == reserva.pasajero_id,
        Reserva.vuelo_id == reserva.vuelo_id
    ).first()
    
    if reserva_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El pasajero ya tiene una reserva para este vuelo"
        )

    # Verificar cupo en el vuelo
    hay_cupo = await vuelos_client.verificar_cupo(reserva.vuelo_id)
    if not hay_cupo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No hay cupos disponibles en este vuelo"
        )

    # Verificar si el vuelo aún no ha partido
    fecha_valida = await vuelos_client.verificar_fecha_vuelo(reserva.vuelo_id)
    if not fecha_valida:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden crear reservas para vuelos que ya partieron"
        )

    # Verificar si el asiento está disponible
    asiento_disponible = await vuelos_client.verificar_asiento_disponible(
        reserva.vuelo_id,
        reserva.numero_asiento
    )
    if not asiento_disponible:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El asiento seleccionado no está disponible"
        )

    # Crear la reserva
    nueva_reserva = Reserva(**reserva.dict())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    
    return nueva_reserva

@router.get("/{reserva_id}", response_model=ReservaSchema)
async def obtener_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene una reserva específica por su ID.
    """
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    return reserva

@router.get("", response_model=List[ReservaSchema])
async def listar_reservas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todas las reservas con paginación.
    """
    reservas = db.query(Reserva).offset(skip).limit(limit).all()
    return reservas

@router.put("/{reserva_id}", response_model=ReservaSchema)
async def actualizar_reserva(
    reserva_id: int,
    reserva_update: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Actualiza una reserva existente.
    """
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )

    # Si se está actualizando el asiento, verificar disponibilidad
    if reserva_update.numero_asiento and reserva_update.numero_asiento != reserva.numero_asiento:
        asiento_disponible = await vuelos_client.verificar_asiento_disponible(
            reserva.vuelo_id,
            reserva_update.numero_asiento
        )
        if not asiento_disponible:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo asiento seleccionado no está disponible"
            )

    # Actualizar la reserva
    for key, value in reserva_update.dict(exclude_unset=True).items():
        setattr(reserva, key, value)
    
    db.commit()
    db.refresh(reserva)
    return reserva

@router.delete("/{reserva_id}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Elimina una reserva existente.
    """
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reserva no encontrada"
        )
    
    db.delete(reserva)
    db.commit()
    return None

@router.get("/pasajero/{pasajero_id}", response_model=List[ReservaSchema])
async def listar_reservas_pasajero(
    pasajero_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todas las reservas de un pasajero específico.
    """
    reservas = db.query(Reserva).filter(Reserva.pasajero_id == pasajero_id).all()
    return reservas

@router.get("/vuelo/{vuelo_id}", response_model=List[ReservaSchema])
async def listar_reservas_vuelo(
    vuelo_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todas las reservas de un vuelo específico.
    """
    reservas = db.query(Reserva).filter(Reserva.vuelo_id == vuelo_id).all()
    return reservas 