from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import vuelos, tripulacion as tripulacion_endpoints, auth
from app.core.config import settings
import logging
from pythonjsonlogger import jsonlogger
from app.database import Base, engine
from app.models import base, vuelo, tripulacion as tripulacion_models  # Importar todos los modelos
from contextlib import asynccontextmanager
from sqlalchemy import text

# Configuración del logger
logger = logging.getLogger()
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(settings.LOG_FORMAT)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)
logger.setLevel(settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Eliminar tablas existentes
        logger.info("Eliminando tablas existentes...")
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            conn.execute(text("DROP TABLE IF EXISTS vuelos"))
            conn.execute(text("DROP TABLE IF EXISTS tripulacion_vuelo"))
            conn.execute(text("DROP TABLE IF EXISTS personal"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()
        logger.info("Tablas eliminadas exitosamente")

        # Recrear tablas
        logger.info("Recreando tablas...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas recreadas exitosamente")
        yield
    except Exception as e:
        logger.error(f"Error al recrear la base de datos: {str(e)}")
        raise

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(vuelos.router, prefix=f"{settings.API_V1_STR}/vuelos", tags=["vuelos"])
app.include_router(tripulacion_endpoints.router, prefix=f"{settings.API_V1_STR}/tripulacion", tags=["tripulacion"])

@app.get("/")
async def root():
    return {"message": "Bienvenido al servicio de vuelos"}

if __name__ == "__main__":
    import uvicorn
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=settings.DEBUG
    ) 