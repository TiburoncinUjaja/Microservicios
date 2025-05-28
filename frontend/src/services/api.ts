import axios from 'axios';
import type { AuthResponse, Passenger, Flight, Airport, Reservation } from '../types';

const BASE_URLS = {
  auth: 'http://localhost:8001',
  passengers: 'http://localhost:8001',
  flights: 'http://localhost:8003',
  airports: 'http://localhost:8005',
  reservations: 'http://localhost:8002',
  planes: 'http://localhost:8004',
  scales: 'http://localhost:8006',
};

const createApi = (baseURL: string) => {
  const api = axios.create({
    baseURL,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  return api;
};

// Auth endpoints
export const authApi = {
  login: async (email: string, password: string): Promise<AuthResponse> => {
    const api = createApi(BASE_URLS.auth);
    const formData = new URLSearchParams();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await api.post<AuthResponse>('/api/v1/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
    return response.data;
  },
};

// Passengers endpoints
export const passengersApi = {
  getAll: async (): Promise<Passenger[]> => {
    const api = createApi(BASE_URLS.passengers);
    const response = await api.get<Passenger[]>('/api/v1/pasajeros');
    return response.data;
  },
  getById: async (id: number): Promise<Passenger> => {
    const api = createApi(BASE_URLS.passengers);
    const response = await api.get<Passenger>(`/api/v1/pasajeros/${id}`);
    return response.data;
  },
  create: async (passenger: Omit<Passenger, 'id'>): Promise<Passenger> => {
    const api = createApi(BASE_URLS.passengers);
    const response = await api.post<Passenger>('/api/v1/pasajeros', passenger);
    return response.data;
  },
  update: async (id: number, passenger: Partial<Passenger>): Promise<Passenger> => {
    const api = createApi(BASE_URLS.passengers);
    const response = await api.put<Passenger>(`/api/v1/pasajeros/${id}`, passenger);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    const api = createApi(BASE_URLS.passengers);
    await api.delete(`/api/v1/pasajeros/${id}`);
  },
};

// Flights endpoints
export const flightsApi = {
  getAll: async (): Promise<Flight[]> => {
    const api = createApi(BASE_URLS.flights);
    const response = await api.get<Flight[]>('/api/v1/vuelos');
    return response.data;
  },
  getById: async (id: number): Promise<Flight> => {
    const api = createApi(BASE_URLS.flights);
    const response = await api.get<Flight>(`/api/v1/vuelos/${id}`);
    return response.data;
  },
  create: async (flight: Omit<Flight, 'id'>): Promise<Flight> => {
    const api = createApi(BASE_URLS.flights);
    const response = await api.post<Flight>('/api/v1/vuelos', flight);
    return response.data;
  },
  update: async (id: number, flight: Partial<Flight>): Promise<Flight> => {
    const api = createApi(BASE_URLS.flights);
    const response = await api.put<Flight>(`/api/v1/vuelos/${id}`, flight);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    const api = createApi(BASE_URLS.flights);
    await api.delete(`/api/v1/vuelos/${id}`);
  },
};

// Airports endpoints
export const airportsApi = {
  getAll: async (): Promise<Airport[]> => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.get<Airport[]>('/api/v1/aeropuertos');
    return response.data;
  },
  getById: async (id: number): Promise<Airport> => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.get<Airport>(`/api/v1/aeropuertos/${id}`);
    return response.data;
  },
  create: async (airport: Omit<Airport, 'id'>): Promise<Airport> => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.post<Airport>('/api/v1/aeropuertos', airport);
    return response.data;
  },
  update: async (id: number, airport: Partial<Airport>): Promise<Airport> => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.put<Airport>(`/api/v1/aeropuertos/${id}`, airport);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    const api = createApi(BASE_URLS.airports);
    await api.delete(`/api/v1/aeropuertos/${id}`);
  },
  getTerminals: async (airportId: number) => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.get(`/api/v1/aeropuertos/${airportId}/terminales`);
    return response.data;
  },
  getRunways: async (airportId: number) => {
    const api = createApi(BASE_URLS.airports);
    const response = await api.get(`/api/v1/aeropuertos/${airportId}/pistas`);
    return response.data;
  },
};

// Reservations endpoints
export const reservationsApi = {
  getAll: async (): Promise<Reservation[]> => {
    const api = createApi(BASE_URLS.reservations);
    const response = await api.get<Reservation[]>('/api/v1/reservas');
    return response.data;
  },
  getById: async (id: number): Promise<Reservation> => {
    const api = createApi(BASE_URLS.reservations);
    const response = await api.get<Reservation>(`/api/v1/reservas/${id}`);
    return response.data;
  },
  getByPassenger: async (passengerId: number): Promise<Reservation[]> => {
    const api = createApi(BASE_URLS.reservations);
    const response = await api.get<Reservation[]>(`/api/v1/reservas/pasajero/${passengerId}`);
    return response.data;
  },
  create: async (reservation: Omit<Reservation, 'id'>): Promise<Reservation> => {
    const api = createApi(BASE_URLS.reservations);
    const response = await api.post<Reservation>('/api/v1/reservas', reservation);
    return response.data;
  },
  update: async (id: number, reservation: Partial<Reservation>): Promise<Reservation> => {
    const api = createApi(BASE_URLS.reservations);
    const response = await api.put<Reservation>(`/api/v1/reservas/${id}`, reservation);
    return response.data;
  },
  delete: async (id: number): Promise<void> => {
    const api = createApi(BASE_URLS.reservations);
    await api.delete(`/api/v1/reservas/${id}`);
  },
};

// Planes endpoints
export const planesApi = {
  getAll: async () => {
    const api = createApi(BASE_URLS.planes);
    const response = await api.get('/api/v1/aviones');
    return response.data;
  },
};

// Scales endpoints
export const scalesApi = {
  getAll: async () => {
    const api = createApi(BASE_URLS.scales);
    const response = await api.get('/api/v1/escalas');
    return response.data;
  },
}; 