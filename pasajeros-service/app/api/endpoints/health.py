from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.database import get_db, engine
from ...core.logger import logger
from sqlalchemy import text
import time
from fastapi_health import health
from typing import Dict, Any
import psutil
from ...core.resilience import check_dependency_health
from ...core.config import settings

router = APIRouter()

async def check_database() -> Dict[str, Any]:
    """Verifica el estado de la base de datos"""
    is_healthy = await check_dependency_health("database")
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "component": "database",
        "timestamp": time.time()
    }

async def check_rabbitmq() -> Dict[str, Any]:
    """Verifica el estado de RabbitMQ"""
    is_healthy = await check_dependency_health("rabbitmq")
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "component": "rabbitmq",
        "timestamp": time.time()
    }

async def check_redis() -> Dict[str, Any]:
    """Verifica el estado de Redis"""
    is_healthy = await check_dependency_health("redis")
    return {
        "status": "healthy" if is_healthy else "unhealthy",
        "component": "redis",
        "timestamp": time.time()
    }

async def check_system_resources() -> Dict[str, Any]:
    """Verifica los recursos del sistema"""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "status": "healthy" if cpu_percent < 90 and memory.percent < 90 and disk.percent < 90 else "unhealthy",
        "component": "system_resources",
        "details": {
            "cpu_usage_percent": cpu_percent,
            "memory_usage_percent": memory.percent,
            "disk_usage_percent": disk.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_free_gb": round(disk.free / (1024**3), 2)
        },
        "timestamp": time.time()
    }

@router.get("/health")
async def health_check():
    """Endpoint de health check que verifica todos los componentes del sistema"""
    health_checks = [
        check_database,
        check_rabbitmq,
        check_redis,
        check_system_resources
    ]
    
    results = {}
    for check in health_checks:
        try:
            result = await check()
            results[result["component"]] = result
        except Exception as e:
            results[check.__name__] = {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
    
    # Determinar el estado general del sistema
    all_healthy = all(result["status"] == "healthy" for result in results.values())
    
    return {
        "status": "healthy" if all_healthy else "unhealthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "timestamp": time.time(),
        "components": results
    }

@router.get("/health/live")
async def liveness_check():
    """Endpoint de liveness check - verifica si el servicio está vivo"""
    return {"status": "alive", "timestamp": time.time()}

@router.get("/health/ready")
async def readiness_check():
    """Endpoint de readiness check - verifica si el servicio está listo para recibir tráfico"""
    # Verificar dependencias críticas
    db_healthy = await check_dependency_health("database")
    rabbitmq_healthy = await check_dependency_health("rabbitmq")
    
    is_ready = db_healthy and rabbitmq_healthy
    
    return {
        "status": "ready" if is_ready else "not_ready",
        "timestamp": time.time(),
        "dependencies": {
            "database": "ready" if db_healthy else "not_ready",
            "rabbitmq": "ready" if rabbitmq_healthy else "not_ready"
        }
    }

@router.get("/health/db")
async def db_health_check(db: Session = Depends(get_db)):
    """
    Health check de la base de datos.
    """
    try:
        # Intentar una consulta simple
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": time.time()
        }
    except Exception as e:
        logger.error(f"Error en health check de base de datos: {str(e)}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": time.time()
        }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """
    Health check detallado que incluye todos los componentes.
    """
    health_info = {
        "status": "healthy",
        "timestamp": time.time(),
        "components": {
            "api": "healthy",
            "database": "checking"
        }
    }

    # Verificar base de datos
    try:
        db.execute(text("SELECT 1"))
        health_info["components"]["database"] = "healthy"
    except Exception as e:
        logger.error(f"Error en health check detallado de base de datos: {str(e)}")
        health_info["components"]["database"] = "unhealthy"
        health_info["status"] = "unhealthy"
        health_info["database_error"] = str(e)

    return health_info 