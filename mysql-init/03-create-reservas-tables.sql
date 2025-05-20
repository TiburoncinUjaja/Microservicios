USE airline_reservas;

-- Tabla de reservas
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pasajero_id INT NOT NULL,
    vuelo_id VARCHAR(20) NOT NULL,
    estado ENUM('PENDIENTE', 'CONFIRMADA', 'CANCELADA', 'COMPLETADA') NOT NULL DEFAULT 'PENDIENTE',
    fecha_reserva TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    precio_total DECIMAL(10,2) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'USD',
    codigo_reserva VARCHAR(10) NOT NULL UNIQUE,
    INDEX idx_pasajero_vuelo (pasajero_id, vuelo_id)
);

-- Tabla de asientos reservados
CREATE TABLE IF NOT EXISTS asientos_reservados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    numero_asiento VARCHAR(10) NOT NULL,
    tipo_asiento ENUM('ECONOMICA', 'EJECUTIVA', 'PRIMERA') NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE,
    UNIQUE KEY unique_asiento_vuelo (reserva_id, numero_asiento)
);

-- Tabla de servicios adicionales
CREATE TABLE IF NOT EXISTS servicios_adicionales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    tipo_servicio ENUM('EQUIPAJE_EXTRA', 'COMIDA_ESPECIAL', 'ASISTENCIA_ESPECIAL', 'SEGURO_VIAJE') NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);

-- Tabla de pagos
CREATE TABLE IF NOT EXISTS pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'USD',
    metodo_pago ENUM('TARJETA', 'TRANSFERENCIA', 'EFECTIVO') NOT NULL,
    estado ENUM('PENDIENTE', 'COMPLETADO', 'RECHAZADO', 'REEMBOLSADO') NOT NULL DEFAULT 'PENDIENTE',
    fecha_pago TIMESTAMP NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
);

-- Tabla de historial de cambios de reserva
CREATE TABLE IF NOT EXISTS historial_cambios_reserva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    reserva_id INT NOT NULL,
    tipo_cambio ENUM('CREACION', 'MODIFICACION', 'CANCELACION', 'CONFIRMACION') NOT NULL,
    descripcion TEXT,
    usuario_id INT,
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (reserva_id) REFERENCES reservas(id) ON DELETE CASCADE
); 