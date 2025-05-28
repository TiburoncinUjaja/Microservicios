#!/bin/bash

# Esperar a que MySQL esté listo
echo "Esperando a que MySQL esté listo..."
while ! nc -z mysql 3306; do
  sleep 1
done
echo "MySQL está listo!"

# Ejecutar script de verificación
echo "Verificando la base de datos..."
python -m app.scripts.verify_data

# Ejecutar script de inserción de datos
echo "Insertando datos de prueba..."
python -m app.scripts.insert_test_data

# Iniciar la aplicación
echo "Iniciando la aplicación..."
python -m app.main

# Ejecutar comando para mostrar los vuelos existentes
echo "Mostrando vuelos existentes..."
docker-compose exec mysql mysql -u root -p1092 -e "USE airline_vuelos; SELECT id, numero_vuelo, estado FROM vuelos;" 