import React from "react";
import { describe, it, expect, beforeAll, afterAll } from '@jest/globals';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

describe('API Integration Tests', () => {
  let authToken;

  beforeAll(async () => {
    // Login to get auth token
    const response = await axios.post(`${API_URL}/api/auth/login`, {
      username: 'testuser',
      password: 'testpass123',
    });
    authToken = response.data.access_token;
  });

  describe('Player API', () => {
    it('should fetch player profile', async () => {
      const response = await axios.get(`${API_URL}/api/player/profile`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('username');
      expect(response.data).toHaveProperty('karma_points');
      expect(response.data).toHaveProperty('traits');
    });

    it('should update player visibility settings', async () => {
      const response = await axios.put(
        `${API_URL}/api/player/visibility`,
        {
          privacy_tier: 'public',
          cash: true,
          karma_score: true,
        },
        {
          headers: { Authorization: `Bearer ${authToken}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data.message).toBe('Visibility updated');
    });

    it('should fetch player stats', async () => {
      const response = await axios.get(`${API_URL}/api/player/stats`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('total_actions');
      expect(response.data).toHaveProperty('pvp_wins');
    });
  });

  describe('Combat API', () => {
    it('should fetch active combat', async () => {
      const response = await axios.get(`${API_URL}/api/combat/active`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });

    it('should fetch combat stats', async () => {
      const response = await axios.get(`${API_URL}/api/combat/stats`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('total_battles');
    });
  });

  describe('Quests API', () => {
    it('should fetch available quests', async () => {
      const response = await axios.get(`${API_URL}/api/quests/available`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });

    it('should fetch active quests', async () => {
      const response = await axios.get(`${API_URL}/api/quests/active`, {
        headers: { Authorization: `Bearer ${authToken}` },
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });
  });

  describe('Leaderboards API', () => {
    it('should fetch karma leaderboard', async () => {
      const response = await axios.get(`${API_URL}/api/leaderboards/karma`);

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
      if (response.data.length > 0) {
        expect(response.data[0]).toHaveProperty('username');
        expect(response.data[0]).toHaveProperty('karma_points');
      }
    });

    it('should fetch wealth leaderboard', async () => {
      const response = await axios.get(`${API_URL}/api/leaderboards/wealth`);

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });
  });
});
