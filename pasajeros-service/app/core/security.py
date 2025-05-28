from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from ..core.config import settings
from ..core.logger import logger

# Configuración de seguridad
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_PREFIX}/auth/token")

# Funciones de seguridad
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Genera un hash de la contraseña."""
    return pwd_context.hash(password)

def generate_test_hash(password: str) -> str:
    """Genera un hash de prueba para la contraseña."""
    test_hash = pwd_context.hash(password)
    logger.info(f"Hash generado para '{password}': {test_hash}")
    return test_hash

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Crea un token JWT."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error al crear token JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al generar token de acceso"
        )

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Obtiene el usuario actual basado en el token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as e:
        logger.error(f"Error al decodificar token JWT: {str(e)}")
        raise credentials_exception
    
    # Aquí deberías obtener el usuario de tu base de datos
    # Por ahora retornamos el username como ejemplo
    return username

# Roles y permisos
class Role:
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"

def check_permissions(required_role: str):
    """Decorator para verificar permisos basados en roles."""
    async def permission_checker(current_user: str = Depends(get_current_user)):
        # Aquí deberías verificar el rol del usuario contra la base de datos
        # Por ahora, asumimos que todos los usuarios tienen el rol USER
        user_role = Role.USER
        
        if required_role == Role.ADMIN and user_role != Role.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes"
            )
        elif required_role == Role.STAFF and user_role not in [Role.ADMIN, Role.STAFF]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes"
            )
        return current_user
    return permission_checker 