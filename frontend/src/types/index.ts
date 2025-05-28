export interface User {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
}

export interface Passenger {
  id: number;
  tipo_documento: string;
  numero_documento: string;
  fecha_nacimiento: string;
  nacionalidad: string;
  telefono: string;
  direccion: string;
  usuario_id: number;
  fecha_creacion: string;
  fecha_actualizacion: string | null;
}

export interface Flight {
  id: number;
  numero_vuelo: string;
  fecha_hora_salida: string;
  fecha_hora_llegada: string;
  aeropuerto_origen_id: number;
  aeropuerto_destino_id: number;
  avion_id: number;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface Airport {
  id: number;
  codigo_iata: string;
  nombre: string;
  ciudad: string;
  pais: string;
  latitud: number;
  longitud: number;
  zona_horaria: string;
  estado: string;
  created_at: string;
  updated_at: string;
  terminales: Terminal[];
  pistas: Runway[];
}

export interface Terminal {
  id: number;
  nombre: string;
  capacidad_pasajeros: number;
  estado: string;
  aeropuerto_id: number;
  created_at: string;
  updated_at: string;
}

export interface Runway {
  id: number;
  numero: string;
  longitud_metros: number;
  ancho_metros: number;
  superficie: string;
  estado: string;
  aeropuerto_id: number;
  created_at: string;
  updated_at: string;
}

export interface Reservation {
  id: number;
  pasajero_id: number;
  vuelo_id: number;
  asiento: string;
  precio: number;
  clase: string;
  estado: string;
  codigo_reserva: string;
  fecha_reserva: string;
  fecha_actualizacion: string;
}

export interface Plane {
  id: number;
  matricula: string;
  modelo: string;
  capacidad_pasajeros: number;
  capacidad_carga: number;
  estado: string;
  ultima_revision: string;
  proxima_revision: string;
  created_at: string;
  updated_at: string;
}

export interface Scale {
  id: number;
  vuelo_id: number;
  aeropuerto_id: number;
  numero_escala: number;
  orden: number;
  fecha_hora_llegada: string;
  fecha_hora_salida: string;
  estado: string;
  tipo_escala: string;
  duracion_minutos: number;
  terminal: string;
  puerta: string;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
} 