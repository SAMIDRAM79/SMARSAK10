import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_URL = `${BACKEND_URL}/api`;

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear token and redirect to login
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/connexion';
    }
    return Promise.reject(error);
  }
);

// Auth APIs
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getProfile: () => api.get('/auth/me'),
};

// Download APIs
export const downloadAPI = {
  getDownloads: () => api.get('/downloads'),
  trackDownload: (downloadId, userId = null) => 
    api.post('/downloads/track', { download_id: downloadId, user_id: userId }),
};

// Product APIs
export const productAPI = {
  getProducts: () => api.get('/products'),
  getProduct: (id) => api.get(`/products/${id}`),
};

// Order APIs
export const orderAPI = {
  createOrder: (data) => api.post('/orders', data),
  getOrders: () => api.get('/orders'),
  getOrder: (id) => api.get(`/orders/${id}`),
};

// Ticket APIs
export const ticketAPI = {
  createTicket: (data) => api.post('/tickets', data),
  getTickets: () => api.get('/tickets'),
  getTicket: (id) => api.get(`/tickets/${id}`),
};

export default api;
