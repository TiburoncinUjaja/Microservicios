from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.usuario import Usuario
from ..core.security import get_password_hash
from ..core.logger import logger
from datetime import datetime

def create_admin_user():
    db = SessionLocal()
    try:
        # Verificar si el usuario ya existe
        admin = db.query(Usuario).filter(Usuario.email == "admin@airline.com").first()
        if admin:
            logger.info("El usuario admin ya existe")
            return
        
        # Crear el usuario admin
        admin = Usuario(
            email="admin@airline.com",
            password_hash=get_password_hash("admin123"),
            nombre="Admin",
            apellido="Sistema",
            rol="admin",
            fecha_creacion=datetime.utcnow(),
            fecha_actualizacion=datetime.utcnow(),
            activo=True
        )
        
        db.add(admin)
        db.commit()
        logger.info("Usuario admin creado exitosamente")
        
    except Exception as e:
        logger.error(f"Error al crear usuario admin: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user() 