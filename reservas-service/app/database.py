import logging
import time
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.reserva import Reserva  # Importar el modelo Reserva

# Configurar logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format=settings.LOG_FORMAT,
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Configuración del engine con reintentos y timeouts
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=5,
    max_overflow=10,
    connect_args={
        "connect_timeout": 10
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        raise
    finally:
        db.close()

def init_db():
    max_retries = 10
    retry_delay = 5
    
    logger.info(f"Conectando a la base de datos: {SQLALCHEMY_DATABASE_URL}")
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Intento {attempt + 1} de {max_retries} para conectar a la base de datos")
            with engine.connect() as conn:
                # Verificar la conexión usando text()
                conn.execute(text("SELECT 1"))
                logger.info("Conexión exitosa a la base de datos")
                # Crear tablas
                Base.metadata.create_all(bind=engine)
                logger.info("Tablas creadas exitosamente")
                return
        except Exception as e:
            logger.warning(f"Intento {attempt + 1} falló: {str(e)}")
            if attempt < max_retries - 1:
                logger.info(f"Esperando {retry_delay} segundos antes del siguiente intento...")
                time.sleep(retry_delay)
            else:
                logger.error(f"Error al conectar con la base de datos después de {max_retries} intentos: {str(e)}")
                raise

# Inicializar la base de datos al importar el módulo
init_db() 