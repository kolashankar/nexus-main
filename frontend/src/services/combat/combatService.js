import React from "react";
import apiClient from '../api/client';

class CombatService {
  async challengePlayer(attackerId, defenderId, battleType = 'duel') {
    const response = await apiClient.post('/api/combat/challenge', {
      attacker_id: attackerId,
      defender_id: defenderId,
      battle_type: battleType,
    });
    return response.data;
  }

  async acceptChallenge(battleId) {
    const response = await apiClient.post(`/api/combat/accept/${battleId}`);
    return response.data;
  }

  async declineChallenge(battleId) {
    const response = await apiClient.post(`/api/combat/decline/${battleId}`);
    return response.data;
  }

  async getActiveBattles(playerId) {
    const response = await apiClient.get('/api/combat/active', {
      params: { player_id: playerId },
    });
    return response.data;
  }

  async executeAction(battleId, actorId, actionType, targetId, abilityName) {
    const response = await apiClient.post('/api/combat/action', {
      battle_id: battleId,
      actor_id: actorId,
      action_type: actionType,
      target_id: targetId,
      ability_name: abilityName,
    });
    return response.data;
  }

  async getBattleState(battleId) {
    const response = await apiClient.get(`/api/combat/state/${battleId}`);
    return response.data;
  }

  async fleeBattle(battleId, playerId) {
    const response = await apiClient.post(`/api/combat/flee/${battleId}`, null, {
      params: { player_id: playerId },
    });
    return response.data;
  }

  async getCombatHistory(playerId, limit = 10) {
    const response = await apiClient.get('/api/combat/history', {
      params: { player_id: playerId, limit },
    });
    return response.data;
  }

  async getCombatStats(playerId) {
    const response = await apiClient.get(`/api/combat/stats/${playerId}`);
    return response.data;
  }

  // Duel specific
  async challengeToDuel(attackerId, defenderId) {
    const response = await apiClient.post('/api/combat/duel/challenge', {
      attacker_id: attackerId,
      defender_id: defenderId,
      battle_type: 'duel',
    });
    return response.data;
  }

  async getPendingDuels(playerId) {
    const response = await apiClient.get(`/api/combat/duel/pending/${playerId}`);
    return response.data;
  }

  // Arena specific
  async joinArenaQueue(playerId, ranked = false) {
    const response = await apiClient.post('/api/combat/arena/join', null, {
      params: { player_id: playerId, ranked },
    });
    return response.data;
  }

  async leaveArenaQueue(playerId) {
    const response = await apiClient.post('/api/combat/arena/leave', null, {
      params: { player_id: playerId },
    });
    return response.data;
  }

  async getQueueStatus(playerId) {
    const response = await apiClient.get('/api/combat/arena/queue', {
      params: { player_id: playerId },
    });
    return response.data;
  }

  async getArenaLeaderboard(limit = 100) {
    const response = await apiClient.get('/api/combat/arena/leaderboard', {
      params: { limit },
    });
    return response.data;
  }
}

export default new CombatService();
