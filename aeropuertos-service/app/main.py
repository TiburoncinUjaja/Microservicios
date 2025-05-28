from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
import logging
import sys
import time

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Importar y registrar los routers
from .api.v1.endpoints import aeropuertos
app.include_router(aeropuertos.router, prefix=settings.API_V1_STR)

@app.on_event("startup")
async def startup_event():
    logger.info("Iniciando aplicación...")
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1} de {max_retries} para crear tablas")
            Base.metadata.create_all(bind=engine)
            logger.info("Tablas creadas correctamente")
            break
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(f"Error al crear tablas (intento {attempt + 1}): {str(e)}")
                time.sleep(retry_delay)
            else:
                logger.error(f"No se pudieron crear las tablas después de {max_retries} intentos: {str(e)}")
                raise

@app.get("/health")
def health_check():
    return {"status": "ok"} 