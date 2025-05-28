import logging
import sys
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import traceback

from app.api.v1.endpoints import reservas
from app.core.config import settings
from app.database import Base, engine, init_db

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicializar la base de datos al iniciar la aplicación
    try:
        logger.info("Iniciando la aplicación...")
        init_db()
        logger.info("Base de datos inicializada correctamente")
        yield
    except Exception as e:
        logger.error(f"Error al inicializar la aplicación: {str(e)}")
        logger.error(traceback.format_exc())
        raise

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware para logging de requests y responses
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Error en la request: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )

# Incluir routers
app.include_router(
    reservas.router,
    prefix=f"{settings.API_V1_STR}/reservas",
    tags=["reservas"]
)

@app.get("/health")
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