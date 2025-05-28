# Microservicio de Reservas

Este microservicio forma parte del Sistema de Gestión de Transporte Aéreo y se encarga de la gestión de reservas y boletos de vuelo.

## 🚀 Características

- Gestión de reservas y boletos
- Control de disponibilidad de asientos
- Procesamiento de pagos
- Gestión de cancelaciones y cambios
- API RESTful documentada
- Integración con base de datos MySQL
- Documentación automática con Swagger

## 📋 Prerrequisitos

- Python 3.10 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd reservas-service
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar la base de datos:
   - Crear una base de datos MySQL llamada `airline_reservas`
   - Configurar las credenciales en el archivo `.env` (ver sección de configuración)

## ⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=airline_reservas
DEBUG=True
```

## 🚀 Ejecución

1. Activar el entorno virtual (si no está activado):
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --port 8005
```

El servicio estará disponible en `http://localhost:8005`

## 📚 Documentación de la API

- Swagger UI: `http://localhost:8005/docs`
- ReDoc: `http://localhost:8005/redoc`

## 📝 Endpoints Disponibles

### Reservas

- `POST /api/v1/reservas/` - Crear una nueva reserva
- `GET /api/v1/reservas/` - Listar todas las reservas
- `GET /api/v1/reservas/{id}` - Obtener una reserva específica
- `PUT /api/v1/reservas/{id}` - Actualizar una reserva
- `DELETE /api/v1/reservas/{id}` - Cancelar una reserva
- `GET /api/v1/reservas/pasajero/{pasajero_id}` - Obtener reservas de un pasajero
- `GET /api/v1/reservas/vuelo/{vuelo_id}` - Obtener reservas de un vuelo
- `POST /api/v1/reservas/{id}/pago` - Procesar pago de reserva
- `POST /api/v1/reservas/{id}/cambio` - Solicitar cambio de reserva

## 📦 Estructura del Proyecto

```
reservas-service/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── reservas.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── reserva.py
│   ├── schemas/
│   │   └── reserva.py
│   ├── services/
│   │   └── reserva_service.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🤝 Comunicación con Otros Microservicios

Este microservicio se comunica con:
- Servicio de Pasajeros (para validación de datos)
- Servicio de Vuelos (para disponibilidad)
- Servicio de Escalas (para conexiones)
- Servicio de Pagos (para procesamiento de transacciones)

## 🧪 Testing

Para ejecutar los tests:
```bash
pytest
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👥 Contribución

1. Fork el proyecto
2. Crea tu rama de características (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 🐳 Despliegue con Docker

Este microservicio está configurado para ser desplegado usando Docker y Docker Compose. Asegúrate de tener Docker Desktop instalado y en ejecución.

1. **Construir y levantar los servicios:**

   ```bash
   docker-compose up -d
   ```

   Este comando construye las imágenes (si es necesario) y levanta los servicios definidos en el archivo `docker-compose.yml`.

2. **Detener los servicios:**

   ```bash
   docker-compose down
   ```

   Este comando detiene y elimina los contenedores.

3. **Configuración para diferentes entornos:**

   Puedes usar variables de entorno (por ejemplo, en el archivo `.env`) para configurar el microservicio según el entorno (desarrollo, pruebas, producción). 