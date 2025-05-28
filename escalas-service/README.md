# Microservicio de Escalas

Este microservicio forma parte del Sistema de Gestión de Transporte Aéreo y se encarga de la gestión de escalas y conexiones entre vuelos.

## 🚀 Características

- Gestión de escalas y conexiones
- Control de tiempos de espera
- Validación de rutas y conexiones
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
cd escalas-service
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
   - Crear una base de datos MySQL llamada `airline_escalas`
   - Configurar las credenciales en el archivo `.env` (ver sección de configuración)

## ⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=airline_escalas
DEBUG=True
```

## 🚀 Ejecución

1. Activar el entorno virtual (si no está activado):
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --port 8004
```

El servicio estará disponible en `http://localhost:8004`

## 📚 Documentación de la API

- Swagger UI: `http://localhost:8004/docs`
- ReDoc: `http://localhost:8004/redoc`

## 📝 Endpoints Disponibles

### Escalas

- `POST /api/v1/escalas/` - Crear una nueva escala
- `GET /api/v1/escalas/` - Listar todas las escalas
- `GET /api/v1/escalas/{id}` - Obtener una escala específica
- `PUT /api/v1/escalas/{id}` - Actualizar una escala
- `DELETE /api/v1/escalas/{id}` - Eliminar una escala
- `GET /api/v1/escalas/vuelo/{vuelo_id}` - Obtener escalas de un vuelo
- `GET /api/v1/escalas/aeropuerto/{aeropuerto_id}` - Obtener escalas en un aeropuerto

## 📦 Estructura del Proyecto

```
escalas-service/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── escalas.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── escala.py
│   ├── schemas/
│   │   └── escala.py
│   ├── services/
│   │   └── escala_service.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🤝 Comunicación con Otros Microservicios

Este microservicio se comunica con:
- Servicio de Vuelos (para gestión de conexiones)
- Servicio de Aeropuertos (para validación de ubicaciones)
- Servicio de Reservas (para gestión de pasajeros en conexiones)

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