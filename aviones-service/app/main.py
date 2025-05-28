from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import aviones
from app.core.config import settings
from app.database import Base, engine
import logging
from contextlib import asynccontextmanager
import time
import sys

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    stream=sys.stdout
)
logger = logging.getLogger("aviones_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Iniciando {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Base de datos: mysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")
    
    # Esperar a que la base de datos esté lista
    max_retries = 5
    retry_count = 0
    while retry_count < max_retries:
        try:
            logger.info("Intentando crear tablas en la base de datos...")
            Base.metadata.create_all(bind=engine)
            logger.info("Tablas creadas correctamente en la base de datos")
            break
        except Exception as e:
            retry_count += 1
            logger.error(f"Error al crear tablas (intento {retry_count}/{max_retries}): {str(e)}")
            if retry_count < max_retries:
                logger.info(f"Esperando 5 segundos antes de reintentar...")
                time.sleep(5)
            else:
                logger.error("No se pudieron crear las tablas después de varios intentos")
                raise
    
    logger.info(f"Servicio {settings.PROJECT_NAME} iniciado correctamente")
    yield
    # Shutdown
    logger.info(f"Deteniendo {settings.PROJECT_NAME}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Incluir routers
app.include_router(aviones.router, prefix=f"{settings.API_V1_STR}/aviones", tags=["aviones"])

@app.get("/")
async def root():
    return {"message": "Bienvenido al Servicio de Aviones"}

@app.get("/health/live")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando aplicación con uvicorn...")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=int(settings.SERVICE_PORT),
        reload=settings.DEBUG
    ) 