-- Crear base de datos para pasajeros
CREATE DATABASE IF NOT EXISTS airline_pasajeros;
USE airline_pasajeros;

-- Crear base de datos para reservas
CREATE DATABASE IF NOT EXISTS airline_reservas;
USE airline_reservas;

-- Crear usuario y otorgar permisos
CREATE USER IF NOT EXISTS 'airline_user'@'%' IDENTIFIED BY 'airline_password';
GRANT ALL PRIVILEGES ON airline_pasajeros.* TO 'airline_user'@'%';
GRANT ALL PRIVILEGES ON airline_reservas.* TO 'airline_user'@'%';
FLUSH PRIVILEGES; 