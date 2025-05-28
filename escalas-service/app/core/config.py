from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la API
    APP_NAME: str = "Servicio de Escalas"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api/v1"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Servicio de Escalas"
    DEBUG: bool = True
    
    # Configuración del servicio
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8082
    
    # Configuración de la base de datos
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3307
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1092"
    MYSQL_DATABASE: str = "airline_escalas"

    # Configuración de Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    # Configuración de RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"

    # URLs de otros servicios
    VUELOS_SERVICE_URL: str = "http://vuelos-service:8003/api/v1"
    AEROPUERTOS_SERVICE_URL: str = "http://aeropuertos-service:8005/api/v1"

    # Configuración de seguridad
    SECRET_KEY: str = "tu_clave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings() 