import api from './api';

/**
 * Upgrade Service
 * Handles all upgrade-related API calls
 */
class UpgradeService {
  /**
   * Calculate upgrade cost based on current level
   * Uses exponential scaling formula
   */
  calculateUpgradeCost(currentLevel, upgradeType = 'trait') {
    const baseLevel = currentLevel || 1;
    
    // Base costs vary by type
    const baseCosts = {
      trait: { credits: 100, karma_tokens: 10, dark_matter: 1 },
      robot: { credits: 200, karma_tokens: 20, dark_matter: 2 },
      ornament: { credits: 150, karma_tokens: 15, dark_matter: 1 },
      chip: { credits: 250, karma_tokens: 25, dark_matter: 3 }
    };

    const base = baseCosts[upgradeType] || baseCosts.trait;
    
    // Exponential scaling: cost = base * (1.15 ^ level)
    const multiplier = Math.pow(1.15, baseLevel);
    
    return {
      credits: Math.floor(base.credits * multiplier),
      karma_tokens: Math.floor(base.karma_tokens * multiplier),
      dark_matter: Math.floor(base.dark_matter * multiplier)
    };
  }

  /**
   * Upgrade a trait
   */
  async upgradeTrait(traitId) {
    try {
      const response = await api.post('/api/upgrades/traits', { trait_id: traitId });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Upgrade a robot
   */
  async upgradeRobot(robotId) {
    try {
      const response = await api.post('/api/upgrades/robots', { robot_id: robotId });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Upgrade an ornament
   */
  async upgradeOrnament(ornamentId) {
    try {
      const response = await api.post('/api/upgrades/ornaments', { ornament_id: ornamentId });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Upgrade a chip
   */
  async upgradeChip(chipId) {
    try {
      const response = await api.post('/api/upgrades/chips', { chip_id: chipId });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get upgrade history
   */
  async getUpgradeHistory(upgradeType = null, limit = 10) {
    try {
      const params = new URLSearchParams();
      if (upgradeType) params.append('upgrade_type', upgradeType);
      params.append('limit', limit);
      
      const response = await api.get(`/api/upgrades/history?${params}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Get upgrade statistics
   */
  async getUpgradeStats() {
    try {
      const response = await api.get('/api/upgrades/stats');
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export const upgradeService = new UpgradeService();
export default upgradeService;