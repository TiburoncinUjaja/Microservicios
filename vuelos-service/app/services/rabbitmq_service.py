import aio_pika
import json
import logging
from typing import Dict, Any
from app.core.config import settings

logger = logging.getLogger(__name__)

class RabbitMQService:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange = None

    async def connect(self):
        """Establece la conexión con RabbitMQ."""
        if not self.connection:
            self.connection = await aio_pika.connect_robust(
                f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/"
            )
            self.channel = await self.connection.channel()
            self.exchange = await self.channel.declare_exchange(
                "airline_events",
                aio_pika.ExchangeType.TOPIC
            )

    async def publish_event(self, event_type: str, data: Dict[str, Any]):
        """Publica un evento en RabbitMQ."""
        try:
            if not self.connection:
                await self.connect()

            message = aio_pika.Message(
                body=json.dumps(data).encode(),
                content_type="application/json"
            )

            await self.exchange.publish(
                message,
                routing_key=f"vuelos.{event_type}"
            )
            logger.info(f"Evento publicado: vuelos.{event_type}")
        except Exception as e:
            logger.error(f"Error publicando evento: {str(e)}")
            raise

    async def close(self):
        """Cierra la conexión con RabbitMQ."""
        if self.connection:
            await self.connection.close()

rabbitmq_service = RabbitMQService() 