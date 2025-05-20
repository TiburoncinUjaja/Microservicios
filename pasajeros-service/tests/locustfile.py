from locust import HttpUser, task, between
import random
import json

class PasajeroServiceUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre peticiones
    
    def on_start(self):
        """Inicialización del usuario - login"""
        # Login para obtener token
        response = self.client.post(
            "/api/v1/auth/login",
            json={
                "email": "test@example.com",
                "password": "testpassword"
            }
        )
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.token = None
            self.headers = {}

    @task(3)
    def get_pasajeros(self):
        """Obtener lista de pasajeros"""
        self.client.get("/api/v1/pasajeros", headers=self.headers)

    @task(2)
    def get_pasajero_by_id(self):
        """Obtener pasajero por ID"""
        pasajero_id = random.randint(1, 100)  # Simulamos IDs existentes
        self.client.get(f"/api/v1/pasajeros/{pasajero_id}", headers=self.headers)

    @task(1)
    def create_pasajero(self):
        """Crear nuevo pasajero"""
        pasajero_data = {
            "nombre": f"Test User {random.randint(1, 1000)}",
            "email": f"test{random.randint(1, 1000)}@example.com",
            "documento_identidad": f"DOC{random.randint(100000, 999999)}",
            "telefono": f"+123456789{random.randint(0, 9)}"
        }
        self.client.post(
            "/api/v1/pasajeros",
            json=pasajero_data,
            headers=self.headers
        )

    @task(1)
    def update_pasajero(self):
        """Actualizar pasajero existente"""
        pasajero_id = random.randint(1, 100)
        update_data = {
            "telefono": f"+123456789{random.randint(0, 9)}"
        }
        self.client.put(
            f"/api/v1/pasajeros/{pasajero_id}",
            json=update_data,
            headers=self.headers
        )

    @task(1)
    def delete_pasajero(self):
        """Eliminar pasajero"""
        pasajero_id = random.randint(1, 100)
        self.client.delete(
            f"/api/v1/pasajeros/{pasajero_id}",
            headers=self.headers
        )

    @task(2)
    def search_pasajeros(self):
        """Buscar pasajeros"""
        query = random.choice(["test", "user", "example", "doc"])
        self.client.get(
            f"/api/v1/pasajeros/search?q={query}",
            headers=self.headers
        )

    @task(1)
    def get_pasajero_reservas(self):
        """Obtener reservas de un pasajero"""
        pasajero_id = random.randint(1, 100)
        self.client.get(
            f"/api/v1/pasajeros/{pasajero_id}/reservas",
            headers=self.headers
        ) 