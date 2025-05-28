# Microservicio de Aviones

Este microservicio forma parte del Sistema de Gestión de Transporte Aéreo y se encarga de la gestión de aviones y su flota.

## 🚀 Características

- Registro y gestión de aviones
- Control de estado y mantenimiento
- Gestión de capacidad y configuración
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
cd aviones-service
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
   - Crear una base de datos MySQL llamada `airline_aviones`
   - Configurar las credenciales en el archivo `.env` (ver sección de configuración)

## ⚙️ Configuración

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_contraseña
DB_NAME=airline_aviones
DEBUG=True
```

## 🚀 Ejecución

1. Activar el entorno virtual (si no está activado):
```bash
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Iniciar el servidor:
```bash
uvicorn app.main:app --reload --port 8003
```

El servicio estará disponible en `http://localhost:8003`

## 📚 Documentación de la API

- Swagger UI: `http://localhost:8003/docs`
- ReDoc: `http://localhost:8003/redoc`

## 📝 Endpoints Disponibles

### Aviones

- `POST /api/v1/aviones/` - Crear un nuevo avión
- `GET /api/v1/aviones/` - Listar todos los aviones
- `GET /api/v1/aviones/{id}` - Obtener un avión específico
- `PUT /api/v1/aviones/{id}` - Actualizar un avión
- `DELETE /api/v1/aviones/{id}` - Eliminar un avión
- `GET /api/v1/aviones/{id}/estado` - Obtener estado de mantenimiento
- `PUT /api/v1/aviones/{id}/estado` - Actualizar estado de mantenimiento

## 📦 Estructura del Proyecto

```
aviones-service/
├── app/
│   ├── api/
│   │   └── endpoints/
│   │       └── aviones.py
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   ├── models/
│   │   └── avion.py
│   ├── schemas/
│   │   └── avion.py
│   ├── services/
│   │   └── avion_service.py
│   └── main.py
├── requirements.txt
└── README.md
```

## 🤝 Comunicación con Otros Microservicios

Este microservicio se comunica con:
- Servicio de Vuelos (para asignación de aviones)
- Servicio de Mantenimiento (para programación de mantenimientos)

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