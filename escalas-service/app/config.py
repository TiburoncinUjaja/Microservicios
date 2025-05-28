from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la base de datos
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3307
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1092"
    MYSQL_DATABASE: str = "airline_escalas"
    
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    API_PREFIX: str = "/api/v1"  # Agregado para compatibilidad
    PROJECT_NAME: str = "Servicio de Escalas"
    VERSION: str = "1.0.0"
    
    # Configuración del servicio
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = 8006
    DEBUG: bool = True
    
    # Configuración de seguridad
    SECRET_KEY: str = "tu_clave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de otros servicios
    VUELOS_SERVICE_URL: str = "http://vuelos-service:8002/api/v1"
    AEROPUERTOS_SERVICE_URL: str = "http://aeropuertos-service:8005/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings() 