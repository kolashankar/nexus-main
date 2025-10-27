import React from "react";
import { apiClient } from './api/client';

class QuestService {
  async getAvailableQuests(questType) {
    const params = questType ? { quest_type: questType } : {};
    const response = await apiClient.get('/api/quests/available', { params });
    return response.data.quests;
  }

  async getActiveQuests() {
    const response = await apiClient.get('/api/quests/active');
    return response.data.quests;
  }

  async getCompletedQuests() {
    const response = await apiClient.get('/api/quests/completed');
    return response.data.quests;
  }

  async acceptQuest(questId) {
    const response = await apiClient.post('/api/quests/accept', { quest_id: questId });
    return response.data;
  }

  async abandonQuest(questId) {
    const response = await apiClient.post('/api/quests/abandon', { quest_id: questId });
    return response.data.success;
  }

  async getQuestDetails(questId) {
    const response = await apiClient.get(`/api/quests/${questId}`);
    return response.data.quest;
  }

  async getDailyQuests() {
    const response = await apiClient.get('/api/quests/daily');
    return response.data.quests;
  }

  async getWeeklyQuests() {
    const response = await apiClient.get('/api/quests/weekly');
    return response.data.quests;
  }

  async getWorldQuests() {
    const response = await apiClient.get('/api/quests/world');
    return response.data.quests;
  }

  async getGuildQuests() {
    const response = await apiClient.get('/api/quests/guild');
    return response.data;
  }

  async joinGuildQuest(questId) {
    const response = await apiClient.post(`/api/quests/guild/${questId}/join`);
    return response.data;
  }

  async getDiscoveredHiddenQuests() {
    const response = await apiClient.get('/api/quests/hidden/discovered');
    return response.data.quests;
  }

  async getHiddenQuestHints() {
    const response = await apiClient.get('/api/quests/hidden/hints');
    return response.data.hints;
  }

  async getCampaigns(status) {
    const params = status ? { status } : {};
    const response = await apiClient.get('/api/quests/campaigns', { params });
    return response.data.campaigns;
  }

  async startCampaign(campaignId) {
    const response = await apiClient.post('/api/quests/campaigns/start', {
      campaign_id: campaignId,
    });
    return response.data;
  }

  async getCurrentChapter(campaignId) {
    const response = await apiClient.get(`/api/quests/campaigns/${campaignId}/current`);
    return response.data.chapter;
  }

  async makeCampaignChoice(campaignId, choiceId) {
    const response = await apiClient.post('/api/quests/campaigns/choice', {
      campaign_id: campaignId,
      choice_id: choiceId,
    });
    return response.data;
  }

  async completeChapter(campaignId) {
    const response = await apiClient.post(`/api/quests/campaigns/${campaignId}/complete-chapter`);
    return response.data;
  }

  async getQuestStats() {
    const response = await apiClient.get('/api/quests/stats');
    return response.data.stats;
  }
}

export const questService = new QuestService();
