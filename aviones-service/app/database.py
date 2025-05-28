from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
import time

# Configurar logging
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}"

# Configuración de reintentos para la conexión a la base de datos
max_retries = 5
retry_delay = 5

for attempt in range(max_retries):
    try:
        logger.info(f"Intento {attempt + 1} de {max_retries} para conectar a la base de datos")
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL,
            pool_pre_ping=True,
            pool_recycle=3600,
            pool_size=5,
            max_overflow=10,
            pool_timeout=30
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        logger.info("Conexión a la base de datos establecida correctamente")
        break
    except Exception as e:
        if attempt < max_retries - 1:
            logger.warning(f"Intento {attempt + 1} falló: {str(e)}")
            time.sleep(retry_delay)
        else:
            logger.error(f"Error al conectar con la base de datos después de {max_retries} intentos: {str(e)}")
            raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Error en la sesión de la base de datos: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

