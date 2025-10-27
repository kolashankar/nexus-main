import React from "react";
import apiClient from '../api/client';

class AchievementsService {
  /**
   * Get all achievements for the current player
   */
  async getAchievements() {
    const response = await apiClient.get('/api/achievements');
    return response.data;
  }

  /**
   * Get achievement summary
   */
  async getAchievementSummary() {
    const response = await apiClient.get('/api/achievements/summary');
    return response.data;
  }

  /**
   * Get unlocked achievements
   */
  async getUnlockedAchievements() {
    const response = await apiClient.get('/api/achievements/unlocked');
    return response.data.unlocked;
  }

  /**
   * Get achievement progress
   */
  async getAchievementProgress() {
    const response = await apiClient.get('/api/achievements/progress');
    return response.data.progress;
  }

  /**
   * Get achievement definitions with optional filters
   */
  async getAchievementDefinitions(category, rarity) {
    let url = '/achievements/definitions';
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    if (rarity) params.append('rarity', rarity);
    if (params.toString()) url += `?${params.toString()}`;

    const response = await apiClient.get(url);
    return response.data.achievements;
  }

  /**
   * Get a specific achievement definition
   */
  async getAchievementDefinition(achievementId) {
    const response = await apiClient.get(`/api/achievements/definitions/${achievementId}`);
    return response.data;
  }

  /**
   * Get achievements by category
   */
  async getAchievementsByCategory(category) {
    const response = await apiClient.get(`/api/achievements/category/${category}`);
    return response.data;
  }

  /**
   * Unlock an achievement (usually called by system)
   */
  async unlockAchievement(achievementId) {
    const response = await apiClient.post(`/api/achievements/unlock/${achievementId}`);
    return response.data;
  }

  /**
   * Update progress towards an achievement
   */
  async updateAchievementProgress(achievementId, progressAmount) {
    const response = await apiClient.post('/api/achievements/progress/update', {
      achievement_id: achievementId,
      progress_amount: progressAmount,
    });
    return response.data;
  }

  /**
   * Get recently unlocked achievements
   */
  async getRecentUnlocks() {
    const response = await apiClient.get('/api/achievements/recent');
    return response.data.recent;
  }
}

export default new AchievementsService();
