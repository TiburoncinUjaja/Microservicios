-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS airline_vuelos;
USE airline_vuelos;

-- Crear la tabla de vuelos
CREATE TABLE IF NOT EXISTS vuelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_vuelo VARCHAR(10) NOT NULL UNIQUE,
    fecha_hora_salida DATETIME NOT NULL,
    fecha_hora_llegada DATETIME NOT NULL,
    aeropuerto_origen_id INT NOT NULL,
    aeropuerto_destino_id INT NOT NULL,
    avion_id INT NOT NULL,
    estado ENUM('PROGRAMADO', 'EN_VUELO', 'COMPLETADO', 'CANCELADO', 'RETRASADO') NOT NULL DEFAULT 'PROGRAMADO',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Limpiar la tabla antes de insertar nuevos datos
TRUNCATE TABLE vuelos;

-- Insertar vuelos de ejemplo
INSERT INTO vuelos (id, numero_vuelo, fecha_hora_salida, fecha_hora_llegada, aeropuerto_origen_id, aeropuerto_destino_id, avion_id, estado) VALUES
(1, 'IB1234', '2024-03-20 10:00:00', '2024-03-20 12:00:00', 1, 2, 1, 'PROGRAMADO'),
(2, 'IB5678', '2024-03-20 14:00:00', '2024-03-20 16:00:00', 2, 1, 1, 'PROGRAMADO'),
(3, 'IB9012', '2024-03-20 18:00:00', '2024-03-20 20:00:00', 1, 3, 2, 'PROGRAMADO');

-- Verificar que los datos se insertaron correctamente
SELECT * FROM vuelos; 