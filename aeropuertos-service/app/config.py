from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuración de la base de datos
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1092"
    MYSQL_DATABASE: str = "airline_aeropuertos"
    
    # Configuración de la API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Servicio de Aeropuertos"
    
    # Configuración de seguridad
    SECRET_KEY: str = "tu_clave_secreta_aqui"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de otros servicios
    VUELOS_SERVICE_URL: str = "http://localhost:8003/api/v1"
    
    class Config:
        env_file = ".env"

settings = Settings() 