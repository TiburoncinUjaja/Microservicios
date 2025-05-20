from sqlalchemy.orm import Session
from ..models.usuario import Usuario
from ..core.security import verify_password
from ..core.logger import logger

class AuthService:
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> Usuario:
        """
        Autentica un usuario usando email y contraseña.
        """
        try:
            logger.info(f"Intentando autenticar usuario: {email}")
            user = db.query(Usuario).filter(Usuario.email == email).first()
            
            if not user:
                logger.warning(f"Intento de login fallido: usuario no encontrado - {email}")
                return None
            
            logger.info(f"Usuario encontrado, verificando contraseña para: {email}")
            logger.info(f"Hash almacenado: {user.password_hash}")
            logger.info(f"Contraseña proporcionada: {password}")
            
            if not verify_password(password, user.password_hash):
                logger.warning(f"Intento de login fallido: contraseña incorrecta - {email}")
                return None
            
            logger.info(f"Login exitoso para usuario: {email}")
            return user
        except Exception as e:
            logger.error(f"Error en autenticación: {str(e)}")
            return None 