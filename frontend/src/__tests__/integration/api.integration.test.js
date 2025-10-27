import React from "react";
/**
 * Integration tests for API client
 */

import { apiClient } from '../../services/api/client';
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.post('/api/auth/login', (req, res, ctx) => {
    return res(
      ctx.json({
        access_token: 'mock-token',
        user: { username: 'testuser' },
      })
    );
  }),

  rest.get('/api/player/profile', (req, res, ctx) => {
    const auth = req.headers.get('Authorization');
    if (!auth) {
      return res(ctx.status(401), ctx.json({ error: 'Unauthorized' }));
    }

    return res(
      ctx.json({
        _id: 'test-id',
        username: 'testuser',
        level: 1,
        karma_points: 0,
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Integration Tests', () => {
  describe('Authentication', () => {
    test('login returns token and user data', async () => {
      const result = await apiClient.post('/auth/login', {
        username: 'testuser',
        password: 'testpass123',
      });

      expect(result.data.access_token).toBe('mock-token');
      expect(result.data.user.username).toBe('testuser');
    });

    test('stores token in localStorage', async () => {
      await apiClient.post('/auth/login', {
        username: 'testuser',
        password: 'testpass123',
      });

      expect(localStorage.getItem('token')).toBe('mock-token');
    });
  });

  describe('Protected Routes', () => {
    test('includes auth token in requests', async () => {
      localStorage.setItem('token', 'test-token');

      const result = await apiClient.get('/player/profile');

      expect(result.data.username).toBe('testuser');
    });

    test('returns 401 when token missing', async () => {
      localStorage.removeItem('token');

      await expect(apiClient.get('/player/profile')).rejects.toThrow();
    });
  });

  describe('Error Handling', () => {
    test('handles network errors', async () => {
      server.use(
        rest.get('/api/player/profile', (req, res) => {
          return res.networkError('Network error');
        })
      );

      await expect(apiClient.get('/player/profile')).rejects.toThrow('Network Error');
    });

    test('handles server errors', async () => {
      server.use(
        rest.get('/api/player/profile', (req, res, ctx) => {
          return res(ctx.status(500), ctx.json({ error: 'Server Error' }));
        })
      );
      
      await expect(apiClient.get('/player/profile')).rejects.toThrow('Request failed with status code 500');
    });
  });

  describe('Request Interceptors', () => {
    test('adds API base URL', async () => {
      const result = await apiClient.get('/player/profile');
      expect(result.config.url).toContain('/api/');
    });

    test('sets correct headers', async () => {
      const result = await apiClient.get('/player/profile');
      expect(result.config.headers['Content-Type']).toBe('application/json');
    });
  });
});