from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from ...core.security import (
    verify_password,
    create_access_token,
    get_current_user,
    Role,
    check_permissions
)
from ...core.config import settings
from ...core.logger import logger
from ...core.database import get_db
from ...services.auth_service import AuthService
from pydantic import BaseModel

router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    role: str

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Obtiene un token de acceso usando las credenciales del usuario.
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.rol},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=TokenData)
async def read_users_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Obtiene la información del usuario actual.
    """
    user = db.query(Usuario).filter(Usuario.email == current_user).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return {"username": user.email, "role": user.rol}

@router.get("/admin")
async def admin_endpoint(current_user: str = Depends(check_permissions(Role.ADMIN))):
    """
    Endpoint de ejemplo que requiere rol de administrador.
    """
    return {"message": "Acceso concedido al endpoint de administrador"}

@router.get("/staff")
async def staff_endpoint(current_user: str = Depends(check_permissions(Role.STAFF))):
    """
    Endpoint de ejemplo que requiere rol de staff o admin.
    """
    return {"message": "Acceso concedido al endpoint de staff"} 