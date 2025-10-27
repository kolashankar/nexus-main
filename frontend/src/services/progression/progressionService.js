import React from "react";
import api from '@/services/api/client';

class ProgressionService {
  async getProgressionData() {
    const response = await api.get('/player/progression');
    return response.data;
  }

  async gainXP(amount) {
    const response = await api.post('/player/progression/xp', { amount });
    return response.data;
  }

  async unlockSkillNode(trait, nodeId) {
    const response = await api.post('/player/skill-trees/unlock', {
      trait,
      node_id: nodeId,
    });
    return response.data;
  }

  async getSkillTree(trait) {
    const response = await api.get(`/player/skill-trees/${trait}`);
    return response.data;
  }

  async activateSuperpower(powerId) {
    const response = await api.post('/player/superpowers/activate', {
      power_id: powerId,
    });
    return response.data;
  }

  async getSuperpowers() {
    const response = await api.get('/player/superpowers');
    return response.data;
  }

  async getAchievements() {
    const response = await api.get('/achievements');
    return response.data;
  }

  async unlockAchievement(achievementId) {
    const response = await api.post('/achievements/unlock', {
      achievement_id: achievementId,
    });
    return response.data;
  }

  async prestige() {
    const response = await api.post('/player/prestige');
    return response.data;
  }

  async getPrestigeInfo() {
    const response = await api.get('/player/prestige/info');
    return response.data;
  }

  async getLegacyPerks() {
    const response = await api.get('/player/legacy/perks');
    return response.data;
  }

  async purchaseLegacyPerk(perkId) {
    const response = await api.post('/player/legacy/perks/purchase', {
      perk_id: perkId,
    });
    return response.data;
  }
}

export const progressionService = new ProgressionService();
