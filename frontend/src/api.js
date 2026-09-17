import axios from 'axios';

// In production, set VITE_API_URL to the deployed backend URL at build time.
const rawApiUrl = (import.meta.env.VITE_API_URL || 'http://localhost:8000').trim();
export const API_URL = rawApiUrl.replace(/\/+$/, '');

const client = axios.create({ baseURL: API_URL });

client.interceptors.request.use((config) => {
  const token = localStorage.getItem('h2s_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

function unwrap(promise) {
  return promise.then((res) => res.data).catch((err) => {
    const detail = err?.response?.data?.detail || err.message || 'Request failed';
    throw new Error(detail);
  });
}

export const api = {
  login: (worker_id, pin) => unwrap(client.post('/api/auth/login', { worker_id, pin })),

  startShift: (worker_id, cartridge_id, shift_label) =>
    unwrap(client.post('/api/shifts/start', { worker_id, cartridge_id, shift_label })),
  endShift: (shiftId) => unwrap(client.post(`/api/shifts/${shiftId}/end`)),
  getShift: (shiftId) => unwrap(client.get(`/api/shifts/${shiftId}`)),
  workerHistory: (workerId) => unwrap(client.get(`/api/shifts/worker/${workerId}/history`)),

  sendReading: (shiftId, reading) => unwrap(client.post(`/api/sensors/${shiftId}/reading`, reading)),
  latestReading: (shiftId) => unwrap(client.get(`/api/sensors/${shiftId}/latest`)),
  readingHistory: (shiftId) => unwrap(client.get(`/api/sensors/${shiftId}/history`)),
  shiftAlerts: (shiftId) => unwrap(client.get(`/api/sensors/${shiftId}/alerts`)),

  registerCartridge: (cartridge_id) => {
    const form = new FormData();
    form.append('cartridge_id', cartridge_id);
    return unwrap(client.post('/api/cartridge/register', form));
  },
  getCartridge: (cartridgeId) => unwrap(client.get(`/api/cartridge/${cartridgeId}`)),
  scanCartridge: (shiftId, cartridgeId, file, temp_c, humidity_pct) => {
    const form = new FormData();
    form.append('shift_id', shiftId);
    form.append('cartridge_id', cartridgeId);
    form.append('temp_c', temp_c);
    form.append('humidity_pct', humidity_pct);
    form.append('image', file);
    return unwrap(client.post('/api/cartridge/scan', form));
  },

  sos: (shiftId) => unwrap(client.post('/api/alerts/sos', { shift_id: shiftId })),
  acknowledgeAlert: (alertId) => unwrap(client.post(`/api/alerts/${alertId}/acknowledge`)),

  supervisorWorkers: () => unwrap(client.get('/api/supervisor/workers')),
  supervisorAlerts: () => unwrap(client.get('/api/supervisor/alerts')),

  report: (shiftId) => unwrap(client.get(`/api/reports/${shiftId}`)),
};
