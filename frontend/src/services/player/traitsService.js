import React from "react";
import apiClient from '../api/client';

class TraitsService {
  async getAllTraits() {
    const response = await apiClient.get('/api/player/traits/');
    return response.data;
  }

  async getBaseTraits() {
    const response = await apiClient.get('/api/player/traits/base');
    return response.data;
  }

  async getMetaTraits() {
    const response = await apiClient.get('/api/player/traits/meta');
    return response.data;
  }

  async getTopTraits(limit = 10) {
    const response = await apiClient.get(`/api/player/traits/top?limit=${limit}`);
    return response.data;
  }

  async getBottomTraits(limit = 10) {
    const response = await apiClient.get(`/api/player/traits/bottom?limit=${limit}`);
    return response.data;
  }

  async getTraitDetails(traitName) {
    const response = await apiClient.get(`/api/player/traits/${traitName}`);
    return response.data;
  }

  async allocateTraitPoints(traitName, points) {
    const response = await apiClient.put('/api/player/traits/allocate', {
      trait_name: traitName,
      points,
    });
    return response.data;
  }
}

export default new TraitsService();
