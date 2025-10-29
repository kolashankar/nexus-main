import React from "react";
/**
 * API client configuration
 */
import axios from 'axios';

// Use relative URL to leverage Vite's proxy configuration
// Support both Vite (import.meta.env) and Create React App (process.env) patterns
const API_URL = import.meta.env?.VITE_BACKEND_URL || 
                process.env.REACT_APP_BACKEND_URL || 
                '';

export const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Extract user-friendly error message
    let errorMessage = 'An error occurred. Please try again.';
    
    if (error.response) {
      // Server responded with error
      const { status, data } = error.response;
      
      if (data && data.detail) {
        // Backend provides detailed error message
        errorMessage = typeof data.detail === 'string' 
          ? data.detail 
          : JSON.stringify(data.detail);
      } else if (status === 400) {
        errorMessage = 'Invalid request. Please check your input.';
      } else if (status === 401) {
        errorMessage = 'Authentication failed. Please check your credentials.';
      } else if (status === 403) {
        errorMessage = 'Access denied. You do not have permission.';
      } else if (status === 404) {
        errorMessage = 'Resource not found.';
      } else if (status === 422) {
        errorMessage = 'Validation error. Please check your input fields.';
      } else if (status === 500) {
        errorMessage = 'Server error. Please try again later.';
      }
    } else if (error.request) {
      // Request made but no response
      if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        errorMessage = 'Request timeout. Please check your connection and try again.';
      } else {
        errorMessage = 'Unable to connect to server. Please check your internet connection.';
      }
    }

    // Attach user-friendly message to error
    error.userMessage = errorMessage;

    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post(`${API_URL}/api/auth/refresh`, {
            refresh_token: refreshToken,
          });

          const { access_token } = response.data;
          localStorage.setItem('access_token', access_token);

          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return apiClient(originalRequest);
        }
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default apiClient;
