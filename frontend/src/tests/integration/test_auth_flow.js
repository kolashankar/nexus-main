import React from "react";
import { describe, it, expect } from '@jest/globals';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

describe('Auth Flow Integration Tests', () => {
  const testUser = {
    username: `testuser_${Date.now()}`,
    email: `testuser_${Date.now()}@example.com`,
    password: 'SecurePass123!',
  };

  let authToken;
  let refreshToken;

  describe('Registration', () => {
    it('should register a new user', async () => {
      const response = await axios.post(`${API_URL}/api/auth/register`, testUser);

      expect(response.status).toBe(201);
      expect(response.data).toHaveProperty('message');
      expect(response.data.message).toContain('registered');
    });

    it('should not register duplicate username', async () => {
      await expect(axios.post(`${API_URL}/api/auth/register`, testUser)).rejects.toThrow();
    });

    it('should validate password strength', async () => {
      const weakUser = {
        ...testUser,
        username: 'testuser_weak',
        password: '123',
      };

      await expect(axios.post(`${API_URL}/api/auth/register`, weakUser)).rejects.toThrow();
    });
  });

  describe('Login', () => {
    it('should login with correct credentials', async () => {
      const response = await axios.post(`${API_URL}/api/auth/login`, {
        username: testUser.username,
        password: testUser.password,
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('access_token');
      expect(response.data).toHaveProperty('token_type', 'bearer');

      authToken = response.data.access_token;
      refreshToken = response.data.refresh_token;
    });

    it('should fail with incorrect password', async () => {
      await expect(axios.post(`${API_URL}/api/auth/login`, {
        username: testUser.username,
        password: 'wrongpassword',
      })).rejects.toThrow();
    });

    it('should fail with non-existent user', async () => {
      await expect(axios.post(`${API_URL}/api/auth/login`, {
        username: 'nonexistentuser',
        password: 'somepassword',
      })).rejects.toThrow();
    });
  });

  describe('Protected Routes', () => {
    it('should access protected route with valid token', async () => {
      const response = await axios.get(`${API_URL}/api/auth/me`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(response.data.username).toBe(testUser.username);
    });

    it('should reject request without token', async () => {
      await expect(axios.get(`${API_URL}/api/auth/me`)).rejects.toThrow();
    });

    it('should reject request with invalid token', async () => {
      await expect(axios.get(`${API_URL}/api/auth/me`, {
        headers: { Authorization: 'Bearer invalid-token' },
      })).rejects.toThrow();
    });
  });

  describe('Token Refresh', () => {
    it('should refresh access token', async () => {
      const response = await axios.post(`${API_URL}/api/auth/refresh`, {
        refresh_token: refreshToken,
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('access_token');
      expect(response.data.access_token).not.toBe(authToken);
    });

    it('should reject invalid refresh token', async () => {
      await expect(axios.post(`${API_URL}/api/auth/refresh`, {
        refresh_token: 'invalid-refresh-token',
      })).rejects.toThrow();
    });
  });

  describe('Logout', () => {
    it('should logout successfully', async () => {
      const response = await axios.post(
        `${API_URL}/api/auth/logout`,
        {},
        {
          headers: { Authorization: `Bearer ${authToken}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data.message).toContain('logout');
    });
  });
});