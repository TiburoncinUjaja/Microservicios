from pydantic_settings import BaseSettings
from typing import Optional, List
from dotenv import load_dotenv
import os
import secrets

# Cargar variables de entorno desde .env
load_dotenv()

class Settings(BaseSettings):
    # Configuración básica
    APP_NAME: str = "Pasajeros Service"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    
    # Configuración del servidor
    SERVICE_HOST: str = os.getenv("SERVICE_HOST", "0.0.0.0")
    SERVICE_PORT: int = int(os.getenv("SERVICE_PORT", "8001"))
    
    # Configuración de la base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql://root:root@mysql:3306/airline_pasajeros")
    
    # Configuración de Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    
    # Configuración de RabbitMQ
    RABBITMQ_URL: str = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq:5672/")
    
    # Configuración de otros servicios
    VUELOS_SERVICE_URL: str = os.getenv("VUELOS_SERVICE_URL", "http://vuelos-service:8003")
    RESERVAS_SERVICE_URL: str = os.getenv("RESERVAS_SERVICE_URL", "http://reservas-service:8002")
    
    # Configuración de seguridad
    SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_CREDENTIALS: bool = True
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]
    
    # Configuración de logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Configuración de RabbitMQ
    RABBITMQ_EXCHANGE: str = "aerolinea_events"
    RABBITMQ_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 