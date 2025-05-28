from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.models.vuelo import Vuelo
from datetime import datetime, timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def insert_test_data():
    try:
        # Crear conexión a la base de datos
        engine = create_engine(settings.DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()

        # Crear datos de prueba
        test_vuelos = [
            Vuelo(
                id=1,
                numero_vuelo="AV001",
                fecha_hora_salida=datetime.now(),
                fecha_hora_llegada=datetime.now() + timedelta(hours=2),
                aeropuerto_origen_id=1,
                aeropuerto_destino_id=2,
                avion_id=1,
                estado="PROGRAMADO"
            ),
            Vuelo(
                id=2,
                numero_vuelo="AV002",
                fecha_hora_salida=datetime.now() + timedelta(hours=3),
                fecha_hora_llegada=datetime.now() + timedelta(hours=5),
                aeropuerto_origen_id=2,
                aeropuerto_destino_id=3,
                avion_id=2,
                estado="PROGRAMADO"
            )
        ]

        # Insertar datos
        logger.info("Insertando datos de prueba...")
        for vuelo in test_vuelos:
            db.add(vuelo)
        
        db.commit()
        logger.info("Datos de prueba insertados correctamente")

    except Exception as e:
        logger.error(f"Error insertando datos de prueba: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    insert_test_data() 