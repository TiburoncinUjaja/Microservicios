from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import logging
from sqlalchemy.exc import SQLAlchemyError
from app.core.config import settings
from app.api.v1.endpoints import escalas
from app.db.session import engine
from app.models import escala
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
    version=settings.VERSION,
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

# Configurar métricas de Prometheus
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Incluir routers
app.include_router(escalas.router, prefix=f"{settings.API_V1_STR}/escalas", tags=["escalas"])

@app.on_event("startup")
async def startup_event():
    logger.info(f"Iniciando {settings.PROJECT_NAME}")
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1} de {max_retries} para crear tablas")
            escala.Base.metadata.create_all(bind=engine)
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

if __name__ == "__main__":
    import uvicorn
    logger.info("Iniciando aplicación con uvicorn...")
    uvicorn.run(
        "app.main:app",
        host=settings.SERVICE_HOST,
        port=int(settings.SERVICE_PORT),
        reload=settings.DEBUG
    ) 