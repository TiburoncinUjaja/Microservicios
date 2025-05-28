import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SECTIONS = [
  { key: 'aviones', label: 'Aviones', icon: 'bi-airplane' },
  { key: 'aeropuertos', label: 'Aeropuertos', icon: 'bi-geo-alt' },
  { key: 'vuelos', label: 'Vuelos', icon: 'bi-airplane-fill' },
  { key: 'escalas', label: 'Escalas', icon: 'bi-diagram-3' },
  { key: 'pasajeros', label: 'Pasajeros', icon: 'bi-people' },
  { key: 'reservas', label: 'Reservas', icon: 'bi-journal-bookmark' },
];

// Utilidad para limpiar formularios
const emptyPlane = {
  matricula: '', modelo: '', capacidad_pasajeros: '', capacidad_carga: '', estado: 'ACTIVO', ultima_revision: '', proxima_revision: ''
};
const emptyAirport = {
  nombre: '', codigo_iata: '', ciudad: '', pais: '', latitud: '', longitud: '', zona_horaria: '', estado: 'ACTIVO'
};
const emptyRunway = {
  numero: '', longitud_metros: '', ancho_metros: '', superficie: '', estado: 'ACTIVO'
};
const emptyTerminal = {
  nombre: '', capacidad_pasajeros: '', estado: 'ACTIVO'
};
const emptyPassenger = {
  tipo_documento: '', numero_documento: '', fecha_nacimiento: '', nacionalidad: '', telefono: '', direccion: '', usuario_id: ''
};
const emptyReservation = {
  pasajero_id: '', vuelo_id: '', asiento: '', precio: '', clase: '', estado: 'PENDIENTE'
};

// Interfaces para el tipado
interface Plane {
  id: number;
  matricula: string;
  modelo: string;
  capacidad_pasajeros: number;
  capacidad_carga: number;
  estado: string;
  ultima_revision: string;
  proxima_revision: string;
}

interface Airport {
  id: number;
  nombre: string;
  codigo_iata: string;
  ciudad: string;
  pais: string;
  estado: string;
}

interface Terminal {
  id: number;
  nombre: string;
  capacidad_pasajeros: number;
  estado: string;
}

interface Vuelo {
  id: number;
  numero_vuelo: string;
  fecha_hora_salida: string;
  fecha_hora_llegada: string;
  aeropuerto_origen_id: number;
  aeropuerto_destino_id: number;
  avion_id: number;
  estado: string;
}

interface Escala {
  id: number;
  vuelo_id: number;
  aeropuerto_id: number;
  numero_escala: number;
  orden: number;
  fecha_hora_llegada: string;
  fecha_hora_salida: string;
  tipo_escala: string;
  duracion_minutos: number;
  terminal: string;
  puerta: string;
}

interface Passenger {
  id: number;
  tipo_documento: string;
  numero_documento: string;
  fecha_nacimiento: string;
  nacionalidad: string;
  telefono: string;
  direccion: string;
  usuario_id: number;
}

