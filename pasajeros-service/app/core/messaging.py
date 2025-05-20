import aio_pika
import json
from typing import Any, Callable, Dict, Optional
from .config import settings
from .logger import logger
from functools import wraps
import asyncio
from datetime import datetime

class MessageBroker:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None
        self._consumers = {}
        self._retry_delays = [1, 5, 15, 30, 60]  # Retry delays in seconds

    async def connect(self):
        """Establece conexión con RabbitMQ."""
        try:
            self.connection = await aio_pika.connect_robust(
                settings.RABBITMQ_URL,
                timeout=settings.RABBITMQ_TIMEOUT
            )
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                settings.RABBITMQ_EXCHANGE,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            logger.info("Conexión establecida con RabbitMQ")
        except Exception as e:
            logger.error(f"Error al conectar con RabbitMQ: {str(e)}")
            raise

    async def close(self):
        """Cierra la conexión con RabbitMQ."""
        if self.connection:
            await self.connection.close()
            logger.info("Conexión cerrada con RabbitMQ")

    async def publish(self, routing_key: str, message: Dict[str, Any], retry: bool = True):
        """
        Publica un mensaje en RabbitMQ.
        
        Args:
            routing_key: La clave de enrutamiento del mensaje
            message: El mensaje a publicar
            retry: Si se debe reintentar en caso de error
        """
        if not self.connection or self.connection.is_closed:
            await self.connect()

        message_body = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": message
        }

        try:
            await self.exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message_body).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type="application/json"
                ),
                routing_key=routing_key
            )
            logger.info(f"Mensaje publicado en {routing_key}: {message}")
        except Exception as e:
            logger.error(f"Error al publicar mensaje en {routing_key}: {str(e)}")
            if retry:
                await self._retry_publish(routing_key, message)
            else:
                raise

    async def _retry_publish(self, routing_key: str, message: Dict[str, Any]):
        """Reintenta publicar un mensaje con backoff exponencial."""
        for delay in self._retry_delays:
            try:
                await asyncio.sleep(delay)
                await self.publish(routing_key, message, retry=False)
                logger.info(f"Reintento exitoso para {routing_key} después de {delay}s")
                return
            except Exception as e:
                logger.error(f"Error en reintento después de {delay}s: {str(e)}")
        logger.error(f"Todos los reintentos fallaron para {routing_key}")

    async def subscribe(self, queue_name: str, routing_key: str, callback: Callable):
        """
        Suscribe una función callback a una cola específica.
        
        Args:
            queue_name: Nombre de la cola
            routing_key: Clave de enrutamiento a escuchar
            callback: Función a ejecutar cuando llegue un mensaje
        """
        if not self.connection or self.connection.is_closed:
            await self.connect()

        try:
            # Declarar cola
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True
            )

            # Vincular cola al exchange
            await queue.bind(
                self.exchange,
                routing_key=routing_key
            )

            # Función wrapper para el callback
            async def process_message(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        body = json.loads(message.body.decode())
                        await callback(body["data"])
                        logger.info(f"Mensaje procesado de {routing_key}")
                    except Exception as e:
                        logger.error(f"Error procesando mensaje de {routing_key}: {str(e)}")
                        # En caso de error, rechazamos el mensaje para que vuelva a la cola
                        await message.nack(requeue=True)

            # Iniciar consumo
            await queue.consume(process_message)
            self._consumers[queue_name] = queue
            logger.info(f"Suscrito a {queue_name} con routing key {routing_key}")

        except Exception as e:
            logger.error(f"Error al suscribirse a {queue_name}: {str(e)}")
            raise

    async def unsubscribe(self, queue_name: str):
        """Cancela la suscripción a una cola."""
        if queue_name in self._consumers:
            await self._consumers[queue_name].cancel()
            del self._consumers[queue_name]
            logger.info(f"Desuscrito de {queue_name}")

# Instancia global del broker
message_broker = MessageBroker()

# Decorador para manejar eventos
def event_handler(routing_key: str):
    """
    Decorador para registrar manejadores de eventos.
    
    Uso:
    @event_handler("pasajero.creado")
    async def handle_pasajero_creado(data: Dict[str, Any]):
        # Procesar evento
        pass
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await func(*args, **kwargs)
        
        # Registrar el manejador
        queue_name = f"pasajeros-service.{routing_key}"
        asyncio.create_task(
            message_broker.subscribe(queue_name, routing_key, wrapper)
        )
        return wrapper
    return decorator 