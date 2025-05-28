import os
import sys
import logging
from sqlalchemy import create_engine, text

# Agregar el directorio raíz al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.database import Base
from app.core.config import settings

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    try:
        # Crear engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Eliminar tablas existentes
        logger.info("Eliminando tablas existentes...")
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            conn.execute(text("DROP TABLE IF EXISTS vuelos"))
            conn.execute(text("DROP TABLE IF EXISTS tripulacion_vuelo"))
            conn.execute(text("DROP TABLE IF EXISTS escalas"))
            conn.execute(text("DROP TABLE IF EXISTS personal"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()
        logger.info("Tablas eliminadas exitosamente")

        # Recrear tablas
        logger.info("Recreando tablas...")
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas recreadas exitosamente")

    except Exception as e:
        logger.error(f"Error al recrear la base de datos: {str(e)}")
        raise

if __name__ == "__main__":
    recreate_database() 