import React from "react";
import apiClient from '../api/client';

class PlayerService {
  async getProfile() {
    const response = await apiClient.get('/api/player/profile');
    return response.data;
  }

  async updateProfile(updates) {
    const response = await apiClient.put('/api/player/profile', updates);
    return response.data;
  }

  async getPlayerProfile(playerId) {
    const response = await apiClient.get(`/api/player/profile/${playerId}`);
    return response.data;
  }

  async getPlayerStats() {
    const response = await apiClient.get('/api/player/stats');
    return response.data;
  }

  async getCurrencies() {
    const response = await apiClient.get('/api/player/currencies');
    return response.data;
  }

  async getNearbyPlayers(limit = 10) {
    const response = await apiClient.get(`/api/player/nearby?limit=${limit}`);
    return response.data;
  }
}

export default new PlayerService();