export default function MenuPage() {
  const navigate = useNavigate();
  const [activeSection, setActiveSection] = useState('aviones');

  // --- Aviones ---
  const [planes, setPlanes] = useState<Plane[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [showPlaneModal, setShowPlaneModal] = useState(false);
  const [editingPlane, setEditingPlane] = useState<any>(null);
  const [planeForm, setPlaneForm] = useState<any>(emptyPlane);
  const [planeSubmitting, setPlaneSubmitting] = useState(false);
  const [planeDeleteId, setPlaneDeleteId] = useState<number|null>(null);

  // --- Aeropuertos ---
  const [airports, setAirports] = useState<Airport[]>([]);
  const [airportLoading, setAirportLoading] = useState(false);
  const [airportError, setAirportError] = useState('');
  const [showAirportModal, setShowAirportModal] = useState(false);
  const [editingAirport, setEditingAirport] = useState<any>(null);
  const [airportForm, setAirportForm] = useState<any>(emptyAirport);
  const [airportSubmitting, setAirportSubmitting] = useState(false);
  const [airportDeleteId, setAirportDeleteId] = useState<number|null>(null);
  const [selectedAirport, setSelectedAirport] = useState<any>(null);
  const [airportTab, setAirportTab] = useState<'pistas' | 'terminales'>('pistas');

  // --- Pistas y Terminales ---
  const [runways, setRunways] = useState([]);
  const [terminals, setTerminals] = useState<Terminal[]>([]);
  const [runwaysLoading, setRunwaysLoading] = useState(false);
  const [terminalsLoading, setTerminalsLoading] = useState(false);
  // Pistas
  const [showRunwayModal, setShowRunwayModal] = useState(false);
  const [editingRunway, setEditingRunway] = useState<any>(null);
  const [runwayForm, setRunwayForm] = useState<any>(emptyRunway);
  const [runwaySubmitting, setRunwaySubmitting] = useState(false);
  const [runwayDeleteId, setRunwayDeleteId] = useState<number|null>(null);
  // Terminales
  const [showTerminalModal, setShowTerminalModal] = useState(false);
  const [editingTerminal, setEditingTerminal] = useState<any>(null);
  const [terminalForm, setTerminalForm] = useState<any>(emptyTerminal);
  const [terminalSubmitting, setTerminalSubmitting] = useState(false);
  const [terminalDeleteId, setTerminalDeleteId] = useState<number|null>(null);

  // --- Pasajeros ---
  const [passengers, setPassengers] = useState<Passenger[]>([]);
  const [passengersLoading, setPassengersLoading] = useState(false);
  const [passengersError, setPassengersError] = useState('');
  const [showPassengerModal, setShowPassengerModal] = useState(false);
  const [editingPassenger, setEditingPassenger] = useState<any>(null);
  const [passengerForm, setPassengerForm] = useState<any>(emptyPassenger);
  const [passengerSubmitting, setPassengerSubmitting] = useState(false);
  const [passengerDeleteId, setPassengerDeleteId] = useState<number|null>(null);

  // --- Reservas ---
  const [reservations, setReservations] = useState([]);
  const [reservationsLoading, setReservationsLoading] = useState(false);
  const [reservationsError, setReservationsError] = useState('');
  const [showReservationModal, setShowReservationModal] = useState(false);
  const [editingReservation, setEditingReservation] = useState<any>(null);
  const [reservationForm, setReservationForm] = useState<any>(emptyReservation);
  const [reservationSubmitting, setReservationSubmitting] = useState(false);
  const [reservationDeleteId, setReservationDeleteId] = useState<number|null>(null);

  // Agregar estados para vuelos
  const [vuelos, setVuelos] = useState<Vuelo[]>([]);
  const [vuelosLoading, setVuelosLoading] = useState(false);
  const [vuelosError, setVuelosError] = useState('');
  const [showVueloModal, setShowVueloModal] = useState(false);
  const [editingVuelo, setEditingVuelo] = useState<any>(null);
  const [vueloForm, setVueloForm] = useState<any>({
    numero_vuelo: '',
    fecha_hora_salida: '',
    fecha_hora_llegada: '',
    aeropuerto_origen_id: '',
    aeropuerto_destino_id: '',
    avion_id: '',
    estado: 'PROGRAMADO'
  });
  const [vueloSubmitting, setVueloSubmitting] = useState(false);
  const [vueloDeleteId, setVueloDeleteId] = useState<number|null>(null);

  // Agregar estados para escalas
  const [escalas, setEscalas] = useState<Escala[]>([]);
  const [escalasLoading, setEscalasLoading] = useState(false);
  const [escalasError, setEscalasError] = useState('');
  const [showEscalaModal, setShowEscalaModal] = useState(false);
  const [editingEscala, setEditingEscala] = useState<any>(null);
  const [escalaForm, setEscalaForm] = useState<any>({
    vuelo_id: '',
    aeropuerto_id: '',
    numero_escala: '',
    orden: '',
    fecha_hora_llegada: '',
    fecha_hora_salida: '',
    tipo_escala: 'TECNICA',
    duracion_minutos: '',
    terminal: '',
    puerta: ''
  });
  const [escalaSubmitting, setEscalaSubmitting] = useState(false);
  const [escalaDeleteId, setEscalaDeleteId] = useState<number|null>(null);
  const [terminalesAeropuerto, setTerminalesAeropuerto] = useState<Terminal[]>([]);

  // Función para cargar terminales del aeropuerto
  const fetchTerminalesAeropuerto = async (aeropuertoId: number) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${aeropuertoId}/terminales`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener terminales');
      const terminales = await res.json();
      setTerminalesAeropuerto(terminales);
    } catch (err: any) {
      console.error('Error al cargar terminales:', err);
      setTerminalesAeropuerto([]);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      navigate('/login');
    }
  }, [navigate]);

  // --- Carga de datos por sección ---
  useEffect(() => {
    if (activeSection === 'aviones') fetchPlanes();
    if (activeSection === 'aeropuertos') { fetchAirports(); setSelectedAirport(null); }
    if (activeSection === 'pasajeros') fetchPassengers();
    if (activeSection === 'reservas') fetchReservations();
    if (activeSection === 'vuelos') fetchVuelos();
    if (activeSection === 'escalas') fetchEscalas();
  }, [activeSection]);

  // --- Aeropuerto seleccionado: cargar pistas y terminales ---
  useEffect(() => {
    if (selectedAirport) {
      fetchRunways(selectedAirport.id);
      fetchTerminals(selectedAirport.id);
    }
  }, [selectedAirport]);

  // --- CRUD Aviones ---
  const fetchPlanes = async () => {
    setLoading(true); setError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8004/api/v1/aviones/', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener aviones');
      setPlanes(await res.json());
    } catch (err: any) { setError(err.message || 'Error al obtener aviones'); }
    finally { setLoading(false); }
  };
  const handlePlaneForm = (e: any) => setPlaneForm({ ...planeForm, [e.target.name]: e.target.value });
  const showModal = (modalId: string) => {
    const modal = document.getElementById(modalId);
    if (modal) {
      const bsModal = new (window as any).bootstrap.Modal(modal);
      bsModal.show();
    }
  };
  const hideModal = (modalId: string) => {
    const modal = document.getElementById(modalId);
    if (modal) {
      const bsModal = (window as any).bootstrap.Modal.getInstance(modal);
      if (bsModal) bsModal.hide();
    }
  };
  const openNewPlane = () => { 
    setEditingPlane(null); 
    setPlaneForm(emptyPlane); 
    showModal('planeModal'); 
  };
  const openEditPlane = (plane: any) => { 
    setEditingPlane(plane); 
    setPlaneForm(plane); 
    showModal('planeModal'); 
  };
  const confirmDeletePlane = (id: number) => { 
    setPlaneDeleteId(id); 
    showModal('deletePlaneModal'); 
  };
  const submitPlane = async (e: any) => {
    e.preventDefault(); 
    setPlaneSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingPlane ? 'PUT' : 'POST';
      const url = editingPlane ? `http://localhost:8004/api/v1/aviones/${editingPlane.id}` : 'http://localhost:8004/api/v1/aviones/';
      
      // Validaciones de campos requeridos
      if (!planeForm.matricula?.trim()) {
        throw new Error('La matrícula es obligatoria');
      }
      if (!planeForm.modelo?.trim()) {
        throw new Error('El modelo es obligatorio');
      }
      if (!planeForm.capacidad_pasajeros?.toString().trim()) {
        throw new Error('La capacidad de pasajeros es obligatoria');
      }
      if (!planeForm.capacidad_carga?.toString().trim()) {
        throw new Error('La capacidad de carga es obligatoria');
      }
      if (!planeForm.ultima_revision?.trim()) {
        throw new Error('La fecha de última revisión es obligatoria');
      }
      if (!planeForm.proxima_revision?.trim()) {
        throw new Error('La fecha de próxima revisión es obligatoria');
      }

      // Validación de matrícula (formato común: EC-ABC o N12345)
      const matriculaRegex = /^[A-Z]{2}-[A-Z]{3}$|^[A-Z]\d{4,5}$/;
      if (!matriculaRegex.test(planeForm.matricula)) {
        throw new Error('La matrícula debe tener el formato EC-ABC o N12345');
      }

      // Validación de capacidades
      const capacidadPasajeros = parseInt(planeForm.capacidad_pasajeros);
      const capacidadCarga = parseInt(planeForm.capacidad_carga);

      if (isNaN(capacidadPasajeros)) {
        throw new Error('La capacidad de pasajeros debe ser un número válido');
      }
      if (isNaN(capacidadCarga)) {
        throw new Error('La capacidad de carga debe ser un número válido');
      }

      if (capacidadPasajeros <= 0) {
        throw new Error('La capacidad de pasajeros debe ser mayor a 0');
      }
      if (capacidadCarga <= 0) {
        throw new Error('La capacidad de carga debe ser mayor a 0');
      }

      if (capacidadPasajeros > 1000) {
        throw new Error('La capacidad de pasajeros no puede ser mayor a 1000');
      }
      if (capacidadCarga > 100000) {
        throw new Error('La capacidad de carga no puede ser mayor a 100,000 kg');
      }

      // Validación de fechas
      const ultimaRevision = new Date(planeForm.ultima_revision);
      const proximaRevision = new Date(planeForm.proxima_revision);
      const hoy = new Date();

      if (isNaN(ultimaRevision.getTime())) {
        throw new Error('La fecha de última revisión no es válida');
      }
      if (isNaN(proximaRevision.getTime())) {
        throw new Error('La fecha de próxima revisión no es válida');
      }

      if (ultimaRevision > hoy) {
        throw new Error('La fecha de última revisión no puede ser futura');
      }
      if (proximaRevision < hoy) {
        throw new Error('La fecha de próxima revisión debe ser futura');
      }
      if (proximaRevision < ultimaRevision) {
        throw new Error('La fecha de próxima revisión debe ser posterior a la última revisión');
      }

      // Validación de estado
      const estadosValidos = ['ACTIVO', 'INACTIVO', 'MANTENIMIENTO'];
      if (!estadosValidos.includes(planeForm.estado)) {
        throw new Error('El estado debe ser ACTIVO, INACTIVO o MANTENIMIENTO');
      }

      // Formatear las fechas al formato ISO 8601
      const formData = {
        ...planeForm,
        capacidad_pasajeros: capacidadPasajeros,
        capacidad_carga: capacidadCarga,
        ultima_revision: `${planeForm.ultima_revision}T00:00:00`,
        proxima_revision: `${planeForm.proxima_revision}T00:00:00`
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('matrícula')) {
            throw new Error('Ya existe un avión con esa matrícula');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('El avión no fue encontrado');
        }
        if (res.status === 422) {
          throw new Error('Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar avión');
      }

      hideModal('planeModal');
      fetchPlanes();
    } catch (err: any) { 
      alert(`Error: ${err.message}`); 
    } finally { 
      setPlaneSubmitting(false); 
    }
  };
  const deletePlane = async () => {
    if (!planeDeleteId) return;
    setPlaneSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8004/api/v1/aviones/${planeDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar avión');
      hideModal('deletePlaneModal');
      setPlaneDeleteId(null); 
      fetchPlanes();
    } catch (err: any) { alert(err.message); }
    finally { setPlaneSubmitting(false); }
  };

  // --- CRUD Aeropuertos ---
  const fetchAirports = async () => {
    setAirportLoading(true); setAirportError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8005/api/v1/aeropuertos', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener aeropuertos');
      setAirports(await res.json());
    } catch (err: any) { setAirportError(err.message || 'Error al obtener aeropuertos'); }
    finally { setAirportLoading(false); }
  };
  const handleAirportForm = (e: any) => setAirportForm({ ...airportForm, [e.target.name]: e.target.value });
  const openNewAirport = () => { 
    setEditingAirport(null); 
    setAirportForm(emptyAirport); 
    showModal('airportModal'); 
  };
  const openEditAirport = (airport: any) => { 
    setEditingAirport(airport); 
    setAirportForm(airport); 
    showModal('airportModal'); 
  };
  const confirmDeleteAirport = (id: number) => { 
    setAirportDeleteId(id); 
    showModal('deleteAirportModal'); 
  };
  const submitAirport = async (e: any) => {
    e.preventDefault();
    setAirportSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingAirport ? 'PUT' : 'POST';
      const url = editingAirport ? `http://localhost:8005/api/v1/aeropuertos/${editingAirport.id}` : 'http://localhost:8005/api/v1/aeropuertos';
      
      // Validaciones de campos requeridos
      if (!airportForm.codigo_iata?.trim()) {
        throw new Error('El código IATA es obligatorio');
      }
      if (!airportForm.nombre?.trim()) {
        throw new Error('El nombre del aeropuerto es obligatorio');
      }
      if (!airportForm.ciudad?.trim()) {
        throw new Error('La ciudad es obligatoria');
      }
      if (!airportForm.pais?.trim()) {
        throw new Error('El país es obligatorio');
      }
      if (!airportForm.zona_horaria?.trim()) {
        throw new Error('La zona horaria es obligatoria');
      }

      // Validación del código IATA
      if (!/^[A-Z]{3}$/.test(airportForm.codigo_iata)) {
        throw new Error('El código IATA debe ser exactamente 3 letras mayúsculas');
      }

      // Validaciones de coordenadas
      if (!airportForm.latitud?.trim()) {
        throw new Error('La latitud es obligatoria');
      }
      if (!airportForm.longitud?.trim()) {
        throw new Error('La longitud es obligatoria');
      }

      const latitud = parseFloat(airportForm.latitud);
      const longitud = parseFloat(airportForm.longitud);

      if (isNaN(latitud)) {
        throw new Error('La latitud debe ser un número válido');
      }
      if (isNaN(longitud)) {
        throw new Error('La longitud debe ser un número válido');
      }

      if (latitud < -90 || latitud > 90) {
        throw new Error('La latitud debe estar entre -90 y 90 grados');
      }
      if (longitud < -180 || longitud > 180) {
        throw new Error('La longitud debe estar entre -180 y 180 grados');
      }

      // Validación de zona horaria
      try {
        Intl.DateTimeFormat(undefined, { timeZone: airportForm.zona_horaria });
      } catch (error) {
        throw new Error('La zona horaria no es válida. Use el formato: Continente/Ciudad (ej: America/Bogota)');
      }

      const formData = {
        ...airportForm,
        latitud,
        longitud
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });
      
      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('código IATA')) {
            throw new Error('Ya existe un aeropuerto con ese código IATA');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('El aeropuerto no fue encontrado');
        }
        if (res.status === 422) {
          throw new Error('Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar aeropuerto');
      }
      
      hideModal('airportModal');
      fetchAirports();
    } catch (err: any) { 
      // Mostrar el mensaje de error en un alert más visible
      alert(`Error: ${err.message}`);
    } finally { 
      setAirportSubmitting(false); 
    }
  };
  const deleteAirport = async () => {
    if (!airportDeleteId) return;
    setAirportSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${airportDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar aeropuerto');
      hideModal('deleteAirportModal');
      setAirportDeleteId(null); 
      fetchAirports();
    } catch (err: any) { alert(err.message); }
    finally { setAirportSubmitting(false); }
  };

  // --- CRUD Pistas ---
  const fetchRunways = async (airportId: number) => {
    setRunwaysLoading(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${airportId}/pistas`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener pistas');
      setRunways(await res.json());
    } catch {
      setRunways([]);
    } finally {
      setRunwaysLoading(false);
    }
  };

  // --- CRUD Terminales ---
  const fetchTerminals = async (airportId: number) => {
    setTerminalsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${airportId}/terminales`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener terminales');
      setTerminals(await res.json());
    } catch {
      setTerminals([]);
    } finally {
      setTerminalsLoading(false);
    }
  };

  // --- CRUD Pasajeros ---
  const fetchPassengers = async () => {
    setPassengersLoading(true); setPassengersError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8001/api/v1/pasajeros', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener pasajeros');
      setPassengers(await res.json());
    } catch (err: any) { setPassengersError(err.message || 'Error al obtener pasajeros'); }
    finally { setPassengersLoading(false); }
  };
  const handlePassengerForm = (e: any) => setPassengerForm({ ...passengerForm, [e.target.name]: e.target.value });
  const openNewPassenger = () => { 
    setEditingPassenger(null); 
    setPassengerForm(emptyPassenger); 
    showModal('passengerModal'); 
  };
  const openEditPassenger = (p: any) => { 
    setEditingPassenger(p); 
    setPassengerForm(p); 
    showModal('passengerModal'); 
  };
  const confirmDeletePassenger = (id: number) => { 
    setPassengerDeleteId(id); 
    showModal('deletePassengerModal'); 
  };
  const submitPassenger = async (e: any) => {
    e.preventDefault(); 
    setPassengerSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingPassenger ? 'PUT' : 'POST';
      const url = editingPassenger ? `http://localhost:8001/api/v1/pasajeros/${editingPassenger.id}` : 'http://localhost:8001/api/v1/pasajeros';
      
      // Validaciones de campos requeridos
      if (!passengerForm.tipo_documento?.trim()) {
        throw new Error('El tipo de documento es obligatorio');
      }
      if (!passengerForm.numero_documento?.trim()) {
        throw new Error('El número de documento es obligatorio');
      }
      if (!passengerForm.fecha_nacimiento?.trim()) {
        throw new Error('La fecha de nacimiento es obligatoria');
      }
      if (!passengerForm.nacionalidad?.trim()) {
        throw new Error('La nacionalidad es obligatoria');
      }
      if (!passengerForm.telefono?.trim()) {
        throw new Error('El teléfono es obligatorio');
      }
      if (!passengerForm.direccion?.trim()) {
        throw new Error('La dirección es obligatoria');
      }

      // Validación de tipo de documento
      const tiposDocumentoValidos = ['DNI', 'PASAPORTE', 'CE'];
      if (!tiposDocumentoValidos.includes(passengerForm.tipo_documento)) {
        throw new Error('El tipo de documento debe ser DNI, PASAPORTE o CE');
      }

      // Validación de número de documento según tipo
      if (passengerForm.tipo_documento === 'DNI') {
        if (!/^\d{8}[A-Z]$/.test(passengerForm.numero_documento)) {
          throw new Error('El DNI debe tener 8 números seguidos de una letra mayúscula');
        }
      } else if (passengerForm.tipo_documento === 'PASAPORTE') {
        if (!/^[A-Z0-9]{8,12}$/.test(passengerForm.numero_documento)) {
          throw new Error('El pasaporte debe tener entre 8 y 12 caracteres alfanuméricos');
        }
      } else if (passengerForm.tipo_documento === 'CE') {
        if (!/^[A-Z0-9]{8,12}$/.test(passengerForm.numero_documento)) {
          throw new Error('El CE debe tener entre 8 y 12 caracteres alfanuméricos');
        }
      }

      // Validación de fecha de nacimiento
      const fechaNacimiento = new Date(passengerForm.fecha_nacimiento);
      const hoy = new Date();

      if (isNaN(fechaNacimiento.getTime())) {
        throw new Error('La fecha de nacimiento no es válida');
      }
      if (fechaNacimiento > hoy) {
        throw new Error('La fecha de nacimiento no puede ser futura');
      }

      // Validación de teléfono
      if (!/^\+?[\d\s-]{8,15}$/.test(passengerForm.telefono)) {
        throw new Error('El teléfono debe tener entre 8 y 15 dígitos y puede incluir +, espacios o guiones');
      }

      // Validación de dirección
      if (passengerForm.direccion.length < 5) {
        throw new Error('La dirección debe tener al menos 5 caracteres');
      }
      if (passengerForm.direccion.length > 200) {
        throw new Error('La dirección no puede tener más de 200 caracteres');
      }

      // Validación de nacionalidad
      if (passengerForm.nacionalidad.length < 2) {
        throw new Error('La nacionalidad debe tener al menos 2 caracteres');
      }
      if (passengerForm.nacionalidad.length > 50) {
        throw new Error('La nacionalidad no puede tener más de 50 caracteres');
      }

      // Asegurar que usuario_id sea un número
      const formData = {
        ...passengerForm,
        usuario_id: parseInt(passengerForm.usuario_id) || 1, // Si no hay usuario_id, usar 1 por defecto
        fecha_nacimiento: passengerForm.fecha_nacimiento
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('número de documento')) {
            throw new Error('Ya existe un pasajero con ese número de documento');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('El pasajero no fue encontrado');
        }
        if (res.status === 422) {
          if (errorData.detail?.includes('usuario_id')) {
            throw new Error('El ID de usuario no es válido o no existe');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar pasajero');
      }

      hideModal('passengerModal');
      fetchPassengers();
    } catch (err: any) { 
      alert(`Error: ${err.message}`); 
    } finally { 
      setPassengerSubmitting(false); 
    }
  };
  const deletePassenger = async () => {
    if (!passengerDeleteId) return;
    setPassengerSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8001/api/v1/pasajeros/${passengerDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar pasajero');
      hideModal('deletePassengerModal');
      setPassengerDeleteId(null); 
      fetchPassengers();
    } catch (err: any) { alert(err.message); }
    finally { setPassengerSubmitting(false); }
  };

  // --- CRUD Reservas ---
  const fetchReservations = async () => {
    setReservationsLoading(true); setReservationsError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8002/api/v1/reservas', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener reservas');
      setReservations(await res.json());
    } catch (err: any) { setReservationsError(err.message || 'Error al obtener reservas'); }
    finally { setReservationsLoading(false); }
  };
  const handleReservationForm = (e: any) => setReservationForm({ ...reservationForm, [e.target.name]: e.target.value });
  const openNewReservation = () => { 
    setEditingReservation(null); 
    setReservationForm(emptyReservation); 
    showModal('reservationModal'); 
  };
  const openEditReservation = (r: any) => { 
    setEditingReservation(r); 
    setReservationForm(r); 
    showModal('reservationModal'); 
  };
  const confirmDeleteReservation = (id: number) => { 
    setReservationDeleteId(id); 
    showModal('deleteReservationModal'); 
  };
  const submitReservation = async (e: any) => {
    e.preventDefault(); 
    setReservationSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingReservation ? 'PUT' : 'POST';
      const url = editingReservation ? `http://localhost:8002/api/v1/reservas/${editingReservation.id}` : 'http://localhost:8002/api/v1/reservas';
      
      // Validaciones de campos requeridos
      if (!reservationForm.pasajero_id?.toString().trim()) {
        throw new Error('Debe seleccionar un pasajero');
      }
      if (!reservationForm.vuelo_id?.toString().trim()) {
        throw new Error('Debe seleccionar un vuelo');
      }
      if (!reservationForm.asiento?.trim()) {
        throw new Error('El asiento es obligatorio');
      }
      if (!reservationForm.precio?.toString().trim()) {
        throw new Error('El precio es obligatorio');
      }
      if (!reservationForm.clase?.trim()) {
        throw new Error('La clase es obligatoria');
      }

      // Validación de asiento
      const asientoRegex = /^[0-9]{1,2}[A-F]$/;
      if (!asientoRegex.test(reservationForm.asiento)) {
        throw new Error('El asiento debe tener el formato: número (1-99) seguido de una letra (A-F)');
      }

      // Validación de precio
      const precio = parseFloat(reservationForm.precio);
      if (isNaN(precio)) {
        throw new Error('El precio debe ser un número válido');
      }
      if (precio <= 0) {
        throw new Error('El precio debe ser mayor a 0');
      }

      // Validación de clase
      const clasesValidas = ['ECONOMICA', 'EJECUTIVA', 'PRIMERA'];
      if (!clasesValidas.includes(reservationForm.clase)) {
        throw new Error('La clase debe ser ECONOMICA, EJECUTIVA o PRIMERA');
      }

      // Validación de estado
      const estadosValidos = ['PENDIENTE', 'CONFIRMADA', 'CANCELADA'];
      if (!estadosValidos.includes(reservationForm.estado)) {
        throw new Error('El estado debe ser PENDIENTE, CONFIRMADA o CANCELADA');
      }

      // Verificar que el pasajero existe
      const pasajeroExiste = passengers.some(p => p.id === parseInt(reservationForm.pasajero_id));
      if (!pasajeroExiste) {
        throw new Error('El pasajero seleccionado no existe');
      }

      // Verificar que el vuelo existe y está activo
      const vueloExiste = vuelos.some(v => v.id === parseInt(reservationForm.vuelo_id));
      if (!vueloExiste) {
        throw new Error('El vuelo seleccionado no existe o no está activo');
      }

      const formData = {
        ...reservationForm,
        pasajero_id: parseInt(reservationForm.pasajero_id),
        vuelo_id: parseInt(reservationForm.vuelo_id),
        precio: precio
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('asiento')) {
            throw new Error('El asiento ya está ocupado en este vuelo');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('La reserva no fue encontrada');
        }
        if (res.status === 422) {
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar reserva');
      }

      hideModal('reservationModal');
      fetchReservations();
    } catch (err: any) { 
      alert(`Error: ${err.message}`); 
    } finally { 
      setReservationSubmitting(false); 
    }
  };
  const deleteReservation = async () => {
    if (!reservationDeleteId) return;
    setReservationSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8002/api/v1/reservas/${reservationDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar reserva');
      hideModal('deleteReservationModal');
      setReservationDeleteId(null); 
      fetchReservations();
    } catch (err: any) { alert(err.message); }
    finally { setReservationSubmitting(false); }
  };

  // Función para cargar vuelos
  const fetchVuelos = async () => {
    setVuelosLoading(true);
    setVuelosError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8003/api/v1/vuelos', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener vuelos');
      setVuelos(await res.json());
    } catch (err: any) { 
      setVuelosError(err.message || 'Error al obtener vuelos'); 
    } finally { 
      setVuelosLoading(false); 
    }
  };

  // Cargar vuelos cuando se selecciona la sección
  useEffect(() => {
    if (activeSection === 'vuelos') {
      fetchVuelos();
    }
  }, [activeSection]);

  const handleVueloForm = (e: any) => setVueloForm({ ...vueloForm, [e.target.name]: e.target.value });

  const openNewVuelo = () => { 
    setEditingVuelo(null); 
    setVueloForm({
      numero_vuelo: '',
      fecha_hora_salida: '',
      fecha_hora_llegada: '',
      aeropuerto_origen_id: '',
      aeropuerto_destino_id: '',
      avion_id: '',
      estado: 'PROGRAMADO'
    }); 
    showModal('vueloModal'); 
  };

  const openEditVuelo = (vuelo: any) => { 
    setEditingVuelo(vuelo); 
    setVueloForm(vuelo); 
    showModal('vueloModal'); 
  };

  const confirmDeleteVuelo = (id: number) => { 
    setVueloDeleteId(id); 
    showModal('deleteVueloModal'); 
  };

  const submitVuelo = async (e: any) => {
    e.preventDefault(); 
    setVueloSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingVuelo ? 'PUT' : 'POST';
      const url = editingVuelo ? `http://localhost:8003/api/v1/vuelos/${editingVuelo.id}` : 'http://localhost:8003/api/v1/vuelos';
      
      // Validaciones de campos requeridos
      if (!vueloForm.numero_vuelo?.trim()) {
        throw new Error('El número de vuelo es obligatorio');
      }
      if (!vueloForm.fecha_hora_salida?.trim()) {
        throw new Error('La fecha y hora de salida es obligatoria');
      }
      if (!vueloForm.fecha_hora_llegada?.trim()) {
        throw new Error('La fecha y hora de llegada es obligatoria');
      }
      if (!vueloForm.aeropuerto_origen_id?.toString().trim()) {
        throw new Error('Debe seleccionar un aeropuerto de origen');
      }
      if (!vueloForm.aeropuerto_destino_id?.toString().trim()) {
        throw new Error('Debe seleccionar un aeropuerto de destino');
      }
      if (!vueloForm.avion_id?.toString().trim()) {
        throw new Error('Debe seleccionar un avión');
      }

      // Validación de número de vuelo (formato: 2 letras + 4 números)
      const numeroVueloRegex = /^[A-Z]{2}\d{4}$/;
      if (!numeroVueloRegex.test(vueloForm.numero_vuelo)) {
        throw new Error('El número de vuelo debe tener el formato: 2 letras seguidas de 4 números (ej: IB1234)');
      }

      // Validación de fechas
      const fechaSalida = new Date(vueloForm.fecha_hora_salida);
      const fechaLlegada = new Date(vueloForm.fecha_hora_llegada);
      const ahora = new Date();

      if (isNaN(fechaSalida.getTime())) {
        throw new Error('La fecha y hora de salida no es válida');
      }
      if (isNaN(fechaLlegada.getTime())) {
        throw new Error('La fecha y hora de llegada no es válida');
      }

      // Ajustar las fechas para comparación (ignorar milisegundos)
      const fechaSalidaAjustada = new Date(fechaSalida.getFullYear(), fechaSalida.getMonth(), fechaSalida.getDate(), fechaSalida.getHours(), fechaSalida.getMinutes());
      const fechaLlegadaAjustada = new Date(fechaLlegada.getFullYear(), fechaLlegada.getMonth(), fechaLlegada.getDate(), fechaLlegada.getHours(), fechaLlegada.getMinutes());
      const ahoraAjustado = new Date(ahora.getFullYear(), ahora.getMonth(), ahora.getDate(), ahora.getHours(), ahora.getMinutes());

      // Solo validar que la fecha de salida no sea en el pasado si es un nuevo vuelo
      if (!editingVuelo && fechaSalidaAjustada < ahoraAjustado) {
        throw new Error('La fecha y hora de salida no puede ser en el pasado');
      }

      // Validar que la llegada sea después de la salida
      if (fechaLlegadaAjustada <= fechaSalidaAjustada) {
        throw new Error('La fecha y hora de llegada debe ser posterior a la de salida');
      }

      // Validar que el vuelo no dure más de 24 horas
      const duracionVuelo = fechaLlegadaAjustada.getTime() - fechaSalidaAjustada.getTime();
      const duracionMaxima = 24 * 60 * 60 * 1000; // 24 horas en milisegundos
      if (duracionVuelo > duracionMaxima) {
        throw new Error('La duración del vuelo no puede ser mayor a 24 horas');
      }

      // Verificar que el aeropuerto de origen existe
      const aeropuertoOrigenExiste = airports.some(a => a.id === parseInt(vueloForm.aeropuerto_origen_id));
      if (!aeropuertoOrigenExiste) {
        throw new Error('El aeropuerto de origen no existe');
      }

      // Verificar que el aeropuerto de destino existe
      const aeropuertoDestinoExiste = airports.some(a => a.id === parseInt(vueloForm.aeropuerto_destino_id));
      if (!aeropuertoDestinoExiste) {
        throw new Error('El aeropuerto de destino no existe');
      }

      // Verificar que el avión existe
      const avionExiste = planes.some(p => p.id === parseInt(vueloForm.avion_id));
      if (!avionExiste) {
        throw new Error('El avión seleccionado no existe');
      }

      // Verificar que el avión está activo
      const avionSeleccionado = planes.find(p => p.id === parseInt(vueloForm.avion_id));
      if (avionSeleccionado?.estado !== 'ACTIVO') {
        throw new Error('El avión seleccionado no está activo');
      }

      // Verificar que origen y destino son diferentes
      if (vueloForm.aeropuerto_origen_id === vueloForm.aeropuerto_destino_id) {
        throw new Error('El aeropuerto de origen y destino no pueden ser el mismo');
      }

      // Validación de estado
      const estadosValidos = ['PROGRAMADO', 'EN_VUELO', 'COMPLETADO', 'CANCELADO'];
      if (!estadosValidos.includes(vueloForm.estado)) {
        throw new Error('El estado debe ser PROGRAMADO, EN_VUELO, COMPLETADO o CANCELADO');
      }

      const formData = {
        ...vueloForm,
        aeropuerto_origen_id: parseInt(vueloForm.aeropuerto_origen_id),
        aeropuerto_destino_id: parseInt(vueloForm.aeropuerto_destino_id),
        avion_id: parseInt(vueloForm.avion_id)
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('número de vuelo')) {
            throw new Error('Ya existe un vuelo con ese número');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('El vuelo no fue encontrado');
        }
        if (res.status === 422) {
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar vuelo');
      }

      hideModal('vueloModal');
      fetchVuelos();
    } catch (err: any) { 
      alert(`Error: ${err.message}`); 
    } finally { 
      setVueloSubmitting(false); 
    }
  };

  const deleteVuelo = async () => {
    if (!vueloDeleteId) return;
    setVueloSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8003/api/v1/vuelos/${vueloDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar vuelo');
      hideModal('deleteVueloModal');
      setVueloDeleteId(null); 
      fetchVuelos();
    } catch (err: any) { alert(err.message); }
    finally { setVueloSubmitting(false); }
  };

  // Función para cargar escalas
  const fetchEscalas = async () => {
    setEscalasLoading(true);
    setEscalasError('');
    try {
      const token = localStorage.getItem('token');
      const res = await fetch('http://localhost:8006/api/v1/escalas', {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al obtener escalas');
      setEscalas(await res.json());
    } catch (err: any) { 
      setEscalasError(err.message || 'Error al obtener escalas'); 
    } finally { 
      setEscalasLoading(false); 
    }
  };

  // Cargar escalas cuando se selecciona la sección
  useEffect(() => {
    if (activeSection === 'escalas') {
      fetchEscalas();
    }
  }, [activeSection]);

  const handleEscalaForm = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setEscalaForm((prev: any) => {
      const newForm = { ...prev, [name]: value };
      // Si se cambia el aeropuerto, cargar sus terminales
      if (name === 'aeropuerto_id' && value) {
        fetchTerminalesAeropuerto(parseInt(value));
        // Resetear la terminal seleccionada
        newForm.terminal = '';
      }
      return newForm;
    });
  };

  const openNewEscala = () => { 
    setEditingEscala(null); 
    setEscalaForm({
      vuelo_id: '',
      aeropuerto_id: '',
      numero_escala: '',
      orden: '',
      fecha_hora_llegada: '',
      fecha_hora_salida: '',
      tipo_escala: 'TECNICA',
      duracion_minutos: '',
      terminal: '',
      puerta: ''
    }); 
    showModal('escalaModal'); 
  };

  const openEditEscala = (escala: any) => { 
    setEditingEscala(escala); 
    setEscalaForm(escala); 
    showModal('escalaModal'); 
  };

  const confirmDeleteEscala = (id: number) => { 
    setEscalaDeleteId(id); 
    showModal('deleteEscalaModal'); 
  };

  const submitEscala = async (e: React.FormEvent) => {
    e.preventDefault(); 
    setEscalaSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingEscala ? 'PUT' : 'POST';
      const url = editingEscala ? `http://localhost:8006/api/v1/escalas/${editingEscala.id}` : 'http://localhost:8006/api/v1/escalas';
      
      // Validaciones de campos requeridos
      if (!escalaForm.vuelo_id?.toString().trim()) {
        throw new Error('Debe seleccionar un vuelo');
      }
      if (!escalaForm.aeropuerto_id?.toString().trim()) {
        throw new Error('Debe seleccionar un aeropuerto');
      }
      if (!escalaForm.numero_escala?.toString().trim()) {
        throw new Error('El número de escala es obligatorio');
      }
      if (!escalaForm.orden?.toString().trim()) {
        throw new Error('El orden es obligatorio');
      }
      if (!escalaForm.fecha_hora_llegada?.trim()) {
        throw new Error('La fecha y hora de llegada es obligatoria');
      }
      if (!escalaForm.fecha_hora_salida?.trim()) {
        throw new Error('La fecha y hora de salida es obligatoria');
      }
      if (!escalaForm.duracion_minutos?.toString().trim()) {
        throw new Error('La duración en minutos es obligatoria');
      }
      if (!escalaForm.terminal?.trim()) {
        throw new Error('La terminal es obligatoria');
      }
      if (!escalaForm.puerta?.trim()) {
        throw new Error('La puerta es obligatoria');
      }

      // Validación de números
      const numeroEscala = parseInt(escalaForm.numero_escala);
      const orden = parseInt(escalaForm.orden);
      const duracionMinutos = parseInt(escalaForm.duracion_minutos);

      if (isNaN(numeroEscala) || numeroEscala <= 0) {
        throw new Error('El número de escala debe ser un número positivo');
      }
      if (isNaN(orden) || orden <= 0) {
        throw new Error('El orden debe ser un número positivo');
      }
      if (isNaN(duracionMinutos) || duracionMinutos <= 0) {
        throw new Error('La duración en minutos debe ser un número positivo');
      }
      if (duracionMinutos > 1440) { // 24 horas en minutos
        throw new Error('La duración no puede ser mayor a 24 horas (1440 minutos)');
      }

      // Validación de fechas
      const fechaLlegada = new Date(escalaForm.fecha_hora_llegada);
      const fechaSalida = new Date(escalaForm.fecha_hora_salida);

      if (isNaN(fechaLlegada.getTime())) {
        throw new Error('La fecha y hora de llegada no es válida');
      }
      if (isNaN(fechaSalida.getTime())) {
        throw new Error('La fecha y hora de salida no es válida');
      }

      if (fechaSalida <= fechaLlegada) {
        throw new Error('La fecha y hora de salida debe ser posterior a la de llegada');
      }

      // Verificar que el vuelo existe
      const vueloExiste = vuelos.some(v => v.id === parseInt(escalaForm.vuelo_id));
      if (!vueloExiste) {
        throw new Error('El vuelo seleccionado no existe');
      }

      // Verificar que el aeropuerto existe
      const aeropuertoExiste = airports.some(a => a.id === parseInt(escalaForm.aeropuerto_id));
      if (!aeropuertoExiste) {
        throw new Error('El aeropuerto seleccionado no existe');
      }

      // Validación de tipo de escala
      const tiposEscalaValidos = ['TECNICA', 'COMERCIAL'];
      if (!tiposEscalaValidos.includes(escalaForm.tipo_escala)) {
        throw new Error('El tipo de escala debe ser TECNICA o COMERCIAL');
      }

      // Validación de formato de terminal (letra T seguida de número)
      const terminalRegex = /^T\d+$/;
      if (!terminalRegex.test(escalaForm.terminal)) {
        throw new Error('La terminal debe tener el formato: T seguido de número (ej: T1)');
      }

      // Validación de formato de puerta (letra seguida de número)
      const puertaRegex = /^[A-Z]\d+$/;
      if (!puertaRegex.test(escalaForm.puerta)) {
        throw new Error('La puerta debe tener el formato: letra seguida de número (ej: A1)');
      }

      const formData = {
        ...escalaForm,
        vuelo_id: parseInt(escalaForm.vuelo_id),
        aeropuerto_id: parseInt(escalaForm.aeropuerto_id),
        numero_escala: numeroEscala,
        orden: orden,
        duracion_minutos: duracionMinutos
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        
        // Manejo específico de errores comunes
        if (res.status === 400) {
          if (errorData.detail?.includes('número de escala')) {
            throw new Error('Ya existe una escala con ese número para este vuelo');
          }
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 401) {
          throw new Error('Sesión expirada. Por favor, inicie sesión nuevamente.');
        }
        if (res.status === 403) {
          throw new Error('No tiene permisos para realizar esta acción');
        }
        if (res.status === 404) {
          throw new Error('La escala no fue encontrada');
        }
        if (res.status === 422) {
          throw new Error(errorData.detail || 'Datos inválidos. Por favor, revise los campos.');
        }
        if (res.status === 500) {
          throw new Error('Error interno del servidor. Por favor, intente más tarde.');
        }
        
        throw new Error(errorData.detail || 'Error al guardar escala');
      }

      hideModal('escalaModal');
      fetchEscalas();
    } catch (err: any) { 
      alert(`Error: ${err.message}`); 
    } finally { 
      setEscalaSubmitting(false); 
    }
  };

  const deleteEscala = async () => {
    if (!escalaDeleteId) return;
    setEscalaSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8006/api/v1/escalas/${escalaDeleteId}`, {
        method: 'DELETE', 
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar escala');
      hideModal('deleteEscalaModal');
      setEscalaDeleteId(null); 
      fetchEscalas();
    } catch (err: any) { alert(err.message); }
    finally { setEscalaSubmitting(false); }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  // --- CRUD Pistas ---
  const handleRunwayForm = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setRunwayForm({ ...runwayForm, [e.target.name]: e.target.value });
  };

  const submitRunway = async (e: React.FormEvent) => {
    e.preventDefault();
    setRunwaySubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingRunway ? 'PUT' : 'POST';
      const url = editingRunway 
        ? `http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/pistas/${editingRunway.id}`
        : `http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/pistas`;

      // Validaciones
      if (!runwayForm.numero?.trim()) {
        throw new Error('El número de pista es obligatorio');
      }
      if (!runwayForm.longitud_metros?.toString().trim()) {
        throw new Error('La longitud es obligatoria');
      }
      if (!runwayForm.ancho_metros?.toString().trim()) {
        throw new Error('El ancho es obligatorio');
      }
      if (!runwayForm.superficie?.trim()) {
        throw new Error('La superficie es obligatoria');
      }

      // Validación de números
      const longitud = parseInt(runwayForm.longitud_metros);
      const ancho = parseInt(runwayForm.ancho_metros);

      if (isNaN(longitud) || longitud <= 0) {
        throw new Error('La longitud debe ser un número positivo');
      }
      if (isNaN(ancho) || ancho <= 0) {
        throw new Error('El ancho debe ser un número positivo');
      }

      // Validación de superficie
      const superficiesValidas = ['ASFALTO', 'CONCRETO', 'TIERRA'];
      if (!superficiesValidas.includes(runwayForm.superficie)) {
        throw new Error('La superficie debe ser ASFALTO, CONCRETO o TIERRA');
      }

      // Validación de estado
      const estadosValidos = ['ACTIVO', 'INACTIVO', 'MANTENIMIENTO'];
      if (!estadosValidos.includes(runwayForm.estado)) {
        throw new Error('El estado debe ser ACTIVO, INACTIVO o MANTENIMIENTO');
      }

      const formData = {
        ...runwayForm,
        longitud_metros: longitud,
        ancho_metros: ancho
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Error al guardar pista');
      }

      hideModal('runwayModal');
      fetchRunways(selectedAirport.id);
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setRunwaySubmitting(false);
    }
  };

  const deleteRunway = async () => {
    if (!runwayDeleteId || !selectedAirport) return;
    setRunwaySubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/pistas/${runwayDeleteId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar pista');
      hideModal('deleteRunwayModal');
      setRunwayDeleteId(null);
      fetchRunways(selectedAirport.id);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setRunwaySubmitting(false);
    }
  };

  // --- CRUD Terminales ---
  const handleTerminalForm = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setTerminalForm({ ...terminalForm, [e.target.name]: e.target.value });
  };

  const submitTerminal = async (e: React.FormEvent) => {
    e.preventDefault();
    setTerminalSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        throw new Error('No hay sesión activa. Por favor, inicie sesión nuevamente.');
      }

      const method = editingTerminal ? 'PUT' : 'POST';
      const url = editingTerminal 
        ? `http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/terminales/${editingTerminal.id}`
        : `http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/terminales`;

      // Validaciones
      if (!terminalForm.nombre?.trim()) {
        throw new Error('El nombre de la terminal es obligatorio');
      }
      if (!terminalForm.capacidad_pasajeros?.toString().trim()) {
        throw new Error('La capacidad de pasajeros es obligatoria');
      }

      // Validación de capacidad
      const capacidad = parseInt(terminalForm.capacidad_pasajeros);
      if (isNaN(capacidad) || capacidad <= 0) {
        throw new Error('La capacidad debe ser un número positivo');
      }

      // Validación de estado
      const estadosValidos = ['ACTIVO', 'INACTIVO', 'MANTENIMIENTO'];
      if (!estadosValidos.includes(terminalForm.estado)) {
        throw new Error('El estado debe ser ACTIVO, INACTIVO o MANTENIMIENTO');
      }

      const formData = {
        ...terminalForm,
        capacidad_pasajeros: capacidad
      };

      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify(formData),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Error al guardar terminal');
      }

      hideModal('terminalModal');
      fetchTerminals(selectedAirport.id);
    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setTerminalSubmitting(false);
    }
  };

  const deleteTerminal = async () => {
    if (!terminalDeleteId || !selectedAirport) return;
    setTerminalSubmitting(true);
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8005/api/v1/aeropuertos/${selectedAirport.id}/terminales/${terminalDeleteId}`, {
        method: 'DELETE',
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!res.ok) throw new Error('Error al eliminar terminal');
      hideModal('deleteTerminalModal');
      setTerminalDeleteId(null);
      fetchTerminals(selectedAirport.id);
    } catch (err: any) {
      alert(err.message);
    } finally {
      setTerminalSubmitting(false);
    }
  };

  return (
    <div className="container-fluid">
      <div className="row">
        <div className="col-md-2 bg-dark text-white p-3" style={{ minHeight: '100vh' }}>
          <h3 className="mb-4">Menú</h3>
          <ul className="nav flex-column">
            {SECTIONS.map(section => (
              <li key={section.key} className="nav-item">
                <button
                  className={`btn btn-link text-white ${activeSection === section.key ? 'active' : ''}`}
                  onClick={() => setActiveSection(section.key)}
                >
                  <i className={`bi ${section.icon} me-2`}></i>
                  {section.label}
                </button>
              </li>
            ))}
          </ul>
          <button className="btn btn-danger mt-4" onClick={handleLogout}>
            <i className="bi bi-box-arrow-right me-2"></i>
            Cerrar Sesión
          </button>
        </div>
        <div className="col-md-10 p-4">
          {activeSection === 'aviones' && (
            <div>
              <h2>Aviones</h2>
              <button className="btn btn-primary mb-3" onClick={openNewPlane}>
                <i className="bi bi-plus-circle me-2"></i>
                Nuevo Avión
              </button>
              {loading ? (
                <p>Cargando...</p>
              ) : error ? (
                <p className="text-danger">{error}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Matrícula</th>
                      <th>Modelo</th>
                      <th>Capacidad Pasajeros</th>
                      <th>Capacidad Carga</th>
                      <th>Estado</th>
                      <th>Última Revisión</th>
                      <th>Próxima Revisión</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {planes.map((plane: any) => (
                      <tr key={plane.id}>
                        <td>{plane.matricula}</td>
                        <td>{plane.modelo}</td>
                        <td>{plane.capacidad_pasajeros}</td>
                        <td>{plane.capacidad_carga}</td>
                        <td>{plane.estado}</td>
                        <td>{plane.ultima_revision}</td>
                        <td>{plane.proxima_revision}</td>
                        <td>
                          <button className="btn btn-sm btn-warning me-2" onClick={() => openEditPlane(plane)}>
                            <i className="bi bi-pencil"></i>
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => confirmDeletePlane(plane.id)}>
                            <i className="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
          {activeSection === 'aeropuertos' && (
            <div>
              <h2>Aeropuertos</h2>
              <button className="btn btn-primary mb-3" onClick={openNewAirport}>
                <i className="bi bi-plus-circle me-2"></i>
                Nuevo Aeropuerto
              </button>
              {airportLoading ? (
                <p>Cargando...</p>
              ) : airportError ? (
                <p className="text-danger">{airportError}</p>
              ) : (
                <div>
                  <table className="table">
                    <thead>
                      <tr>
                        <th>Nombre</th>
                        <th>Código IATA</th>
                        <th>Ciudad</th>
                        <th>País</th>
                        <th>Estado</th>
                        <th>Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      {airports.map((airport: any) => (
                        <tr key={airport.id}>
                          <td>{airport.nombre}</td>
                          <td>{airport.codigo_iata}</td>
                          <td>{airport.ciudad}</td>
                          <td>{airport.pais}</td>
                          <td>{airport.estado}</td>
                          <td>
                            <button className="btn btn-sm btn-info me-2" onClick={() => {
                              setSelectedAirport(airport);
                              setAirportTab('pistas');
                            }}>
                              <i className="bi bi-airplane me-1"></i>
                              Pistas
                            </button>
                            <button className="btn btn-sm btn-info me-2" onClick={() => {
                              setSelectedAirport(airport);
                              setAirportTab('terminales');
                            }}>
                              <i className="bi bi-building me-1"></i>
                              Terminales
                            </button>
                            <button className="btn btn-sm btn-warning me-2" onClick={() => openEditAirport(airport)}>
                              <i className="bi bi-pencil"></i>
                            </button>
                            <button className="btn btn-sm btn-danger" onClick={() => confirmDeleteAirport(airport.id)}>
                              <i className="bi bi-trash"></i>
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>

                  {selectedAirport && (
                    <div className="mt-4">
                      <h3>{selectedAirport.nombre} - {selectedAirport.codigo_iata}</h3>
                      <ul className="nav nav-tabs mb-3">
                        <li className="nav-item">
                          <button 
                            className={`nav-link ${airportTab === 'pistas' ? 'active' : ''}`}
                            onClick={() => setAirportTab('pistas')}
                          >
                            Pistas
                          </button>
                        </li>
                        <li className="nav-item">
                          <button 
                            className={`nav-link ${airportTab === 'terminales' ? 'active' : ''}`}
                            onClick={() => setAirportTab('terminales')}
                          >
                            Terminales
                          </button>
                        </li>
                      </ul>

                      {airportTab === 'pistas' && (
                        <div>
                          <button className="btn btn-primary mb-3" onClick={() => {
                            setEditingRunway(null);
                            setRunwayForm(emptyRunway);
                            showModal('runwayModal');
                          }}>
                            <i className="bi bi-plus-circle me-2"></i>
                            Nueva Pista
                          </button>
                          {runwaysLoading ? (
                            <p>Cargando pistas...</p>
                          ) : (
                            <table className="table">
                              <thead>
                                <tr>
                                  <th>Número</th>
                                  <th>Longitud (m)</th>
                                  <th>Ancho (m)</th>
                                  <th>Superficie</th>
                                  <th>Estado</th>
                                  <th>Acciones</th>
                                </tr>
                              </thead>
                              <tbody>
                                {runways.map((runway: any) => (
                                  <tr key={runway.id}>
                                    <td>{runway.numero}</td>
                                    <td>{runway.longitud_metros}</td>
                                    <td>{runway.ancho_metros}</td>
                                    <td>{runway.superficie}</td>
                                    <td>{runway.estado}</td>
                                    <td>
                                      <button className="btn btn-sm btn-warning me-2" onClick={() => {
                                        setEditingRunway(runway);
                                        setRunwayForm(runway);
                                        showModal('runwayModal');
                                      }}>
                                        <i className="bi bi-pencil"></i>
                                      </button>
                                      <button className="btn btn-sm btn-danger" onClick={() => {
                                        setRunwayDeleteId(runway.id);
                                        showModal('deleteRunwayModal');
                                      }}>
                                        <i className="bi bi-trash"></i>
                                      </button>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          )}
                        </div>
                      )}

                      {airportTab === 'terminales' && (
                        <div>
                          <button className="btn btn-primary mb-3" onClick={() => {
                            setEditingTerminal(null);
                            setTerminalForm(emptyTerminal);
                            showModal('terminalModal');
                          }}>
                            <i className="bi bi-plus-circle me-2"></i>
                            Nueva Terminal
                          </button>
                          {terminalsLoading ? (
                            <p>Cargando terminales...</p>
                          ) : (
                            <table className="table">
                              <thead>
                                <tr>
                                  <th>Nombre</th>
                                  <th>Capacidad Pasajeros</th>
                                  <th>Estado</th>
                                  <th>Acciones</th>
                                </tr>
                              </thead>
                              <tbody>
                                {terminals.map((terminal: any) => (
                                  <tr key={terminal.id}>
                                    <td>{terminal.nombre}</td>
                                    <td>{terminal.capacidad_pasajeros}</td>
                                    <td>{terminal.estado}</td>
                                    <td>
                                      <button className="btn btn-sm btn-warning me-2" onClick={() => {
                                        setEditingTerminal(terminal);
                                        setTerminalForm(terminal);
                                        showModal('terminalModal');
                                      }}>
                                        <i className="bi bi-pencil"></i>
                                      </button>
                                      <button className="btn btn-sm btn-danger" onClick={() => {
                                        setTerminalDeleteId(terminal.id);
                                        showModal('deleteTerminalModal');
                                      }}>
                                        <i className="bi bi-trash"></i>
                                      </button>
                                    </td>
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          )}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
          {activeSection === 'vuelos' && (
            <div>
              <h2>Vuelos</h2>
              <button className="btn btn-primary mb-3" onClick={openNewVuelo}>
                <i className="bi bi-plus-circle me-2"></i>
                Nuevo Vuelo
              </button>
              {vuelosLoading ? (
                <p>Cargando...</p>
              ) : vuelosError ? (
                <p className="text-danger">{vuelosError}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Número Vuelo</th>
                      <th>Fecha Salida</th>
                      <th>Fecha Llegada</th>
                      <th>Aeropuerto Origen</th>
                      <th>Aeropuerto Destino</th>
                      <th>Avión</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {vuelos.map((vuelo: any) => (
                      <tr key={vuelo.id}>
                        <td>{vuelo.numero_vuelo}</td>
                        <td>{new Date(vuelo.fecha_hora_salida).toLocaleString()}</td>
                        <td>{new Date(vuelo.fecha_hora_llegada).toLocaleString()}</td>
                        <td>{airports.find(a => a.id === vuelo.aeropuerto_origen_id)?.nombre || 'N/A'}</td>
                        <td>{airports.find(a => a.id === vuelo.aeropuerto_destino_id)?.nombre || 'N/A'}</td>
                        <td>{planes.find(p => p.id === vuelo.avion_id)?.matricula || 'N/A'}</td>
                        <td>{vuelo.estado}</td>
                        <td>
                          <button className="btn btn-sm btn-warning me-2" onClick={() => openEditVuelo(vuelo)}>
                            <i className="bi bi-pencil"></i>
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => confirmDeleteVuelo(vuelo.id)}>
                            <i className="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
          {activeSection === 'escalas' && (
            <div>
              <h2>Escalas</h2>
              <button className="btn btn-primary mb-3" onClick={openNewEscala}>
                <i className="bi bi-plus-circle me-2"></i>
                Nueva Escala
              </button>
              {escalasLoading ? (
                <p>Cargando...</p>
              ) : escalasError ? (
                <p className="text-danger">{escalasError}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Vuelo</th>
                      <th>Aeropuerto</th>
                      <th>Número Escala</th>
                      <th>Orden</th>
                      <th>Fecha Llegada</th>
                      <th>Fecha Salida</th>
                      <th>Tipo</th>
                      <th>Duración</th>
                      <th>Terminal</th>
                      <th>Puerta</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {escalas.map((escala: any) => (
                      <tr key={escala.id}>
                        <td>{vuelos.find(v => v.id === escala.vuelo_id)?.numero_vuelo || 'N/A'}</td>
                        <td>{airports.find(a => a.id === escala.aeropuerto_id)?.nombre || 'N/A'}</td>
                        <td>{escala.numero_escala}</td>
                        <td>{escala.orden}</td>
                        <td>{new Date(escala.fecha_hora_llegada).toLocaleString()}</td>
                        <td>{new Date(escala.fecha_hora_salida).toLocaleString()}</td>
                        <td>{escala.tipo_escala}</td>
                        <td>{escala.duracion_minutos} min</td>
                        <td>{escala.terminal}</td>
                        <td>{escala.puerta}</td>
                        <td>
                          <button className="btn btn-sm btn-warning me-2" onClick={() => openEditEscala(escala)}>
                            <i className="bi bi-pencil"></i>
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => confirmDeleteEscala(escala.id)}>
                            <i className="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
          {activeSection === 'pasajeros' && (
            <div>
              <h2>Pasajeros</h2>
              <button className="btn btn-primary mb-3" onClick={openNewPassenger}>
                <i className="bi bi-plus-circle me-2"></i>
                Nuevo Pasajero
              </button>
              {passengersLoading ? (
                <p>Cargando...</p>
              ) : passengersError ? (
                <p className="text-danger">{passengersError}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Tipo Documento</th>
                      <th>Número Documento</th>
                      <th>Fecha Nacimiento</th>
                      <th>Nacionalidad</th>
                      <th>Teléfono</th>
                      <th>Dirección</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {passengers.map((passenger: any) => (
                      <tr key={passenger.id}>
                        <td>{passenger.tipo_documento}</td>
                        <td>{passenger.numero_documento}</td>
                        <td>{passenger.fecha_nacimiento}</td>
                        <td>{passenger.nacionalidad}</td>
                        <td>{passenger.telefono}</td>
                        <td>{passenger.direccion}</td>
                        <td>
                          <button className="btn btn-sm btn-warning me-2" onClick={() => openEditPassenger(passenger)}>
                            <i className="bi bi-pencil"></i>
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => confirmDeletePassenger(passenger.id)}>
                            <i className="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
          {activeSection === 'reservas' && (
            <div>
              <h2>Reservas</h2>
              <button className="btn btn-primary mb-3" onClick={openNewReservation}>
                <i className="bi bi-plus-circle me-2"></i>
                Nueva Reserva
              </button>
              {reservationsLoading ? (
                <p>Cargando...</p>
              ) : reservationsError ? (
                <p className="text-danger">{reservationsError}</p>
              ) : (
                <table className="table">
                  <thead>
                    <tr>
                      <th>Pasajero ID</th>
                      <th>Vuelo ID</th>
                      <th>Asiento</th>
                      <th>Precio</th>
                      <th>Clase</th>
                      <th>Estado</th>
                      <th>Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {reservations.map((reservation: any) => (
                      <tr key={reservation.id}>
                        <td>{reservation.pasajero_id}</td>
                        <td>{reservation.vuelo_id}</td>
                        <td>{reservation.asiento}</td>
                        <td>{reservation.precio}</td>
                        <td>{reservation.clase}</td>
                        <td>{reservation.estado}</td>
                        <td>
                          <button className="btn btn-sm btn-warning me-2" onClick={() => openEditReservation(reservation)}>
                            <i className="bi bi-pencil"></i>
                          </button>
                          <button className="btn btn-sm btn-danger" onClick={() => confirmDeleteReservation(reservation.id)}>
                            <i className="bi bi-trash"></i>
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Modal de Avión */}
      <div className="modal fade" id="planeModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingPlane ? 'Editar Avión' : 'Nuevo Avión'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitPlane}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Matrícula</label>
                  <input type="text" className="form-control" name="matricula" value={planeForm.matricula} onChange={handlePlaneForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Modelo</label>
                  <input type="text" className="form-control" name="modelo" value={planeForm.modelo} onChange={handlePlaneForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Capacidad Pasajeros</label>
                  <input type="number" className="form-control" name="capacidad_pasajeros" value={planeForm.capacidad_pasajeros} onChange={handlePlaneForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Capacidad Carga</label>
                  <input type="number" className="form-control" name="capacidad_carga" value={planeForm.capacidad_carga} onChange={handlePlaneForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select className="form-select" name="estado" value={planeForm.estado} onChange={handlePlaneForm} required>
                    <option value="ACTIVO">Activo</option>
                    <option value="INACTIVO">Inactivo</option>
                    <option value="MANTENIMIENTO">Mantenimiento</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Última Revisión</label>
                  <input type="date" className="form-control" name="ultima_revision" value={planeForm.ultima_revision} onChange={handlePlaneForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Próxima Revisión</label>
                  <input type="date" className="form-control" name="proxima_revision" value={planeForm.proxima_revision} onChange={handlePlaneForm} required />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={planeSubmitting}>
                  {planeSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Avión */}
      <div className="modal fade" id="deletePlaneModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar este avión?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deletePlane} disabled={planeSubmitting}>
                {planeSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Aeropuerto */}
      <div className="modal fade" id="airportModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingAirport ? 'Editar Aeropuerto' : 'Nuevo Aeropuerto'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitAirport}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Nombre</label>
                  <input type="text" className="form-control" name="nombre" value={airportForm.nombre} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Código IATA</label>
                  <input type="text" className="form-control" name="codigo_iata" value={airportForm.codigo_iata} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Ciudad</label>
                  <input type="text" className="form-control" name="ciudad" value={airportForm.ciudad} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">País</label>
                  <input type="text" className="form-control" name="pais" value={airportForm.pais} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Latitud</label>
                  <input type="number" step="any" className="form-control" name="latitud" value={airportForm.latitud} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Longitud</label>
                  <input type="number" step="any" className="form-control" name="longitud" value={airportForm.longitud} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Zona Horaria</label>
                  <input type="text" className="form-control" name="zona_horaria" value={airportForm.zona_horaria} onChange={handleAirportForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select className="form-select" name="estado" value={airportForm.estado} onChange={handleAirportForm} required>
                    <option value="ACTIVO">Activo</option>
                    <option value="INACTIVO">Inactivo</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={airportSubmitting}>
                  {airportSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Aeropuerto */}
      <div className="modal fade" id="deleteAirportModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar este aeropuerto?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteAirport} disabled={airportSubmitting}>
                {airportSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Pasajero */}
      <div className="modal fade" id="passengerModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingPassenger ? 'Editar Pasajero' : 'Nuevo Pasajero'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitPassenger}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Tipo Documento</label>
                  <select className="form-select" name="tipo_documento" value={passengerForm.tipo_documento} onChange={handlePassengerForm} required>
                    <option value="DNI">DNI</option>
                    <option value="PASAPORTE">Pasaporte</option>
                    <option value="CE">CE</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Número Documento</label>
                  <input type="text" className="form-control" name="numero_documento" value={passengerForm.numero_documento} onChange={handlePassengerForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Fecha Nacimiento</label>
                  <input type="date" className="form-control" name="fecha_nacimiento" value={passengerForm.fecha_nacimiento} onChange={handlePassengerForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Nacionalidad</label>
                  <input type="text" className="form-control" name="nacionalidad" value={passengerForm.nacionalidad} onChange={handlePassengerForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Teléfono</label>
                  <input type="tel" className="form-control" name="telefono" value={passengerForm.telefono} onChange={handlePassengerForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Dirección</label>
                  <input type="text" className="form-control" name="direccion" value={passengerForm.direccion} onChange={handlePassengerForm} required />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={passengerSubmitting}>
                  {passengerSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Pasajero */}
      <div className="modal fade" id="deletePassengerModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar este pasajero?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deletePassenger} disabled={passengerSubmitting}>
                {passengerSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Reserva */}
      <div className="modal fade" id="reservationModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingReservation ? 'Editar Reserva' : 'Nueva Reserva'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitReservation}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Pasajero</label>
                  <select 
                    className="form-select" 
                    name="pasajero_id" 
                    value={reservationForm.pasajero_id} 
                    onChange={handleReservationForm} 
                    required
                  >
                    <option value="">Seleccione un pasajero</option>
                    {passengers.map((passenger: any) => (
                      <option key={passenger.id} value={passenger.id}>
                        {passenger.tipo_documento} {passenger.numero_documento} - {passenger.nacionalidad}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Vuelo</label>
                  <select 
                    className="form-select" 
                    name="vuelo_id" 
                    value={reservationForm.vuelo_id} 
                    onChange={handleReservationForm} 
                    required
                  >
                    <option value="">Seleccione un vuelo</option>
                    {vuelos.map((vuelo: any) => {
                      const fechaSalida = new Date(vuelo.fecha_hora_salida);
                      const fechaLlegada = new Date(vuelo.fecha_hora_llegada);
                      const fechaFormateada = fechaSalida.toLocaleString('es-ES', {
                        year: 'numeric',
                        month: '2-digit',
                        day: '2-digit',
                        hour: '2-digit',
                        minute: '2-digit'
                      });
                      return (
                        <option key={vuelo.id} value={vuelo.id}>
                          {vuelo.numero_vuelo} - {fechaFormateada} ({vuelo.origen} a {vuelo.destino})
                        </option>
                      );
                    })}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Asiento</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    name="asiento" 
                    value={reservationForm.asiento} 
                    onChange={handleReservationForm} 
                    placeholder="Ej: 12A" 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Precio</label>
                  <input 
                    type="number" 
                    step="0.01" 
                    className="form-control" 
                    name="precio" 
                    value={reservationForm.precio} 
                    onChange={handleReservationForm} 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Clase</label>
                  <select 
                    className="form-select" 
                    name="clase" 
                    value={reservationForm.clase} 
                    onChange={handleReservationForm} 
                    required
                  >
                    <option value="ECONOMICA">Económica</option>
                    <option value="EJECUTIVA">Ejecutiva</option>
                    <option value="PRIMERA">Primera</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select 
                    className="form-select" 
                    name="estado" 
                    value={reservationForm.estado} 
                    onChange={handleReservationForm} 
                    required
                  >
                    <option value="PENDIENTE">Pendiente</option>
                    <option value="CONFIRMADA">Confirmada</option>
                    <option value="CANCELADA">Cancelada</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={reservationSubmitting}>
                  {reservationSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Reserva */}
      <div className="modal fade" id="deleteReservationModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar esta reserva?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteReservation} disabled={reservationSubmitting}>
                {reservationSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Vuelo */}
      <div className="modal fade" id="vueloModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingVuelo ? 'Editar Vuelo' : 'Nuevo Vuelo'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitVuelo}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Número de Vuelo</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    name="numero_vuelo" 
                    value={vueloForm.numero_vuelo} 
                    onChange={handleVueloForm} 
                    placeholder="Ej: IB1234"
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Fecha y Hora de Salida</label>
                  <input 
                    type="datetime-local" 
                    className="form-control" 
                    name="fecha_hora_salida" 
                    value={vueloForm.fecha_hora_salida} 
                    onChange={handleVueloForm} 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Fecha y Hora de Llegada</label>
                  <input 
                    type="datetime-local" 
                    className="form-control" 
                    name="fecha_hora_llegada" 
                    value={vueloForm.fecha_hora_llegada} 
                    onChange={handleVueloForm} 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Aeropuerto de Origen</label>
                  <select 
                    className="form-select" 
                    name="aeropuerto_origen_id" 
                    value={vueloForm.aeropuerto_origen_id} 
                    onChange={handleVueloForm} 
                    required
                  >
                    <option value="">Seleccione un aeropuerto</option>
                    {airports.map((airport: any) => (
                      <option key={airport.id} value={airport.id}>
                        {airport.nombre} ({airport.codigo_iata})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Aeropuerto de Destino</label>
                  <select 
                    className="form-select" 
                    name="aeropuerto_destino_id" 
                    value={vueloForm.aeropuerto_destino_id} 
                    onChange={handleVueloForm} 
                    required
                  >
                    <option value="">Seleccione un aeropuerto</option>
                    {airports.map((airport: any) => (
                      <option key={airport.id} value={airport.id}>
                        {airport.nombre} ({airport.codigo_iata})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Avión</label>
                  <select 
                    className="form-select" 
                    name="avion_id" 
                    value={vueloForm.avion_id} 
                    onChange={handleVueloForm} 
                    required
                  >
                    <option value="">Seleccione un avión</option>
                    {planes.filter(p => p.estado === 'ACTIVO').map((plane: any) => (
                      <option key={plane.id} value={plane.id}>
                        {plane.matricula} - {plane.modelo}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select 
                    className="form-select" 
                    name="estado" 
                    value={vueloForm.estado} 
                    onChange={handleVueloForm} 
                    required
                  >
                    <option value="PROGRAMADO">Programado</option>
                    <option value="EN_VUELO">En Vuelo</option>
                    <option value="COMPLETADO">Completado</option>
                    <option value="CANCELADO">Cancelado</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={vueloSubmitting}>
                  {vueloSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Vuelo */}
      <div className="modal fade" id="deleteVueloModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar este vuelo?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteVuelo} disabled={vueloSubmitting}>
                {vueloSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Escala */}
      <div className="modal fade" id="escalaModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingEscala ? 'Editar Escala' : 'Nueva Escala'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitEscala}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Vuelo</label>
                  <select 
                    className="form-select" 
                    name="vuelo_id" 
                    value={escalaForm.vuelo_id} 
                    onChange={handleEscalaForm} 
                    required
                  >
                    <option value="">Seleccione un vuelo</option>
                    {vuelos.map((vuelo: any) => (
                      <option key={vuelo.id} value={vuelo.id}>
                        {vuelo.numero_vuelo} - {new Date(vuelo.fecha_hora_salida).toLocaleString()}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Aeropuerto</label>
                  <select 
                    className="form-select" 
                    name="aeropuerto_id" 
                    value={escalaForm.aeropuerto_id} 
                    onChange={handleEscalaForm} 
                    required
                  >
                    <option value="">Seleccione un aeropuerto</option>
                    {airports.map((airport: any) => (
                      <option key={airport.id} value={airport.id}>
                        {airport.nombre} ({airport.codigo_iata})
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Número de Escala</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    name="numero_escala" 
                    value={escalaForm.numero_escala} 
                    onChange={handleEscalaForm} 
                    min="1"
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Orden</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    name="orden" 
                    value={escalaForm.orden} 
                    onChange={handleEscalaForm} 
                    min="1"
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Fecha y Hora de Llegada</label>
                  <input 
                    type="datetime-local" 
                    className="form-control" 
                    name="fecha_hora_llegada" 
                    value={escalaForm.fecha_hora_llegada} 
                    onChange={handleEscalaForm} 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Fecha y Hora de Salida</label>
                  <input 
                    type="datetime-local" 
                    className="form-control" 
                    name="fecha_hora_salida" 
                    value={escalaForm.fecha_hora_salida} 
                    onChange={handleEscalaForm} 
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Tipo de Escala</label>
                  <select 
                    className="form-select" 
                    name="tipo_escala" 
                    value={escalaForm.tipo_escala} 
                    onChange={handleEscalaForm} 
                    required
                  >
                    <option value="TECNICA">Técnica</option>
                    <option value="COMERCIAL">Comercial</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Duración (minutos)</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    name="duracion_minutos" 
                    value={escalaForm.duracion_minutos} 
                    onChange={handleEscalaForm} 
                    min="1"
                    max="1440"
                    required 
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Terminal</label>
                  <select 
                    className="form-select" 
                    name="terminal" 
                    value={escalaForm.terminal} 
                    onChange={handleEscalaForm} 
                    required
                    disabled={!escalaForm.aeropuerto_id}
                  >
                    <option value="">Seleccione una terminal</option>
                    {terminalesAeropuerto.map((terminal: any) => (
                      <option key={terminal.id} value={terminal.nombre}>
                        {terminal.nombre}
                      </option>
                    ))}
                  </select>
                  {!escalaForm.aeropuerto_id && (
                    <small className="text-muted">Seleccione primero un aeropuerto</small>
                  )}
                </div>
                <div className="mb-3">
                  <label className="form-label">Puerta</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    name="puerta" 
                    value={escalaForm.puerta} 
                    onChange={handleEscalaForm} 
                    placeholder="Ej: A1"
                    required 
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={escalaSubmitting}>
                  {escalaSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Escala */}
      <div className="modal fade" id="deleteEscalaModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar esta escala?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteEscala} disabled={escalaSubmitting}>
                {escalaSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Pista */}
      <div className="modal fade" id="runwayModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingRunway ? 'Editar Pista' : 'Nueva Pista'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitRunway}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Número</label>
                  <input type="text" className="form-control" name="numero" value={runwayForm.numero} onChange={handleRunwayForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Longitud (metros)</label>
                  <input type="number" className="form-control" name="longitud_metros" value={runwayForm.longitud_metros} onChange={handleRunwayForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Ancho (metros)</label>
                  <input type="number" className="form-control" name="ancho_metros" value={runwayForm.ancho_metros} onChange={handleRunwayForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Superficie</label>
                  <select className="form-select" name="superficie" value={runwayForm.superficie} onChange={handleRunwayForm} required>
                    <option value="ASFALTO">Asfalto</option>
                    <option value="CONCRETO">Concreto</option>
                    <option value="TIERRA">Tierra</option>
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select className="form-select" name="estado" value={runwayForm.estado} onChange={handleRunwayForm} required>
                    <option value="ACTIVO">Activo</option>
                    <option value="INACTIVO">Inactivo</option>
                    <option value="MANTENIMIENTO">Mantenimiento</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={runwaySubmitting}>
                  {runwaySubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Terminal */}
      <div className="modal fade" id="terminalModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">{editingTerminal ? 'Editar Terminal' : 'Nueva Terminal'}</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <form onSubmit={submitTerminal}>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Nombre</label>
                  <input type="text" className="form-control" name="nombre" value={terminalForm.nombre} onChange={handleTerminalForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Capacidad Pasajeros</label>
                  <input type="number" className="form-control" name="capacidad_pasajeros" value={terminalForm.capacidad_pasajeros} onChange={handleTerminalForm} required />
                </div>
                <div className="mb-3">
                  <label className="form-label">Estado</label>
                  <select className="form-select" name="estado" value={terminalForm.estado} onChange={handleTerminalForm} required>
                    <option value="ACTIVO">Activo</option>
                    <option value="INACTIVO">Inactivo</option>
                    <option value="MANTENIMIENTO">Mantenimiento</option>
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                <button type="submit" className="btn btn-primary" disabled={terminalSubmitting}>
                  {terminalSubmitting ? 'Guardando...' : 'Guardar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Pista */}
      <div className="modal fade" id="deleteRunwayModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar esta pista?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteRunway} disabled={runwaySubmitting}>
                {runwaySubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Modal de Confirmación Eliminar Terminal */}
      <div className="modal fade" id="deleteTerminalModal" tabIndex={-1} aria-hidden="true">
        <div className="modal-dialog">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title">Confirmar Eliminación</h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div className="modal-body">
              ¿Está seguro que desea eliminar esta terminal?
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
              <button type="button" className="btn btn-danger" onClick={deleteTerminal} disabled={terminalSubmitting}>
                {terminalSubmitting ? 'Eliminando...' : 'Eliminar'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
} 