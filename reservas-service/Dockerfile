# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
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
    MYSQL_HOST="mysql" \
    MYSQL_PORT="3307" \
    MYSQL_USER="root" \
    MYSQL_PASSWORD="1092" \
    MYSQL_DATABASE="airline_reservas" \
    REDIS_HOST="redis" \
    REDIS_PORT="6379" \
    RABBITMQ_HOST="rabbitmq" \
    RABBITMQ_PORT="5672" \
    RABBITMQ_USER="guest" \
    RABBITMQ_PASSWORD="guest" \
    SERVICE_PORT="8002" \
    SERVICE_HOST="0.0.0.0" \
    SECRET_KEY="tu_clave_secreta_muy_segura" \
    ALGORITHM="HS256" \
    ACCESS_TOKEN_EXPIRE_MINUTES="30"

# Script de inicio
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"] 