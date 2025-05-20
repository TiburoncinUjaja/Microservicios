import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.endpoints import pasajeros, health, auth
from .core.config import settings
from .core.database import Base, engine
from .core.messaging import MessageBroker
from .core.events import setup_event_handlers
import logging

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT
)
logger = logging.getLogger("pasajeros_service")

# Crear la aplicación FastAPI
app = FastAPI(
    title="Servicio de Pasajeros",
    description="API para la gestión de pasajeros",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_CREDENTIALS,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Configurar el broker de mensajes
message_broker = MessageBroker()

@app.on_event("startup")
async def startup_event():
    logger.info(f"Iniciando {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Modo debug: {settings.DEBUG}")
    logger.info(f"Base de datos: {settings.DATABASE_URL}")
    Base.metadata.create_all(bind=engine)
    
    # Configurar el event loop
    loop = asyncio.get_event_loop()
    
    # Inicializar el broker de mensajes
    await message_broker.connect()
    
    # Configurar los manejadores de eventos
    await setup_event_handlers(message_broker)

@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Deteniendo {settings.APP_NAME}")
    await message_broker.disconnect()

# Incluir routers
app.include_router(auth.router, prefix="/api/v1", tags=["Autenticación"])
app.include_router(pasajeros.router, prefix="/api/v1/pasajeros", tags=["Pasajeros"])
app.include_router(health.router, prefix="/api/v1/health", tags=["Salud"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=settings.SERVICE_PORT,
        reload=True
    ) 