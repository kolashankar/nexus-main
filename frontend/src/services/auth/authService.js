import React from "react";
/**
 * Authentication service
 */
import apiClient from '../api/client';

class AuthService {
  async register(data) {
    const response = await apiClient.post('/api/auth/register', data);
    const authData = response.data;

    // Store tokens
    this.setTokens(authData.access_token, authData.refresh_token);

    return authData;
  }

  async login(data) {
    const response = await apiClient.post('/api/auth/login', data);
    const authData = response.data;

    // Store tokens
    this.setTokens(authData.access_token, authData.refresh_token);

    return authData;
  }

  async logout() {
    try {
      await apiClient.post('/api/auth/logout');
    } finally {
      this.clearTokens();
    }
  }

  async getCurrentUser() {
    const response = await apiClient.get('/api/auth/me');
    return response.data;
  }

  setTokens(accessToken, refreshToken) {
    localStorage.setItem('access_token', accessToken);
    localStorage.setItem('refresh_token', refreshToken);
  }

  clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  getAccessToken() {
    return localStorage.getItem('access_token');
  }

  isAuthenticated() {
    return !!this.getAccessToken();
  }
}

export default new AuthService();
