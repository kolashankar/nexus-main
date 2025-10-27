import React from "react";
import apiClient from '../api/client';

class PrestigeService {
  /**
   * Get prestige information for the current player
   */
  async getPrestige() {
    const response = await apiClient.get('/api/player/prestige');
    return response.data;
  }

  /**
   * Get current prestige benefits
   */
  async getPrestigeBenefits() {
    const response = await apiClient.get('/api/player/prestige/benefits');
    return response.data;
  }

  /**
   * Check if player can prestige
   */
  async checkPrestigeEligibility() {
    const response = await apiClient.get('/api/player/prestige/eligibility');
    return response.data;
  }

  /**
   * Perform prestige reset
   */
  async performPrestige() {
    const response = await apiClient.post('/api/player/prestige/perform');
    return response.data;
  }

  /**
   * Get all prestige rewards
   */
  async getPrestigeRewards() {
    const response = await apiClient.get('/api/player/prestige/rewards');
    return response.data.rewards;
  }

  /**
   * Get rewards for a specific prestige level
   */
  async getPrestigeReward(level) {
    const response = await apiClient.get(`/api/player/prestige/rewards/${level}`);
    return response.data;
  }

  /**
   * Get prestige history
   */
  async getPrestigeHistory() {
    const response = await apiClient.get('/api/player/prestige/history');
    return response.data;
  }
}

export default new PrestigeService();
