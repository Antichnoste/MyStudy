import axios from 'axios';

const BASE_URL = import.meta.env.PROD ? '' : 'http://localhost:8080';

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
        const requestUrl = error.config.url || '';

        if (!requestUrl.includes('/api/auth/login') && !requestUrl.includes('/api/auth/register')) {
            localStorage.removeItem('jwt_token');
            window.location.href = '/login';
        }
    }
    return Promise.reject(error);
  }
);

export default api;