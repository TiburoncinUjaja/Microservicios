from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
import time
from .logger import logger
from .exceptions import BaseAPIException
from sqlalchemy.exc import SQLAlchemyError
import traceback
from .config import settings
from collections import defaultdict
from datetime import datetime, timedelta

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Agregar headers de seguridad
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.requests = defaultdict(list)
        self.cleanup_task = None

    async def dispatch(self, request: Request, call_next):
        # Obtener IP del cliente
        client_ip = request.client.host
        
        # Limpiar solicitudes antiguas
        current_time = datetime.now()
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if current_time - req_time < timedelta(minutes=1)
        ]
        
        # Verificar límite de tasa
        if len(self.requests[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
            logger.warning(f"Rate limit excedido para IP: {client_ip}")
            return JSONResponse(
                status_code=429,
                content={"detail": "Demasiadas solicitudes. Por favor, intente más tarde."}
            )
        
        # Agregar solicitud actual
        self.requests[client_ip].append(current_time)
        
        # Continuar con la solicitud
        return await call_next(request)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_id = request.headers.get("X-Request-ID", "N/A")
        
        # Log de la petición
        logger.info(
            f"Request ID: {request_id} - "
            f"Method: {request.method} - "
            f"Path: {request.url.path} - "
            f"Client IP: {request.client.host}"
        )
        
        try:
            response = await call_next(request)
            
            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id
            
            # Log de la respuesta
            logger.info(
                f"Request ID: {request_id} - "
                f"Method: {request.method} - "
                f"Path: {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Request ID: {request_id} - "
                f"Error: {str(e)}"
            )
            logger.error(traceback.format_exc())
            raise

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", "N/A")
        try:
            return await call_next(request)
            
        except BaseAPIException as e:
            logger.error(
                f"Request ID: {request_id} - "
                f"API Error: {str(e)}"
            )
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "detail": e.detail,
                    "request_id": request_id
                },
                headers=e.headers
            )
            
        except SQLAlchemyError as e:
            logger.error(
                f"Request ID: {request_id} - "
                f"Database Error: {str(e)}"
            )
            return JSONResponse(
                status_code=503,
                content={
                    "detail": "Error en la base de datos",
                    "request_id": request_id
                }
            )
            
        except Exception as e:
            logger.error(
                f"Request ID: {request_id} - "
                f"Unhandled Error: {str(e)}"
            )
            logger.error(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={
                    "detail": "Error interno del servidor",
                    "request_id": request_id
                }
            ) 