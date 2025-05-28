from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Vuelos Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Database
    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3307
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "1092"
    MYSQL_DATABASE: str = "airline_vuelos"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    # Redis
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    
    # RabbitMQ
    RABBITMQ_HOST: str = "rabbitmq"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"  # En producción, usar una clave segura
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Service
    SERVICE_PORT: int = 8003
    SERVICE_HOST: str = "0.0.0.0"
    DEBUG: bool = True
    
    # URLs de otros servicios
    AEROPUERTOS_SERVICE_URL: str = "http://aeropuertos-service:8005/api/v1"
    AVIONES_SERVICE_URL: str = "http://aviones-service:8004/api/v1"
    ESCALAS_SERVICE_URL: str = "http://escalas-service:8006/api/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"

settings = Settings() 