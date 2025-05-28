# Sistema de Reservas de Vuelos

Este proyecto implementa un sistema de microservicios para la gestión de reservas de vuelos, utilizando FastAPI, MySQL, Redis y Docker.

## Servicios Implementados

### Servicio de Pasajeros
- Gestión de usuarios y autenticación
- CRUD de pasajeros
- Validación de datos

### Servicio de Reservas
- Gestión de reservas de vuelos
- Validación de disponibilidad
- Integración con servicio de vuelos (pendiente)

## Requisitos

- Docker y Docker Compose
- Python 3.8+
- MySQL 8.0
- Redis

## Configuración

1. Clonar el repositorio
2. Crear archivo `.env` con las variables de entorno necesarias
3. Ejecutar `docker-compose up -d`

## Variables de Entorno

Crear un archivo `.env` con las siguientes variables:

```env
# MySQL
MYSQL_ROOT_PASSWORD=root
MYSQL_MULTIPLE_DATABASES=airline_pasajeros,airline_reservas

# Redis
REDIS_PASSWORD=redis123

# Servicios
PASAJEROS_SERVICE_PORT=8001
RESERVAS_SERVICE_PORT=8002
```

## Uso

1. Iniciar los servicios:
```bash
docker-compose up -d
```

2. Acceder a los servicios:
- Pasajeros: http://localhost:8001
- Reservas: http://localhost:8002
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Documentación API

- Pasajeros: http://localhost:8001/docs
- Reservas: http://localhost:8002/docs

## Notas

- El servicio de vuelos está pendiente de implementación
- Las credenciales por defecto son:
  - Usuario: admin@airline.com
  - Contraseña: admin123 