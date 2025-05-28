-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS airline_reservas;

-- Usar la base de datos
USE airline_reservas;

-- Crear la tabla de reservas
DROP TABLE IF EXISTS reservas;
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pasajero_id INT NOT NULL,
    vuelo_id INT NOT NULL,
    asiento VARCHAR(10) NOT NULL,
    estado ENUM('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA') DEFAULT 'PENDIENTE',
    fecha_reserva DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    codigo_reserva VARCHAR(10) UNIQUE,
    precio INT NOT NULL,
    clase VARCHAR(20) NOT NULL,
    INDEX idx_pasajero (pasajero_id),
    INDEX idx_vuelo (vuelo_id),
    INDEX idx_codigo_reserva (codigo_reserva)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 