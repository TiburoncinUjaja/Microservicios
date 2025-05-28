from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Use the DATABASE_URL directly from settings
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
logger.info(f"Database URL: {SQLALCHEMY_DATABASE_URL}")

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database connection successful")
except Exception as e:
    logger.error(f"Error connecting to database: {str(e)}")
    raise

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 