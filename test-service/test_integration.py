import requests
import pytest
import json
from datetime import datetime, timedelta, date
import time

# Configuración de URLs base para cada servicio
PASAJEROS_URL = "http://localhost:8001/api/v1"
AVIONES_URL = "http://localhost:8004/api/v1"
VUELOS_URL = "http://localhost:8003/api/v1"
RESERVAS_URL = "http://localhost:8004/api/v1"

# Variables globales para almacenar IDs y token
PASAJERO_ID = None
AVION_ID = None
VUELO_ID = None
RESERVA_ID = None
TOKEN = None

def get_auth_headers():
    """Obtiene los headers con el token de autenticación"""
    if not TOKEN:
        test_obtener_token()
    return {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

def test_obtener_token():
    """Test para obtener el token de autenticación"""
    global TOKEN
    auth_data = {
        "username": "admin@airline.com",
        "password": "admin123"
    }
    
    response = requests.post(
        f"{PASAJEROS_URL}/token",
        json=auth_data
    )
    assert response.status_code == 200, f"Error al obtener token: {response.text}"
    TOKEN = response.json()["access_token"]
    return response.json()

# Función auxiliar para esperar a que un servicio esté disponible
def wait_for_service(url, max_retries=5, delay=2):
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/health")  # Removido headers=get_auth_headers()
            if response.status_code < 500:  # Si no es un error del servidor
                return True
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(delay)
    return False

# Verificar que los servicios estén disponibles antes de las pruebas
@pytest.fixture(autouse=True)
def setup():
    assert wait_for_service(PASAJEROS_URL), "Servicio de pasajeros no disponible"
    assert wait_for_service(AVIONES_URL), "Servicio de aviones no disponible"
    assert wait_for_service(VUELOS_URL), "Servicio de vuelos no disponible"
    assert wait_for_service(RESERVAS_URL), "Servicio de reservas no disponible"

def test_crear_pasajero():
    """Test para crear un pasajero"""
    global PASAJERO_ID
    pasajero_data = {
        "usuario_id": 1,
        "tipo_documento": "PASAPORTE",
        "numero_documento": f"ABC{int(time.time())}",
        "nacionalidad": "Española",
        "fecha_nacimiento": "1990-01-02",
        "telefono": "123456789",
        "direccion": "Calle Principal 123"
    }
    
    response = requests.post(
        f"{PASAJEROS_URL}/pasajeros",
        json=pasajero_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, f"Error al crear pasajero: {response.text}"
    PASAJERO_ID = response.json()["id"]
    return response.json()

def test_crear_avion():
    """Test para crear un avión"""
    global AVION_ID
    avion_data = {
        "matricula": f"EC-{int(time.time())}",
        "modelo": "Boeing 737",
        "capacidad_pasajeros": 180,
        "capacidad_carga": 5000,
        "estado": "ACTIVO",
        "ultima_revision": datetime.now().isoformat(),
        "proxima_revision": (datetime.now() + timedelta(days=180)).isoformat()
    }
    
    response = requests.post(
        f"{AVIONES_URL}/aviones",
        json=avion_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, f"Error al crear avión: {response.text}"
    AVION_ID = response.json()["id"]
    return response.json()

def test_crear_vuelo():
    """Test para crear un vuelo"""
    global VUELO_ID
    # Asegurarse de que existe un avión
    if not AVION_ID:
        test_crear_avion()
    
    vuelo_data = {
        "origen": "MAD",
        "destino": "BCN",
        "fecha_salida": (datetime.now() + timedelta(days=1)).isoformat(),
        "fecha_llegada": (datetime.now() + timedelta(days=1, hours=2)).isoformat(),
        "avion_id": AVION_ID,
        "estado": "programado",
        "precio_base": 150.00,
        "asientos_disponibles": 150
    }
    
    response = requests.post(
        f"{VUELOS_URL}/vuelos",
        json=vuelo_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, f"Error al crear vuelo: {response.text}"
    VUELO_ID = response.json()["id"]
    return response.json()

def test_crear_reserva():
    """Test para crear una reserva"""
    global RESERVA_ID
    # Asegurarse de que existen pasajero y vuelo
    if not PASAJERO_ID:
        test_crear_pasajero()
    if not VUELO_ID:
        test_crear_vuelo()
    
    reserva_data = {
        "pasajero_id": PASAJERO_ID,
        "vuelo_id": VUELO_ID,
        "fecha_reserva": datetime.now().isoformat(),
        "estado": "confirmada",
        "asiento": "12A",
        "precio_final": 150.00
    }
    
    response = requests.post(
        f"{RESERVAS_URL}/reservas",
        json=reserva_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 201, f"Error al crear reserva: {response.text}"
    RESERVA_ID = response.json()["id"]
    return response.json()

def test_obtener_pasajero():
    """Test para obtener un pasajero"""
    if not PASAJERO_ID:
        test_crear_pasajero()
    
    response = requests.get(
        f"{PASAJEROS_URL}/pasajeros/{PASAJERO_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener pasajero: {response.text}"
    return response.json()

def test_obtener_avion():
    """Test para obtener un avión"""
    if not AVION_ID:
        test_crear_avion()
    
    response = requests.get(
        f"{AVIONES_URL}/aviones/{AVION_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener avión: {response.text}"
    return response.json()

def test_obtener_vuelo():
    """Test para obtener un vuelo"""
    if not VUELO_ID:
        test_crear_vuelo()
    
    response = requests.get(
        f"{VUELOS_URL}/vuelos/{VUELO_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener vuelo: {response.text}"
    return response.json()

def test_obtener_reserva():
    """Test para obtener una reserva"""
    if not RESERVA_ID:
        test_crear_reserva()
    
    response = requests.get(
        f"{RESERVAS_URL}/reservas/{RESERVA_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener reserva: {response.text}"
    return response.json()

def test_actualizar_pasajero():
    """Test para actualizar un pasajero"""
    if not PASAJERO_ID:
        test_crear_pasajero()
    
    pasajero_data = {
        "tipo_documento": "PASAPORTE",
        "numero_documento": f"P{int(time.time())}",
        "fecha_nacimiento": "1990-01-01",
        "nacionalidad": "Española",
        "telefono": "987654321",
        "direccion": "Calle Nueva 456"
    }
    
    response = requests.put(
        f"{PASAJEROS_URL}/pasajeros/{PASAJERO_ID}",
        json=pasajero_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al actualizar pasajero: {response.text}"
    return response.json()

def test_actualizar_avion():
    """Test para actualizar un avión"""
    if not AVION_ID:
        test_crear_avion()
    
    avion_data = {
        "modelo": "Boeing 737",
        "capacidad_pasajeros": 180,
        "capacidad_carga": 5000,
        "estado": "mantenimiento",
        "ultima_revision": datetime.now().isoformat(),
        "proxima_revision": (datetime.now() + timedelta(days=180)).isoformat()
    }
    
    response = requests.put(
        f"{AVIONES_URL}/aviones/{AVION_ID}",
        json=avion_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al actualizar avión: {response.text}"
    return response.json()

def test_actualizar_vuelo():
    """Test para actualizar un vuelo"""
    if not VUELO_ID:
        test_crear_vuelo()
    
    vuelo_data = {
        "origen": "MAD",
        "destino": "BCN",
        "fecha_salida": (datetime.now() + timedelta(days=2)).isoformat(),
        "fecha_llegada": (datetime.now() + timedelta(days=2, hours=2)).isoformat(),
        "avion_id": AVION_ID,
        "estado": "retrasado",
        "precio_base": 175.00,
        "asientos_disponibles": 145
    }
    
    response = requests.put(
        f"{VUELOS_URL}/vuelos/{VUELO_ID}",
        json=vuelo_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al actualizar vuelo: {response.text}"
    return response.json()

def test_actualizar_reserva():
    """Test para actualizar una reserva"""
    if not RESERVA_ID:
        test_crear_reserva()
    
    reserva_data = {
        "pasajero_id": PASAJERO_ID,
        "vuelo_id": VUELO_ID,
        "fecha_reserva": datetime.now().isoformat(),
        "estado": "cancelada",
        "asiento": "12A",
        "precio_final": 150.00
    }
    
    response = requests.put(
        f"{RESERVAS_URL}/reservas/{RESERVA_ID}",
        json=reserva_data,
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al actualizar reserva: {response.text}"
    return response.json()

def test_eliminar_reserva():
    """Test para eliminar una reserva"""
    if not RESERVA_ID:
        test_crear_reserva()
    
    response = requests.delete(
        f"{RESERVAS_URL}/reservas/{RESERVA_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 204, f"Error al eliminar reserva: {response.text}"

def test_eliminar_vuelo():
    """Test para eliminar un vuelo"""
    if not VUELO_ID:
        test_crear_vuelo()
    
    response = requests.delete(
        f"{VUELOS_URL}/vuelos/{VUELO_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 204, f"Error al eliminar vuelo: {response.text}"

def test_eliminar_avion():
    """Test para eliminar un avión"""
    if not AVION_ID:
        test_crear_avion()
    
    response = requests.delete(
        f"{AVIONES_URL}/aviones/{AVION_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 204, f"Error al eliminar avión: {response.text}"

def test_eliminar_pasajero():
    """Test para eliminar un pasajero"""
    if not PASAJERO_ID:
        test_crear_pasajero()
    
    response = requests.delete(
        f"{PASAJEROS_URL}/pasajeros/{PASAJERO_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 204, f"Error al eliminar pasajero: {response.text}"

def test_listar_pasajeros():
    """Test para listar todos los pasajeros"""
    response = requests.get(
        f"{PASAJEROS_URL}/pasajeros",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al listar pasajeros: {response.text}"
    return response.json()

def test_listar_aviones():
    """Test para listar todos los aviones"""
    response = requests.get(
        f"{AVIONES_URL}/aviones",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al listar aviones: {response.text}"
    return response.json()

def test_listar_vuelos():
    """Test para listar todos los vuelos"""
    response = requests.get(
        f"{VUELOS_URL}/vuelos",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al listar vuelos: {response.text}"
    return response.json()

def test_listar_reservas():
    """Test para listar todas las reservas"""
    response = requests.get(
        f"{RESERVAS_URL}/reservas",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al listar reservas: {response.text}"
    return response.json()

def test_buscar_vuelos_por_fecha():
    """Test para buscar vuelos por fecha"""
    fecha_inicio = (datetime.now() + timedelta(days=1)).date().isoformat()
    fecha_fin = (datetime.now() + timedelta(days=7)).date().isoformat()
    
    response = requests.get(
        f"{VUELOS_URL}/vuelos/buscar",
        params={"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin},
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al buscar vuelos por fecha: {response.text}"
    return response.json()

def test_buscar_vuelos_por_ruta():
    """Test para buscar vuelos por ruta"""
    response = requests.get(
        f"{VUELOS_URL}/vuelos/buscar",
        params={"origen": "MAD", "destino": "BCN"},
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al buscar vuelos por ruta: {response.text}"
    return response.json()

def test_obtener_reservas_por_pasajero():
    """Test para obtener las reservas de un pasajero"""
    if not PASAJERO_ID:
        test_crear_pasajero()
    
    response = requests.get(
        f"{RESERVAS_URL}/reservas/pasajero/{PASAJERO_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener reservas del pasajero: {response.text}"
    return response.json()

def test_obtener_vuelos_por_avion():
    """Test para obtener los vuelos de un avión"""
    if not AVION_ID:
        test_crear_avion()
    
    response = requests.get(
        f"{VUELOS_URL}/vuelos/avion/{AVION_ID}",
        headers=get_auth_headers()
    )
    assert response.status_code == 200, f"Error al obtener vuelos del avión: {response.text}"
    return response.json()

def test_integracion_completa():
    """Test de integración completa que prueba el flujo completo"""
    # 0. Obtener token
    token_response = test_obtener_token()
    assert "access_token" in token_response
    
    # 1. Crear pasajero
    pasajero = test_crear_pasajero()
    assert pasajero["numero_documento"].startswith("ABC")
    
    # 2. Crear avión
    avion = test_crear_avion()
    assert avion["modelo"] == "Boeing 737"
    
    # 3. Crear vuelo
    vuelo = test_crear_vuelo()
    assert vuelo["origen"] == "MAD"
    
    # 4. Crear reserva
    reserva = test_crear_reserva()
    assert reserva["estado"] == "confirmada"
    
    # 5. Verificar que todos los elementos existen
    pasajero_obtenido = test_obtener_pasajero()
    assert pasajero_obtenido["id"] == pasajero["id"]
    
    avion_obtenido = test_obtener_avion()
    assert avion_obtenido["id"] == avion["id"]
    
    vuelo_obtenido = test_obtener_vuelo()
    assert vuelo_obtenido["id"] == vuelo["id"]
    
    reserva_obtenida = test_obtener_reserva()
    assert reserva_obtenida["id"] == reserva["id"]
    
    # 6. Probar endpoints adicionales
    pasajeros = test_listar_pasajeros()
    assert len(pasajeros) > 0
    
    aviones = test_listar_aviones()
    assert len(aviones) > 0
    
    vuelos = test_listar_vuelos()
    assert len(vuelos) > 0
    
    reservas = test_listar_reservas()
    assert len(reservas) > 0
    
    vuelos_fecha = test_buscar_vuelos_por_fecha()
    assert isinstance(vuelos_fecha, list)
    
    vuelos_ruta = test_buscar_vuelos_por_ruta()
    assert isinstance(vuelos_ruta, list)
    
    reservas_pasajero = test_obtener_reservas_por_pasajero()
    assert isinstance(reservas_pasajero, list)
    
    vuelos_avion = test_obtener_vuelos_por_avion()
    assert isinstance(vuelos_avion, list)
    
    # 7. Actualizar todos los elementos
    pasajero_actualizado = test_actualizar_pasajero()
    assert pasajero_actualizado["telefono"] == "987654321"
    
    avion_actualizado = test_actualizar_avion()
    assert avion_actualizado["capacidad_pasajeros"] == 180
    
    vuelo_actualizado = test_actualizar_vuelo()
    assert vuelo_actualizado["estado"] == "retrasado"
    
    reserva_actualizada = test_actualizar_reserva()
    assert reserva_actualizada["estado"] == "cancelada"
    
    # 8. Eliminar todos los elementos en orden inverso
    test_eliminar_reserva()
    test_eliminar_vuelo()
    test_eliminar_avion()
    test_eliminar_pasajero()

if __name__ == "__main__":
    pytest.main(["-v", "test_integration.py"]) 