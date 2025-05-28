USE airline_pasajeros;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    rol ENUM('admin', 'usuario') NOT NULL DEFAULT 'usuario',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE
);

-- Tabla de pasajeros
CREATE TABLE IF NOT EXISTS pasajeros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo_documento ENUM('DNI', 'PASAPORTE', 'CE') NOT NULL,
    numero_documento VARCHAR(20) NOT NULL UNIQUE,
    fecha_nacimiento DATE NOT NULL,
    nacionalidad VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    direccion TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Tabla de preferencias de pasajeros
CREATE TABLE IF NOT EXISTS preferencias_pasajeros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pasajero_id INT NOT NULL,
    tipo_asiento ENUM('VENTANA', 'PASILLO', 'CENTRO') NOT NULL,
    comida_especial VARCHAR(100),
    necesidades_especiales TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pasajero_id) REFERENCES pasajeros(id) ON DELETE CASCADE
);

-- Tabla de historial de vuelos
CREATE TABLE IF NOT EXISTS historial_vuelos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pasajero_id INT NOT NULL,
    vuelo_id VARCHAR(20) NOT NULL,
    fecha_vuelo DATE NOT NULL,
    origen VARCHAR(100) NOT NULL,
    destino VARCHAR(100) NOT NULL,
    estado ENUM('COMPLETADO', 'CANCELADO', 'RETRASADO') NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (pasajero_id) REFERENCES pasajeros(id) ON DELETE CASCADE
);

-- Insertar usuario administrador por defecto
INSERT INTO usuarios (email, password_hash, nombre, apellido, rol)
VALUES ('admin@airline.com', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'Admin', 'Sistema', 'admin')
ON DUPLICATE KEY UPDATE id=id; 