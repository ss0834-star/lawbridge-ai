import axios from 'axios';
const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export const api = axios.create({ baseURL: API });
api.interceptors.request.use(c => {
  const t = typeof window !== 'undefined' ? localStorage.getItem('lb_token') : null;
  if (t) c.headers.Authorization = `Bearer ${t}`;
  return c;
});
api.interceptors.response.use(r => r, e => {
  if (e.response?.status === 401 && typeof window !== 'undefined') {
    localStorage.removeItem('lb_token'); localStorage.removeItem('lb_user');
    window.location.href = '/login';
  }
  return Promise.reject(e);
});
export const authApi = {
  register: (d: any) => api.post('/auth/register', d),
  login: (d: any) => api.post('/auth/login', d),
  demo: () => api.post('/auth/demo-login'),
  me: () => api.get('/auth/me'),
  acceptDisclaimer: () => api.post('/auth/accept-disclaimer'),
};
export const docApi = {
  upload: (file: File, type?: string, lang?: string) => {
    const fd = new FormData(); fd.append('file', file);
    if (type) fd.append('document_type', type);
    if (lang) fd.append('language', lang);
    return api.post('/documents/upload', fd, { headers: { 'Content-Type': 'multipart/form-data' } });
  },
  list: () => api.get('/documents'),
  get: (id: number) => api.get(`/documents/${id}`),
  del: (id: number) => api.delete(`/documents/${id}`),
};
export const analysisApi = {
  start: (id: number) => api.post(`/analysis/start/${id}`),
  get: (id: number) => api.get(`/analysis/${id}`),
};
export const chatApi = {
  createSession: (docId?: number, lang?: string, type?: string) => api.post('/chat/session', { document_id: docId, language: lang, session_type: type || 'document' }),
  getSession: (id: number) => api.get(`/chat/session/${id}`),
  send: (sessionId: number, content: string, lang?: string) => api.post('/chat/message', { session_id: sessionId, content, language: lang }),
  sessions: () => api.get('/chat/sessions'),
};
export const qaApi = {
  ask: (question: string, language?: string, context?: string, category?: string) => api.post('/legal-qa/ask', { question, language, context, category }),
  history: () => api.get('/legal-qa/history'),
  popular: () => api.get('/legal-qa/popular'),
};
export const locationApi = {
  update: (state: string, city?: string) => api.post('/location/update', { state, city: city || '' }),
  resources: (state?: string) => api.get('/location/resources', { params: { state } }),
  checklist: (state: string, docType: string) => api.get('/location/checklist', { params: { state, document_type: docType } }),
  states: () => api.get('/location/states'),
  my: () => api.get('/location/my'),
};
export const rightsApi = {
  categories: () => api.get('/rights/categories'),
  get: (cat: string) => api.get(`/rights/${cat}`),
};
export const adminApi = {
  stats: () => api.get('/admin/stats'),
  users: () => api.get('/admin/users'),
  health: () => api.get('/admin/system-health'),
  logs: () => api.get('/admin/audit-logs'),
};
