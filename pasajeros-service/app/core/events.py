from typing import Dict, Any, Optional
from datetime import datetime
from .messaging import message_broker, event_handler
from .logger import logger

# Definición de eventos
class EventTypes:
    # Eventos de pasajeros
    PASAJERO_CREADO = "pasajero.creado"
    PASAJERO_ACTUALIZADO = "pasajero.actualizado"
    PASAJERO_ELIMINADO = "pasajero.eliminado"
    
    # Eventos de reservas
    RESERVA_CREADA = "reserva.creada"
    RESERVA_CANCELADA = "reserva.cancelada"
    RESERVA_CONFIRMADA = "reserva.confirmada"
    
    # Eventos de vuelos
    VUELO_CREADO = "vuelo.creado"
    VUELO_CANCELADO = "vuelo.cancelado"
    VUELO_ACTUALIZADO = "vuelo.actualizado"

# Funciones para publicar eventos
async def publish_pasajero_event(event_type: str, pasajero_data: Dict[str, Any]):
    """
    Publica un evento relacionado con pasajeros.
    
    Args:
        event_type: Tipo de evento (de EventTypes)
        pasajero_data: Datos del pasajero
    """
    try:
        await message_broker.publish(
            routing_key=event_type,
            message={
                "event_type": event_type,
                "timestamp": datetime.utcnow().isoformat(),
                "pasajero": pasajero_data
            }
        )
    except Exception as e:
        logger.error(f"Error publicando evento {event_type}: {str(e)}")
        raise

# Manejadores de eventos
async def handle_reserva_creada(data: Dict[str, Any]):
    """
    Maneja el evento de reserva creada.
    Actualiza el estado del pasajero si es necesario.
    """
    try:
        logger.info(f"Procesando reserva creada: {data}")
        # Aquí iría la lógica para actualizar el estado del pasajero
        # Por ejemplo, marcar al pasajero como "con reserva activa"
    except Exception as e:
        logger.error(f"Error procesando reserva creada: {str(e)}")
        raise

async def handle_reserva_cancelada(data: Dict[str, Any]):
    """
    Maneja el evento de reserva cancelada.
    Actualiza el estado del pasajero si es necesario.
    """
    try:
        logger.info(f"Procesando reserva cancelada: {data}")
        # Aquí iría la lógica para actualizar el estado del pasajero
        # Por ejemplo, marcar al pasajero como "sin reserva activa"
    except Exception as e:
        logger.error(f"Error procesando reserva cancelada: {str(e)}")
        raise

async def handle_vuelo_cancelado(data: Dict[str, Any]):
    """
    Maneja el evento de vuelo cancelado.
    Notifica a los pasajeros afectados.
    """
    try:
        logger.info(f"Procesando vuelo cancelado: {data}")
        # Aquí iría la lógica para notificar a los pasajeros
        # Por ejemplo, enviar una notificación a todos los pasajeros del vuelo
    except Exception as e:
        logger.error(f"Error procesando vuelo cancelado: {str(e)}")
        raise

# Función para inicializar los manejadores de eventos
async def setup_event_handlers(broker):
    """
    Inicializa todos los manejadores de eventos.
    Esta función debe ser llamada al iniciar la aplicación.
    """
    try:
        # Registrar los manejadores de eventos
        await broker.subscribe("pasajeros-service.reserva-creada", EventTypes.RESERVA_CREADA, handle_reserva_creada)
        await broker.subscribe("pasajeros-service.reserva-cancelada", EventTypes.RESERVA_CANCELADA, handle_reserva_cancelada)
        await broker.subscribe("pasajeros-service.vuelo-cancelado", EventTypes.VUELO_CANCELADO, handle_vuelo_cancelado)
        
        logger.info("Manejadores de eventos inicializados")
    except Exception as e:
        logger.error(f"Error inicializando manejadores de eventos: {str(e)}")
        raise 