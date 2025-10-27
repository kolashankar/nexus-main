import React from "react";
import apiClient from '../api/client';

class SocialService {
  // General social
  async getNearbyPlayers(limit = 20) {
    const response = await apiClient.get('/api/social/nearby', { params: { limit } });
    return response.data;
  }

  async getOnlinePlayers(skip = 0, limit = 20) {
    const response = await apiClient.get('/api/social/online', { params: { skip, limit } });
    return response.data;
  }

  async getMyRelationships(type) {
    const params = type ? { type } : {};
    const response = await apiClient.get('/api/social/relationships', { params });
    return response.data;
  }

  async getPlayerProfile(playerId) {
    const response = await apiClient.get(`/api/social/players/${playerId}`);
    return response.data;
  }

  // Alliances
  async createAlliance(allianceName) {
    const response = await apiClient.post('/api/social/alliances', { alliance_name: allianceName });
    return response.data;
  }

  async getMyAlliance() {
    const response = await apiClient.get('/api/social/alliances/my-alliance');
    return response.data;
  }

  async addAllianceMember(playerId) {
    const response = await apiClient.post('/api/social/alliances/add-member', { player_id: playerId });
    return response.data;
  }

  async leaveAlliance() {
    const response = await apiClient.delete('/api/social/alliances/leave');
    return response.data;
  }

  async disbandAlliance() {
    const response = await apiClient.delete('/api/social/alliances/disband');
    return response.data;
  }

  // Marriage
  async proposeMarriage(playerId) {
    const response = await apiClient.post('/api/social/marriage/propose', { player_id: playerId });
    return response.data;
  }

  async getPendingProposals() {
    const response = await apiClient.get('/api/social/marriage/proposals');
    return response.data;
  }

  async acceptProposal(proposalId) {
    const response = await apiClient.post(`/api/social/marriage/proposals/${proposalId}/accept`);
    return response.data;
  }

  async rejectProposal(proposalId) {
    const response = await apiClient.post(`/api/social/marriage/proposals/${proposalId}/reject`);
    return response.data;
  }

  async getMyMarriage() {
    const response = await apiClient.get('/api/social/marriage/my-marriage');
    return response.data;
  }

  async divorce() {
    const response = await apiClient.post('/api/social/marriage/divorce');
    return response.data;
  }

  // Mentorship
  async requestMentorship(mentorId) {
    const response = await apiClient.post('/api/social/mentorship/request', { mentor_id: mentorId });
    return response.data;
  }

  async getPendingMentorshipRequests() {
    const response = await apiClient.get('/api/social/mentorship/requests');
    return response.data;
  }

  async acceptMentorshipRequest(requestId) {
    const response = await apiClient.post(`/api/social/mentorship/requests/${requestId}/accept`);
    return response.data;
  }

  async rejectMentorshipRequest(requestId) {
    const response = await apiClient.post(`/api/social/mentorship/requests/${requestId}/reject`);
    return response.data;
  }

  async getMyMentorship(asMentor = false) {
    const response = await apiClient.get('/api/social/mentorship/my-mentorship', {
      params: { as_mentor: asMentor },
    });
    return response.data;
  }

  async graduateApprentice() {
    const response = await apiClient.post('/api/social/mentorship/graduate');
    return response.data;
  }

  async completeLesson() {
    const response = await apiClient.post('/api/social/mentorship/lesson/complete');
    return response.data;
  }

  async listAvailableMentors(skip = 0, limit = 20) {
    const response = await apiClient.get('/api/social/mentorship/mentors', { params: { skip, limit } });
    return response.data;
  }
}

export default new SocialService();
