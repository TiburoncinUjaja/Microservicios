from typing import Optional, Callable, Any
import pybreaker
from functools import wraps
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

# Circuit breaker para operaciones de base de datos
db_breaker = pybreaker.CircuitBreaker(
    fail_max=5,  # Número máximo de fallos antes de abrir el circuito
    reset_timeout=60,  # Tiempo en segundos antes de intentar cerrar el circuito
    exclude=[ValueError, AttributeError],  # Excepciones que no cuentan como fallos
    name="database_operations"
)

# Circuit breaker para operaciones de RabbitMQ
rabbitmq_breaker = pybreaker.CircuitBreaker(
    fail_max=3,
    reset_timeout=30,
    exclude=[ValueError],
    name="rabbitmq_operations"
)

def circuit_breaker(breaker: pybreaker.CircuitBreaker):
    """
    Decorador para aplicar circuit breakers a funciones
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            try:
                return await breaker(func)(*args, **kwargs)
            except pybreaker.CircuitBreakerError as e:
                logger.error(f"Circuit breaker {breaker.name} está abierto: {str(e)}")
                # Aquí podrías implementar una lógica de fallback
                raise
            except Exception as e:
                logger.error(f"Error en {func.__name__}: {str(e)}")
                raise
        return wrapper
    return decorator

# Función de retry con backoff exponencial
async def retry_with_backoff(
    func: Callable,
    max_retries: int = 3,
    initial_delay: float = 1.0,
    max_delay: float = 10.0,
    *args,
    **kwargs
) -> Any:
    """
    Implementa retry con backoff exponencial para operaciones que pueden fallar
    """
    delay = initial_delay
    last_exception = None

    for attempt in range(max_retries):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt == max_retries - 1:
                raise last_exception
            
            logger.warning(
                f"Intento {attempt + 1} fallido para {func.__name__}. "
                f"Reintentando en {delay} segundos..."
            )
            
            await asyncio.sleep(delay)
            delay = min(delay * 2, max_delay)

    raise last_exception

# Función para verificar el estado de salud de dependencias
async def check_dependency_health(dependency_name: str) -> bool:
    """
    Verifica el estado de salud de una dependencia específica
    """
    try:
        if dependency_name == "database":
            # Implementar verificación de base de datos
            return True
        elif dependency_name == "rabbitmq":
            # Implementar verificación de RabbitMQ
            return True
        elif dependency_name == "redis":
            # Implementar verificación de Redis
            return True
        return False
    except Exception as e:
        logger.error(f"Error verificando salud de {dependency_name}: {str(e)}")
        return False 