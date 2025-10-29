"""Advanced tasks service for frontend."""

import axios from 'axios';

const API_URL = import.meta.env.VITE_REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

class AdvancedTaskService {
  /**
   * Generate advanced tasks of specific type
   */
  async generateTasks(taskType, count = 1) {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/tasks/advanced-tasks/generate`,
      { task_type: taskType, count },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Get appropriate difficulties for player
   */
  async getAppropriateDifficulties() {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/api/tasks/advanced-tasks/difficulty/appropriate`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Validate skill requirements
   */
  async validateSkillRequirements(skillRequirements) {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/tasks/advanced-tasks/skills/validate`,
      { skill_requirements: skillRequirements },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Get player's skill levels
   */
  async getSkillLevels() {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/api/tasks/advanced-tasks/skills/levels`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Get daily tasks
   */
  async getDailyTasks() {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/api/tasks/daily`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Check task cooldowns
   */
  async getTaskCooldowns() {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/api/tasks/cooldowns`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Get nearby locations
   */
  async getNearbyLocations(playerPosition) {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/tasks/locations/nearby`,
      { player_position: playerPosition },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }

  /**
   * Get all game locations
   */
  async getAllLocations() {
    const token = localStorage.getItem('token');
    const response = await axios.get(
      `${API_URL}/api/tasks/locations/all`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  }
}

export default new AdvancedTaskService();
