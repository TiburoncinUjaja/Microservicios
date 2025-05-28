from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_database():
    try:
        # Crear conexión a la base de datos
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Verificar la conexión
        logger.info("Verificando conexión a la base de datos...")
        result = db.execute("SELECT DATABASE()").scalar()
        logger.info(f"Base de datos actual: {result}")

        # Verificar tablas
        logger.info("Verificando tablas en la base de datos...")
        result = db.execute("SHOW TABLES").fetchall()
        tables = [row[0] for row in result]
        logger.info(f"Tablas encontradas: {tables}")

        # Verificar datos en la tabla vuelos
        logger.info("Verificando datos en la tabla vuelos...")
        result = db.execute("SELECT * FROM vuelos").fetchall()
        if result:
            logger.info(f"Vuelos encontrados: {len(result)}")
            for vuelo in result:
                logger.info(f"Vuelo: ID={vuelo[0]}, Número={vuelo[1]}, Estado={vuelo[7]}")
        else:
            logger.warning("No se encontraron vuelos en la base de datos")

    except Exception as e:
        logger.error(f"Error verificando la base de datos: {str(e)}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    verify_database() 