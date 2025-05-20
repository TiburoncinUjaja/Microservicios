# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto que usa la aplicación
EXPOSE 8002

# Variables de entorno por defecto
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    APP_NAME="Reservas Service" \
    VERSION="1.0.0" \
    API_PREFIX="/api/v1" \
    DEBUG="true" \
    LOG_LEVEL="INFO" \
    LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s" \
    DATABASE_URL="mysql://root:root@mysql:3306/airline_reservas" \
    REDIS_URL="redis://redis:6379/0" \
    RABBITMQ_URL="amqp://guest:guest@rabbitmq:5672/" \
    PASAJEROS_SERVICE_URL="http://pasajeros-service:8001" \
    VUELOS_SERVICE_URL="http://vuelos-service:8003" \
    SERVICE_PORT="8002" \
    SERVICE_HOST="0.0.0.0" \
    SECRET_KEY="tu_clave_secreta_muy_segura" \
    ALGORITHM="HS256" \
    ACCESS_TOKEN_EXPIRE_MINUTES="30"

# Script de inicio
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Comando para ejecutar la aplicación
CMD ["/wait-for-it.sh", "mysql:3306", "--", "python", "-m", "app.main"] 