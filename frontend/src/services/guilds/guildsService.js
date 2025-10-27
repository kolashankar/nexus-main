import React from "react";
import apiClient from '../api/client';

class GuildsService {
  async createGuild(name, tag, description) {
    const response = await apiClient.post('/api/guilds', { name, tag, description });
    return response.data;
  }

  async listGuilds(skip = 0, limit = 20) {
    const response = await apiClient.get('/api/guilds', { params: { skip, limit } });
    return response.data;
  }

  async getGuild(guildId) {
    const response = await apiClient.get(`/api/guilds/${guildId}`);
    return response.data;
  }

  async joinGuild(guildId) {
    const response = await apiClient.post(`/api/guilds/${guildId}/join`);
    return response.data;
  }

  async leaveGuild() {
    const response = await apiClient.post('/api/guilds/leave');
    return response.data;
  }

  async getGuildMembers(guildId) {
    const response = await apiClient.get(`/api/guilds/${guildId}/members`);
    return response.data;
  }

  async kickMember(playerId) {
    const response = await apiClient.post('/api/guilds/management/kick', { player_id: playerId });
    return response.data;
  }

  async promoteMember(playerId, newRank) {
    const response = await apiClient.post('/api/guilds/management/promote', {
      player_id: playerId,
      new_rank: newRank,
    });
    return response.data;
  }

  async contributeToBank(credits) {
    const response = await apiClient.post('/api/guilds/management/contribute', { credits });
    return response.data;
  }

  async getGuildBank() {
    const response = await apiClient.get('/api/guilds/management/bank');
    return response.data;
  }

  // Territories
  async getAllTerritories() {
    const response = await apiClient.get('/api/guilds/territories');
    return response.data;
  }

  async getTerritory(territoryId) {
    const response = await apiClient.get(`/api/guilds/territories/${territoryId}`);
    return response.data;
  }

  async getMyGuildTerritories() {
    const response = await apiClient.get('/api/guilds/territories/guild/my-territories');
    return response.data;
  }

  async attackTerritory(territoryId) {
    const response = await apiClient.post(`/api/guilds/territories/${territoryId}/attack`);
    return response.data;
  }

  async defendTerritory(territoryId) {
    const response = await apiClient.post(`/api/guilds/territories/${territoryId}/defend`);
    return response.data;
  }

  // Wars
  async declareWar(defenderGuildId, targetTerritory) {
    const response = await apiClient.post('/api/guilds/wars/declare', {
      defender_guild_id: defenderGuildId,
      target_territory: targetTerritory,
    });
    return response.data;
  }

  async getMyGuildWars() {
    const response = await apiClient.get('/api/guilds/wars/my-wars');
    return response.data;
  }

  async getWar(warId) {
    const response = await apiClient.get(`/api/guilds/wars/${warId}`);
    return response.data;
  }

  async offerPeace(warId, terms) {
    const response = await apiClient.post('/api/guilds/wars/peace/offer', { war_id: warId, terms });
    return response.data;
  }

  async acceptPeace(warId) {
    const response = await apiClient.post(`/api/guilds/wars/peace/${warId}/accept`);
    return response.data;
  }

  async rejectPeace(warId) {
    const response = await apiClient.post(`/api/guilds/wars/peace/${warId}/reject`);
    return response.data;
  }
}

export default new GuildsService();
