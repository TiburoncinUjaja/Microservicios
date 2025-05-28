-- Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS airline_vuelos;
USE airline_vuelos;

-- Tabla de Aeropuertos
CREATE TABLE IF NOT EXISTS aeropuertos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo_iata VARCHAR(3) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    pais VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Aviones
CREATE TABLE IF NOT EXISTS aviones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    matricula VARCHAR(10) UNIQUE NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    capacidad_pasajeros INT NOT NULL,
    estado ENUM('ACTIVO', 'MANTENIMIENTO', 'INACTIVO') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabla de Personal
CREATE TABLE IF NOT EXISTS personal (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero_empleado VARCHAR(10) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    tipo ENUM('PILOTO', 'COPILOTO', 'ASISTENTE') NOT NULL,
    estado ENUM('ACTIVO', 'INACTIVO', 'VACACIONES') NOT NULL DEFAULT 'ACTIVO',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Índices para mejorar el rendimiento
CREATE INDEX idx_aeropuerto_codigo ON aeropuertos(codigo_iata);
CREATE INDEX idx_avion_matricula ON aviones(matricula);
CREATE INDEX idx_personal_numero ON personal(numero_empleado); 