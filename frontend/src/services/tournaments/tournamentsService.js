import React from "react";
import apiClient from '../api/client';

class TournamentsService {
  async getActiveTournaments() {
    const response = await apiClient.get('/api/tournaments/active');
    return response.data;
  }

  async registerForTournament(tournamentId, playerId) {
    const response = await apiClient.post('/api/tournaments/register', {
      tournament_id: tournamentId,
      player_id: playerId,
    });
    return response.data;
  }

  async getTournament(tournamentId) {
    const response = await apiClient.get(`/api/tournaments/${tournamentId}`);
    return response.data;
  }

  async getTournamentBracket(tournamentId) {
    const response = await apiClient.get(`/api/tournaments/${tournamentId}/bracket`);
    return response.data;
  }

  async getMyMatch(tournamentId, playerId) {
    const response = await apiClient.get(`/api/tournaments/${tournamentId}/my-match`, {
      params: { player_id: playerId },
    });
    return response.data;
  }

  async getTournamentHistory(playerId, limit = 10) {
    const params = playerId ? { player_id: playerId, limit } : { limit };
    const response = await apiClient.get('/api/tournaments/history', {
      params,
    });
    return response.data;
  }
}

export default new TournamentsService();
