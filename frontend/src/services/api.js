import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_URL = `${BACKEND_URL}/api`;
const USER_EMAIL = 'konatdra@gmail.com';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-User-Email': USER_EMAIL,
  },
});

// Students API
export const studentsAPI = {
  getAll: (niveau = null, classe = null) => {
    let url = '/students';
    const params = new URLSearchParams();
    if (niveau) params.append('niveau', niveau);
    if (classe) params.append('classe', classe);
    if (params.toString()) url += `?${params.toString()}`;
    return api.get(url);
  },
  getById: (id) => api.get(`/students/${id}`),
  create: (data) => api.post('/students', data),
  update: (id, data) => api.put(`/students/${id}`, data),
  delete: (id) => api.delete(`/students/${id}`),
};

// Classes API
export const classesAPI = {
  getAll: (niveau = null) => {
    let url = '/classes';
    if (niveau) url += `?niveau=${niveau}`;
    return api.get(url);
  },
  getById: (id) => api.get(`/classes/${id}`),
  create: (data) => api.post('/classes', data),
};

// Matières API
export const matieresAPI = {
  getAll: (niveau = null) => {
    let url = '/matieres';
    if (niveau) url += `?niveau=${niveau}`;
    return api.get(url);
  },
  getById: (id) => api.get(`/matieres/${id}`),
  create: (data) => api.post('/matieres', data),
};

// Notes API
export const notesAPI = {
  getStudentNotes: (studentId, periode = null) => {
    let url = `/notes/student/${studentId}`;
    if (periode) url += `?periode=${periode}`;
    return api.get(url);
  },
  getClasseNotes: (classe, matiereId = null, periode = null) => {
    let url = `/notes/classe/${classe}`;
    const params = new URLSearchParams();
    if (matiereId) params.append('matiere_id', matiereId);
    if (periode) params.append('periode', periode);
    if (params.toString()) url += `?${params.toString()}`;
    return api.get(url);
  },
  create: (data) => api.post('/notes', data),
  update: (id, data) => api.put(`/notes/${id}`, data),
  delete: (id) => api.delete(`/notes/${id}`),
};

// Bulletins API
export const bulletinsAPI = {
  generate: (studentId, periode, anneeScolaire) => 
    api.post('/bulletins/generate', null, {
      params: { student_id: studentId, periode, annee_scolaire: anneeScolaire }
    }),
  getStudentBulletins: (studentId) => api.get(`/bulletins/student/${studentId}`),
  getById: (id) => api.get(`/bulletins/${id}`),
};

// Enseignants API
export const enseignantsAPI = {
  getAll: () => api.get('/enseignants'),
  getById: (id) => api.get(`/enseignants/${id}`),
  create: (data) => api.post('/enseignants', data),
};

// Statistics API
export const statsAPI = {
  getDashboard: () => api.get('/statistics/dashboard'),
  getClasseStats: (classe) => api.get(`/statistics/classe/${classe}`),
};

export default api;
