FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    netcat-traditional \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 8004

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8004"] 