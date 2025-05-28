from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings(BaseSettings):
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Reservas Service"
    VERSION: str = "1.0.0"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8002

    # Configuración de la base de datos
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3307
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1092"
    MYSQL_DATABASE: str = "airline_reservas"
    
    DATABASE_URL: str = "mysql+pymysql://root:1092@localhost:3307/airline_reservas"

    # Configuración de CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Configuración de seguridad
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Configuración de Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://redis:6379/0"

    # Configuración de RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"

    # URLs de otros servicios
    PASAJEROS_SERVICE_URL: str = "http://pasajeros-service:8001"
    VUELOS_SERVICE_URL: str = "http://vuelos-service:8003"
    AVIONES_SERVICE_URL: str = "http://aviones-service:8004"
    AEROPUERTOS_SERVICE_URL: str = "http://aeropuertos-service:8005"
    ESCALAS_SERVICE_URL: str = "http://escalas-service:8006"

    # Configuración de logging
    LOG_LEVEL: str = "DEBUG"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Configuración de debug
    DEBUG: bool = True

    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Permitir variables de entorno adicionales

settings = Settings() 