import React from "react";
import { apiClient } from './client';

class WorldService {
  /**
   * Get currently active global event
   */
  async getActiveEvent() {
    try {
      const response = await apiClient.get('/api/world/events/active');
      return response.data;
    } catch (error) {
      console.error('Error fetching active event', error);
      return null;
    }
  }

  /**
   * Get recent world events
   */
  async getRecentEvents(limit = 10) {
    const response = await apiClient.get(`/api/world/events/recent?limit=${limit}`);
    return response.data;
  }

  /**
   * Get event by ID
   */
  async getEventById(eventId) {
    const response = await apiClient.get(`/api/world/events/${eventId}`);
    return response.data;
  }

  /**
   * Participate in an event
   */
  async participateInEvent(eventId) {
    const response = await apiClient.post('/api/world/events/participate', {
      event_id: eventId,
    });
    return response.data;
  }

  /**
   * Get regional events for a territory
   */
  async getTerritoryEvents(territoryId) {
    const response = await apiClient.get(`/api/world/events/territory/${territoryId}`);
    return response.data;
  }

  /**
   * Get current world state
   */
  async getWorldState() {
    const response = await apiClient.get('/api/world/state/current');
    return response.data;
  }

  /**
   * Get karma statistics
   */
  async getKarmaStatistics() {
    const response = await apiClient.get('/api/world/state/karma');
    return response.data;
  }

  /**
   * Get top karma players
   */
  async getTopKarmaPlayers(limit = 10) {
    const response = await apiClient.get(`/api/world/state/karma/top?limit=${limit}`);
    return response.data;
  }

  /**
   * Get bottom karma players
   */
  async getBottomKarmaPlayers(limit = 10) {
    const response = await apiClient.get(`/api/world/state/karma/bottom?limit=${limit}`);
    return response.data;
  }

  /**
   * Get all territories
   */
  async getAllTerritories() {
    const response = await apiClient.get('/api/world/territories/all');
    return response.data;
  }

  /**
   * Get contested territories
   */
  async getContestedTerritories() {
    const response = await apiClient.get('/api/world/territories/contested');
    return response.data;
  }

  /**
   * Get territory by ID
   */
  async getTerritoryById(territoryId) {
    const response = await apiClient.get(`/api/app/world/territories/${territoryId}`);
    return response.data;
  }

  /**
   * Get territories controlled by a guild
   */
  async getGuildTerritories(guildId) {
    const response = await apiClient.get(`/api/world/territories/guild/${guildId}`);
    return response.data;
  }

  /**
   * Initialize territories (admin)
   */
  async initializeTerritories() {
    const response = await apiClient.post('/api/world/territories/initialize');
    return response.data;
  }
}

export const worldService = new WorldService();
