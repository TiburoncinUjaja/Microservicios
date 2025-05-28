CREATE DATABASE IF NOT EXISTS airline_escalas;
USE airline_escalas;

CREATE TABLE IF NOT EXISTS escalas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vuelo_id INT NOT NULL,
    aeropuerto_id INT NOT NULL,
    numero_escala INT NOT NULL,
    hora_llegada DATETIME NOT NULL,
    hora_salida DATETIME NOT NULL,
    estado ENUM('PROGRAMADA', 'EN_PROGRESO', 'COMPLETADA', 'CANCELADA') NOT NULL DEFAULT 'PROGRAMADA',
    tipo_escala ENUM('TECNICA', 'COMERCIAL') NOT NULL,
    duracion_minutos INT NOT NULL,
    terminal VARCHAR(50),
    puerta VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_vuelo_id (vuelo_id),
    INDEX idx_aeropuerto_id (aeropuerto_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci; 