from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class BaseAPIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class DatabaseException(BaseAPIException):
    def __init__(
        self,
        detail: str = "Error en la base de datos",
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail,
            headers=headers
        )

class PasajeroNotFoundException(BaseAPIException):
    def __init__(
        self,
        pasajero_id: int,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pasajero con ID {pasajero_id} no encontrado",
            headers=headers
        )

class PasajeroDuplicadoException(BaseAPIException):
    def __init__(
        self,
        numero_documento: str,
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe un pasajero con el número de documento {numero_documento}",
            headers=headers
        )

class ValidationException(BaseAPIException):
    def __init__(
        self,
        detail: str = "Error de validación en los datos",
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            headers=headers
        )

class ExternalServiceException(BaseAPIException):
    def __init__(
        self,
        service_name: str,
        detail: str = "Error en servicio externo",
        headers: Optional[Dict[str, str]] = None
    ) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Error en el servicio {service_name}: {detail}",
            headers=headers
        )

class UsuarioNotFoundException(Exception):
    def __init__(self, usuario_id: int):
        self.usuario_id = usuario_id
        super().__init__(f"Usuario no encontrado con ID: {usuario_id}") 