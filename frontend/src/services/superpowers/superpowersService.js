import React from "react";
import apiClient from '../api/client';

class SuperpowersService {
  /**
   * Get all superpowers for the current player
   */
  async getSuperpowers() {
    const response = await apiClient.get('/api/player/superpowers');
    return response.data;
  }

  /**
   * Get list of powers player can unlock
   */
  async getAvailablePowers() {
    const response = await apiClient.get('/api/player/superpowers/available');
    return response.data.available_powers;
  }

  /**
   * Get all superpower definitions
   */
  async getPowerDefinitions() {
    const response = await apiClient.get('/api/player/superpowers/definitions');
    return response.data.powers;
  }

  /**
   * Get a specific superpower definition
   */
  async getPowerDefinition(powerId) {
    const response = await apiClient.get(`/api/player/superpowers/definitions/${powerId}`);
    return response.data;
  }

  /**
   * Unlock a superpower
   */
  async unlockPower(powerId) {
    const response = await apiClient.post('/api/player/superpowers/unlock', { power_id: powerId });
    return response.data;
  }

  /**
   * Equip a superpower
   */
  async equipPower(powerId) {
    const response = await apiClient.post('/api/player/superpowers/equip', { power_id: powerId });
    return response.data;
  }

  /**
   * Unequip a superpower
   */
  async unequipPower(powerId) {
    const response = await apiClient.post(`/api/player/superpowers/unequip/${powerId}`);
    return response.data;
  }

  /**
   * Use a superpower
   */
  async usePower(powerId) {
    const response = await apiClient.post('/api/player/superpowers/use', { power_id: powerId });
    return response.data;
  }
}

export default new SuperpowersService();
