import axios, { AxiosError } from 'axios';

export interface ApiError {
  message: string;
  statusCode?: number;
  data?: any;
}

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => {
    // If static host rewrote missing API route to index.html, reject cleanly
    if (typeof response.data === 'string' && response.data.trim().startsWith('<!doctype html>')) {
      const apiError: ApiError = {
        message: 'Endpoint returned HTML instead of JSON (API unavailable)',
        statusCode: 404,
      };
      return Promise.reject(apiError);
    }
    return response;
  },
  (error: AxiosError) => {
    const apiError: ApiError = {
      message: error.message || 'Network error occurred',
      statusCode: error.response?.status,
      data: error.response?.data,
    };
    return Promise.reject(apiError);
  }
);
