from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Configuración general
    APP_NAME: str = os.getenv("APP_NAME", "Reservas Service")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://root:root@mysql:3306/airline_reservas")

    # Configuración de Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")

    # Configuración de RabbitMQ
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")

    # Configuración de servicios
    PASAJEROS_SERVICE_URL: str = os.getenv("PASAJEROS_SERVICE_URL", "http://pasajeros-service:8001")
    VUELOS_SERVICE_URL: str = os.getenv("VUELOS_SERVICE_URL", "http://vuelos-service:8003")

    # Configuración del servidor
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8002"))
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "0.0.0.0")

    # Configuración de CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    class Config:
        case_sensitive = True

settings = Settings() 