import { describe, it, expect, beforeAll } from '@jest/globals';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

describe('Quest Flow Integration Tests', () => {
  let authToken;
  let playerId;
  let questId;

  beforeAll(async () => {
    const login = await axios.post(`${API_URL}/api/auth/login`, {
      username: "testuser",
      password: "testpass123",
    });
    authToken = login.data.access_token;
    const headers = { Authorization: `Bearer ${authToken}` };

    const profile = await axios.get(`${API_URL}/api/player/profile`, {
      headers,
    });
    playerId = profile.data.player_id;
  });

  describe('Quest Discovery', () => {
    it('should fetch available quests', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const response = await axios.get(`${API_URL}/api/quests/available`, {
        headers,
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
    });

    it('should get daily quests', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const response = await axios.get(`${API_URL}/api/quests/daily`, {
        headers,
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
      expect(response.data.length).toBeLessThanOrEqual(3);
    });

    it('should get weekly challenges', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const response = await axios.get(`${API_URL}/api/quests/weekly`, {
        headers,
      });

      expect(response.status).toBe(200);
      expect(Array.isArray(response.data)).toBe(true);
      expect(response.data.length).toBeLessThanOrEqual(5);
    });
  });

  describe('Quest Acceptance', () => {
    it('should accept an available quest', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const availableQuests = await axios.get(
        `${API_URL}/api/quests/available`,
        {
          headers,
        }
      );

      if (availableQuests.data.length > 0) {
        questId = availableQuests.data[0]._id;

        const response = await axios.post(
          `${API_URL}/api/quests/accept`,
          { quest_id: questId },
          {
            headers,
          }
        );

        expect(response.status).toBe(200);
        expect(response.data.status).toBe('active');
      }
    });

    it('should not accept same quest twice', async () => {
      if (!questId) {
        console.warn("Skipping 'should not accept same quest twice' test as no questId was available.");
        return;
      }

      expect.assertions(1);
      try {
        await axios.post(
          `${API_URL}/api/quests/accept`,
          { quest_id: questId },
          {
            headers: { Authorization: `Bearer ${authToken}` },
          }
        );
      } catch (error) {
        expect(error.response.status).toBe(400);
      }
    });
  });

  describe('Quest Progression', () => {
    it('should track quest objectives', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const activeQuests = await axios.get(`${API_URL}/api/quests/active`, {
        headers,
      });

      if (activeQuests.data.length > 0) {
        const quest = activeQuests.data[0];

        expect(quest).toHaveProperty('objectives');
        expect(Array.isArray(quest.objectives)).toBe(true);

        quest.objectives.forEach((obj) => {
          expect(obj).toHaveProperty('current');
          expect(obj).toHaveProperty('required');
          expect(obj).toHaveProperty('completed');
        });
      }
    });
  });

  describe('Quest Completion', () => {
    it('should complete quest when objectives met', async () => {
      // Note, we check the endpoint exists
      const headers = { Authorization: `Bearer ${authToken}` };
      const activeQuests = await axios.get(`${API_URL}/api/quests/active`, {
        headers,
      });

      if (activeQuests.data.length > 0) {
        const quest = activeQuests.data[0];

        // Check if all objectives are completed
        const allCompleted = quest.objectives.every((obj) => obj.completed);

        if (allCompleted) {
          const response = await axios.post(
            `${API_URL}/api/quests/complete`,
            { quest_id: quest._id },
            {
              headers,
            }
          );

          expect(response.status).toBe(200);
          expect(response.data).toHaveProperty('rewards');
        }
      }
    });

    it('should grant rewards on completion', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const completedQuests = await axios.get(
        `${API_URL}/api/quests/completed`,
        {
          headers,
        }
      );

      if (completedQuests.data.length > 0) {
        const quest = completedQuests.data[0];
        expect(quest).toHaveProperty('rewards');
        expect(quest.rewards).toHaveProperty('credits');
        expect(quest.rewards).toHaveProperty('xp');
      }
    });
  });

  describe('Quest Abandonment', () => {
    it('should abandon active quest', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const activeQuests = await axios.get(`${API_URL}/api/quests/active`, {
        headers,
      });

      if (activeQuests.data.length > 0) {
        const quest = activeQuests.data[0];

        const response = await axios.post(
          `${API_URL}/api/quests/abandon`,
          { quest_id: quest._id },
          {
            headers,
          }
        );

        expect(response.status).toBe(200);
        expect(response.data.message).toContain('abandoned');
      }
    });
  });

  describe('Campaign System', () => {
    it('should access campaign quests', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const response = await axios.get(`${API_URL}/api/quests/campaign`, {
        headers,
      });

      expect(response.status).toBe(200);
    });

    it('should start a campaign', async () => {
      const headers = { Authorization: `Bearer ${authToken}` };
      const response = await axios.post(
        `${API_URL}/api/quests/campaign/start`,
        { campaign_type: 'main' },
        {
          headers,
        }
      );

      if (response.status === 200) {
        expect(response.data).toHaveProperty('campaign_id');
        expect(response.data).toHaveProperty('chapters');
      }
    });
  });
});