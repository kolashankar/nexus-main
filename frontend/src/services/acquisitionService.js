/**
 * Service for item acquisitions API calls
 */

import apiClient from '../api/client';

const acquisitionService = {
  /**
   * Get all acquisitions for the current player
   */
  async getAcquisitions(statusFilter = null) {
    const params = statusFilter ? { status_filter: statusFilter } : {};
    const response = await apiClient.get('/api/player/acquisitions', { params });
    return response.data;
  },

  /**
   * Get player's currently active acquisition
   */
  async getActiveAcquisition() {
    const response = await apiClient.get('/api/player/acquisitions/active');
    return response.data;
  },

  /**
   * Start acquiring a world item
   */
  async startAcquisition(worldItemId) {
    const response = await apiClient.post('/api/player/acquisitions/start', {
      world_item_id: worldItemId
    });
    return response.data;
  },

  /**
   * Claim a completed acquisition
   */
  async claimAcquisition(acquisitionId) {
    const response = await apiClient.post('/api/player/acquisitions/claim', {
      acquisition_id: acquisitionId
    });
    return response.data;
  },

  /**
   * Cancel an ongoing acquisition
   */
  async cancelAcquisition(acquisitionId) {
    const response = await apiClient.post(`/api/player/acquisitions/${acquisitionId}/cancel`);
    return response.data;
  }
};

export default acquisitionService;
