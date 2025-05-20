from sqlalchemy.orm import Session
from ..core.database import SessionLocal
from ..models.usuario import Usuario
from ..core.security import get_password_hash
from ..core.logger import logger

def update_admin_password():
    db = SessionLocal()
    try:
        # Buscar el usuario admin
        admin = db.query(Usuario).filter(Usuario.email == "admin@airline.com").first()
        if not admin:
            logger.error("Usuario admin no encontrado")
            return
        
        # Generar nuevo hash
        new_password = "admin123"
        new_hash = get_password_hash(new_password)
        
        # Actualizar el hash
        admin.password_hash = new_hash
        db.commit()
        
        logger.info("Contraseña de admin actualizada exitosamente")
        logger.info(f"Nuevo hash: {new_hash}")
    except Exception as e:
        logger.error(f"Error al actualizar contraseña: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin_password() 