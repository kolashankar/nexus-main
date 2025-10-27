import React from "react";
import apiClient from '../api/client';

class SkillTreesService {
  /**
   * Get all skill trees for the current player
   */
  async getSkillTrees() {
    const response = await apiClient.get('/api/player/skill-trees');
    return response.data;
  }

  /**
   * Get skill tree summary
   */
  async getSkillTreeSummary() {
    const response = await apiClient.get('/api/player/skill-trees/summary');
    return response.data;
  }

  /**
   * Get a specific skill tree
   */
  async getSkillTree(traitName) {
    const response = await apiClient.get(`/api/player/skill-trees/${traitName}`);
    return response.data;
  }

  /**
   * Unlock a skill node
   */
  async unlockNode(request) {
    const response = await apiClient.post('/api/player/skill-trees/unlock-node', request);
    return response.data;
  }

  /**
   * Choose a branch path (A or B)
   */
  async chooseBranch(request) {
    const response = await apiClient.post('/api/player/skill-trees/choose-branch', request);
    return response.data;
  }

  /**
   * Calculate synergy bonuses
   */
  async calculateSynergies() {
    const response = await apiClient.get('/api/player/skill-trees/synergies/calculate');
    return response.data.synergies;
  }
}

export default new SkillTreesService();
