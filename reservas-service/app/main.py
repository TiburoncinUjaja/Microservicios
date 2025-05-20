from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import reservas
from .core.config import settings
from .core.database import Base, engine
import logging
import time
import sys

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    stream=sys.stdout
)
logger = logging.getLogger("reservas_service")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Modo debug: {settings.DEBUG}")
    logger.info(f"Base de datos: {settings.DATABASE_URL}")
    
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
    
    logger.info(f"Servicio {settings.APP_NAME} iniciado correctamente")
    yield
    # Shutdown
    logger.info(f"Deteniendo {settings.APP_NAME}")

# Crear la aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
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
app.include_router(reservas.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Bienvenido al Servicio de Reservas"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando aplicación con uvicorn...")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=int(settings.SERVICE_PORT),
        reload=settings.DEBUG
    ) 