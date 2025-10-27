import React from "react";
import { describe, it, expect, beforeAll } from '@jest/globals';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

describe('Combat Flow Integration Tests', () => {
  let authToken1;
  let authToken2;
  let player1Id;
  let player2Id;
  let combatId;

  beforeAll(async () => {
    // Login two test users
    const login1 = await axios.post(`${API_URL}/api/auth/login`, {
      username: 'testuser1',
      password: 'testpass123',
    });
    authToken1 = login1.data.access_token;

    const login2 = await axios.post(`${API_URL}/api/auth/login`, {
      username: 'testuser2',
      password: 'testpass123',
    });
    authToken2 = login2.data.access_token;

    // Get player IDs
    const profile1 = await axios.get(`${API_URL}/api/player/profile`, {
      headers: { Authorization: `Bearer ${authToken1}` },
    });
    player1Id = profile1.data.player_id;

    const profile2 = await axios.get(`${API_URL}/api/player/profile`, {
      headers: { Authorization: `Bearer ${authToken2}` },
    });
    player2Id = profile2.data.player_id;
  });

  describe('Combat Challenge', () => {
    it('should challenge another player to combat', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/challenge`,
        {
          target_player_id: player2Id,
        },
        {
          headers: { Authorization: `Bearer ${authToken1}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('combat_id');
      expect(response.data.status).toBe('pending');
      combatId = response.data.combat_id;
    });

    it('should accept combat challenge', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/accept`,
        {
          combat_id: combatId,
        },
        {
          headers: { Authorization: `Bearer ${authToken2}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data.status).toBe('active');
    });
  });

  describe('Combat Actions', () => {
    it('should perform attack action', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/action`,
        {
          combat_id: combatId,
          action_type: 'attack',
          target: 'opponent',
        },
        {
          headers: { Authorization: `Bearer ${authToken1}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('damage_dealt');
      expect(response.data).toHaveProperty('new_hp');
    });

    it('should perform defend action', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/action`,
        {
          combat_id: combatId,
          action_type: 'defend',
        },
        {
          headers: { Authorization: `Bearer ${authToken2}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data.action).toBe('defend');
    });

    it('should use superpower in combat', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/action`,
        {
          combat_id: combatId,
          action_type: 'use_power',
          power_name: 'fireball',
          target: 'opponent',
        },
        {
          headers: { Authorization: `Bearer ${authToken1}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('power_effect');
    });
  });

  describe('Combat State', () => {
    it('should fetch current combat state', async () => {
      const response = await axios.get(`${API_URL}/api/combat/state?combat_id=${combatId}`, {
        headers: { Authorization: `Bearer ${authToken1}` },
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('combat_id', combatId);
      expect(response.data).toHaveProperty('turn');
      expect(response.data).toHaveProperty('player1_hp');
      expect(response.data).toHaveProperty('player2_hp');
    });

    it('should validate turn order', async () => {
      const response = await axios.get(`${API_URL}/api/combat/state?combat_id=${combatId}`, {
        headers: { Authorization: `Bearer ${authToken1}` },
      });

      expect(response.data.current_turn).toBeDefined();
      expect(['player1', 'player2']).toContain(response.data.current_turn);
    });
  });

  describe('Combat Completion', () => {
    it('should handle combat victory', async () => {
      // Simulate combat until one player wins
      // This would involve multiple attack actions
      const response = await axios.get(`${API_URL}/api/combat/state?combat_id=${combatId}`, {
        headers: { Authorization: `Bearer ${authToken1}` },
      });

      if (response.data.status === 'completed') {
        expect(response.data).toHaveProperty('winner');
        expect(response.data).toHaveProperty('rewards');
      }
    });

    it('should update player stats after combat', async () => {
      const statsResponse = await axios.get(`${API_URL}/api/combat/stats`, {
        headers: { Authorization: `Bearer ${authToken1}` },
      });

      expect(statsResponse.status).toBe(200);
      expect(statsResponse.data).toHaveProperty('total_battles');
      expect(statsResponse.data.total_battles).toBeGreaterThan(0);
    });
  });

  describe('Arena Mode', () => {
    it('should join arena queue', async () => {
      const response = await axios.post(
        `${API_URL}/api/combat/arena/join`,
        {},
        {
          headers: { Authorization: `Bearer ${authToken1}` },
        }
      );

      expect(response.status).toBe(200);
      expect(response.data.message).toContain('queue');
    });

    it('should fetch arena queue status', async () => {
      const response = await axios.get(`${API_URL}/api/combat/arena/queue`, {
        headers: { Authorization: `Bearer ${authToken1}` },
      });

      expect(response.status).toBe(200);
      expect(response.data).toHaveProperty('queue_position');
    });
  });
});
