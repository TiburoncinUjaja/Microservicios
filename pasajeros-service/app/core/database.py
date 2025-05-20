from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from .logger import logger
import time

# Usar la URL de la base de datos directamente desde la configuración
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
logger.info(f"Conectando a la base de datos: {SQLALCHEMY_DATABASE_URL}")

# Crear el motor de SQLAlchemy
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=True
)

# Verificar la conexión y el esquema
max_retries = 3
retry_delay = 2

for attempt in range(max_retries):
    try:
        with engine.connect() as conn:
            # Verificar la base de datos actual
            result = conn.execute(text("SELECT DATABASE()"))
            current_db = result.scalar()
            logger.info(f"Base de datos actual: {current_db}")
            
            # Verificar las tablas existentes
            result = conn.execute(text("SHOW TABLES"))
            tables = result.fetchall()
            logger.info(f"Tablas en la base de datos: {[table[0] for table in tables]}")
            
            # Verificar la estructura de la tabla usuarios
            result = conn.execute(text("DESCRIBE usuarios"))
            columns = result.fetchall()
            logger.info(f"Estructura de la tabla usuarios: {[col[0] for col in columns]}")
            
            # Verificar si el usuario admin existe
            result = conn.execute(text("SELECT * FROM usuarios WHERE email = 'admin@airline.com'"))
            admin = result.fetchone()
            if admin:
                logger.info(f"Usuario admin encontrado: {admin}")
            else:
                logger.warning("Usuario admin no encontrado en la base de datos")
            
            break
    except Exception as e:
        logger.error(f"Error al verificar la base de datos (intento {attempt + 1}/{max_retries}): {str(e)}")
        if attempt < max_retries - 1:
            time.sleep(retry_delay)
        else:
            raise

# Crear la sesión de SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos
Base = declarative_base()

# Función para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        logger.info("Obteniendo sesión de base de datos")
        yield db
    except Exception as e:
        logger.error(f"Error en la sesión de base de datos: {str(e)}")
        raise
    finally:
        logger.info("Cerrando sesión de base de datos")
        db.close() 