import axios, { AxiosError } from 'axios';

export interface ApiError {
  message: string;
  statusCode?: number;
  data?: any;
}

export const apiClient = axios.create({
  baseURL: '/api/v1',
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const apiError: ApiError = {
      message: error.message || 'Network error occurred',
      statusCode: error.response?.status,
      data: error.response?.data,
    };
    return Promise.reject(apiError);
  }
);
