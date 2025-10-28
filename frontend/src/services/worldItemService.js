/**
 * Service for world items API calls
 */

import apiClient from '../api/client';

const worldItemService = {
  /**
   * Get all active world items
   */
  async getActiveItems(region = null) {
    const params = region ? { region } : {};
    const response = await apiClient.get('/api/world/items/active', { params });
    return response.data;
  },

  /**
   * Get items near player's position
   */
  async getNearbyItems(position, radius = 50.0) {
    const response = await apiClient.post('/api/world/items/nearby', {
      x: position.x,
      y: position.y,
      z: position.z,
      radius
    });
    return response.data;
  },

  /**
   * Get detailed information about a specific item
   */
  async getItemDetails(itemId) {
    const response = await apiClient.get(`/api/world/items/${itemId}`);
    return response.data;
  },

  /**
   * Check if player can acquire an item
   */
  async canAcquire(itemId) {
    const response = await apiClient.post(`/api/world/items/${itemId}/can-acquire`);
    return response.data;
  },

  /**
   * Admin: Manually spawn an item (for testing)
   */
  async adminSpawnItem(itemType) {
    const response = await apiClient.post(`/api/world/items/admin/spawn/${itemType}`);
    return response.data;
  }
};

export default worldItemService;
