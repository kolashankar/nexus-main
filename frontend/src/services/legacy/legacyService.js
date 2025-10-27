import React from "react";
import apiClient from '../api/client';

class LegacyService {
  /**
   * Get legacy information for the current account
   */
  async getLegacy() {
    const response = await apiClient.get('/api/player/legacy');
    return response.data;
  }

  /**
   * Get legacy system summary
   */
  async getLegacySummary() {
    const response = await apiClient.get('/api/player/legacy/summary');
    return response.data;
  }

  /**
   * Get all available legacy perks
   */
  async getAvailablePerks() {
    const response = await apiClient.get('/api/player/legacy/perks');
    return response.data.perks;
  }

  /**
   * Get unlocked perks
   */
  async getUnlockedPerks() {
    const response = await apiClient.get('/api/player/legacy/perks/unlocked');
    return response.data.unlocked_perks;
  }

  /**
   * Get active perks
   */
  async getActivePerks() {
    const response = await apiClient.get('/api/player/legacy/perks/active');
    return response.data.active_perks;
  }

  /**
   * Unlock a legacy perk
   */
  async unlockPerk(perkId) {
    const response = await apiClient.post('/api/player/legacy/perks/unlock', { perk_id: perkId });
    return response.data;
  }

  /**
   * Activate a legacy perk
   */
  async activatePerk(perkId) {
    const response = await apiClient.post('/api/player/legacy/perks/activate', { perk_id: perkId });
    return response.data;
  }

  /**
   * Deactivate a legacy perk
   */
  async deactivatePerk(perkId) {
    const response = await apiClient.post(`/api/player/legacy/perks/deactivate/${perkId}`);
    return response.data;
  }

  /**
   * Earn legacy points
   */
  async earnLegacyPoints(amount, source) {
    const response = await apiClient.post('/api/player/legacy/points/earn', { amount, source });
    return response.data;
  }

  /**
   * Get legacy titles
   */
  async getLegacyTitles() {
    const response = await apiClient.get('/api/player/legacy/titles');
    return response.data.titles;
  }

  /**
   * Activate a legacy title
   */
  async activateTitle(titleId) {
    const response = await apiClient.post(`/api/player/legacy/titles/activate/${titleId}`);
    return response.data;
  }

  /**
   * Get heirloom items
   */
  async getHeirlooms() {
    const response = await apiClient.get('/api/player/legacy/heirlooms');
    return response.data.heirlooms;
  }

  /**
   * Get mentorship statistics
   */
  async getMentorshipStats() {
    const response = await apiClient.get('/api/player/legacy/mentorship');
    return response.data;
  }

  /**
   * Get bonuses that apply to new characters
   */
  async getNewCharacterBonuses() {
    const response = await apiClient.get('/api/player/legacy/new-character-bonuses');
    return response.data.bonuses;
  }
}

export default new LegacyService();
