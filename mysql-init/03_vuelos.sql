-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS airline_vuelos;
USE airline_vuelos;

-- Tabla de Vuelos
CREATE TABLE IF NOT EXISTS vuelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_vuelo VARCHAR(10) UNIQUE NOT NULL,
    fecha_hora_salida DATETIME NOT NULL,
    fecha_hora_llegada DATETIME NOT NULL,
    aeropuerto_origen_id INT NOT NULL,
    aeropuerto_destino_id INT NOT NULL,
    avion_id INT NOT NULL,
    estado ENUM('PROGRAMADO', 'EN_VUELO', 'COMPLETADO', 'CANCELADO', 'RETRASADO') NOT NULL DEFAULT 'PROGRAMADO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_vuelo_aeropuerto_origen FOREIGN KEY (aeropuerto_origen_id) REFERENCES aeropuertos(id),
    CONSTRAINT fk_vuelo_aeropuerto_destino FOREIGN KEY (aeropuerto_destino_id) REFERENCES aeropuertos(id),
    CONSTRAINT fk_vuelo_avion FOREIGN KEY (avion_id) REFERENCES aviones(id)
);

-- Tabla de Tripulación de Vuelo (relación muchos a muchos entre vuelos y personal)
CREATE TABLE IF NOT EXISTS tripulacion_vuelo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vuelo_id INT NOT NULL,
    personal_id INT NOT NULL,
    rol ENUM('PILOTO', 'COPILOTO', 'ASISTENTE') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_tripulacion_vuelo FOREIGN KEY (vuelo_id) REFERENCES vuelos(id),
    CONSTRAINT fk_tripulacion_personal FOREIGN KEY (personal_id) REFERENCES personal(id),
    CONSTRAINT unique_tripulacion_vuelo UNIQUE (vuelo_id, personal_id)
);

-- Tabla de Escalas
CREATE TABLE IF NOT EXISTS escalas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    vuelo_id INT NOT NULL,
    aeropuerto_id INT NOT NULL,
    orden INT NOT NULL,
    fecha_hora_llegada DATETIME NOT NULL,
    fecha_hora_salida DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_escala_vuelo FOREIGN KEY (vuelo_id) REFERENCES vuelos(id),
    CONSTRAINT fk_escala_aeropuerto FOREIGN KEY (aeropuerto_id) REFERENCES aeropuertos(id),
    CONSTRAINT unique_escala_orden UNIQUE (vuelo_id, orden)
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_vuelo_numero ON vuelos(numero_vuelo);
CREATE INDEX idx_vuelo_fechas ON vuelos(fecha_hora_salida, fecha_hora_llegada);
CREATE INDEX idx_tripulacion_vuelo ON tripulacion_vuelo(vuelo_id);
CREATE INDEX idx_tripulacion_personal ON tripulacion_vuelo(personal_id);
CREATE INDEX idx_escalas_vuelo ON escalas(vuelo_id);
CREATE INDEX idx_escalas_aeropuerto ON escalas(aeropuerto_id); 