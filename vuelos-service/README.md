# Microservicio de Vuelos

Este microservicio forma parte del Sistema de Gestión de Transporte Aéreo y se encarga de la gestión de vuelos y rutas aéreas.

## 🚀 Características

- Gestión de vuelos y rutas
- Control de horarios y programación
- Gestión de tripulación
- Control de estado de vuelos
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
cd vuelos-service
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
   - Crear una base de datos MySQL llamada `airline_vuelos`
   - Configurar las credenciales en el archivo `.env` (ver sección de configuración)

## ⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=airline_vuelos
DEBUG=True
```

## 🚀 Ejecución

1. Activar el entorno virtual (si no está activado):
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --port 8006
```

El servicio estará disponible en `http://localhost:8006`

## 📚 Documentación de la API

- Swagger UI: `http://localhost:8006/docs`
- ReDoc: `http://localhost:8006/redoc`

## 📝 Endpoints Disponibles

### Vuelos

- `POST /api/v1/vuelos/` - Crear un nuevo vuelo
- `GET /api/v1/vuelos/` - Listar todos los vuelos
- `GET /api/v1/vuelos/{id}` - Obtener un vuelo específico
- `PUT /api/v1/vuelos/{id}` - Actualizar un vuelo
- `DELETE /api/v1/vuelos/{id}` - Eliminar un vuelo
- `GET /api/v1/vuelos/origen/{aeropuerto_id}` - Obtener vuelos por origen
- `GET /api/v1/vuelos/destino/{aeropuerto_id}` - Obtener vuelos por destino
- `GET /api/v1/vuelos/avion/{avion_id}` - Obtener vuelos por avión
- `PUT /api/v1/vuelos/{id}/estado` - Actualizar estado del vuelo
- `GET /api/v1/vuelos/{id}/tripulacion` - Obtener tripulación del vuelo
- `PUT /api/v1/vuelos/{id}/tripulacion` - Asignar tripulación al vuelo

## 📦 Estructura del Proyecto

```
vuelos-service/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── vuelos.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── vuelo.py
│   ├── schemas/
│   │   └── vuelo.py
│   ├── services/
│   │   └── vuelo_service.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🤝 Comunicación con Otros Microservicios

Este microservicio se comunica con:
- Servicio de Aeropuertos (para rutas)
- Servicio de Aviones (para asignación)
- Servicio de Escalas (para conexiones)
- Servicio de Reservas (para disponibilidad)
- Servicio de Tripulación (para asignación de personal)

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