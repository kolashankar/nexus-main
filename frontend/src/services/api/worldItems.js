/**
 * World Items API Service
 * Handles all API calls related to world items
 */

import apiClient from './client';

/**
 * Get all active world items
 * @param {string} region - Optional region filter
 * @returns {Promise} List of active items
 */
export const getActiveWorldItems = async (region = null) => {
  try {
    const params = region ? { region } : {};
    const response = await apiClient.get('/world/items/active', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching active world items:', error);
    throw error;
  }
};

/**
 * Get items near player's position
 * @param {object} position - Player position {x, y, z}
 * @param {number} radius - Search radius (default: 50)
 * @returns {Promise} List of nearby items
 */
export const getNearbyItems = async (position, radius = 50) => {
  try {
    const response = await apiClient.post('/world/items/nearby', {
      x: position.x,
      y: position.y,
      z: position.z,
      radius
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching nearby items:', error);
    throw error;
  }
};

/**
 * Get detailed information about a specific item
 * @param {string} itemId - Item ID
 * @returns {Promise} Item details
 */
export const getItemDetails = async (itemId) => {
  try {
    const response = await apiClient.get(`/world/items/${itemId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching item details:', error);
    throw error;
  }
};

/**
 * Check if player can acquire an item
 * @param {string} itemId - Item ID
 * @returns {Promise} Can acquire status
 */
export const checkCanAcquireItem = async (itemId) => {
  try {
    const response = await apiClient.post(`/world/items/${itemId}/can-acquire`);
    return response.data;
  } catch (error) {
    console.error('Error checking acquisition status:', error);
    throw error;
  }
};

/**
 * Start item acquisition process
 * @param {string} itemId - Item ID
 * @returns {Promise} Acquisition details
 */
export const startItemAcquisition = async (itemId) => {
  try {
    const response = await apiClient.post(`/world/items/${itemId}/acquire`);
    return response.data;
  } catch (error) {
    console.error('Error starting item acquisition:', error);
    throw error;
  }
};

/**
 * Get player's active acquisitions
 * @returns {Promise} List of active acquisitions
 */
export const getActiveAcquisitions = async () => {
  try {
    const response = await apiClient.get('/world/items/acquisitions/active');
    return response.data;
  } catch (error) {
    console.error('Error fetching active acquisitions:', error);
    throw error;
  }
};

/**
 * Claim a completed acquisition
 * @param {string} acquisitionId - Acquisition ID
 * @returns {Promise} Claim result
 */
export const claimAcquisition = async (acquisitionId) => {
  try {
    const response = await apiClient.post(`/world/items/acquisitions/${acquisitionId}/claim`);
    return response.data;
  } catch (error) {
    console.error('Error claiming acquisition:', error);
    throw error;
  }
};

/**
 * Cancel an active acquisition
 * @param {string} acquisitionId - Acquisition ID
 * @returns {Promise} Cancel result
 */
export const cancelAcquisition = async (acquisitionId) => {
  try {
    const response = await apiClient.post(`/world/items/acquisitions/${acquisitionId}/cancel`);
    return response.data;
  } catch (error) {
    console.error('Error canceling acquisition:', error);
    throw error;
  }
};

/**
 * Admin: Manually spawn an item (for testing)
 * @param {string} itemType - Type of item to spawn (skill, superpower_tool, meta_trait)
 * @returns {Promise} Spawned item details
 */
export const adminSpawnItem = async (itemType) => {
  try {
    const response = await apiClient.post(`/world/items/admin/spawn/${itemType}`);
    return response.data;
  } catch (error) {
    console.error('Error spawning item:', error);
    throw error;
  }
};

export default {
  getActiveWorldItems,
  getNearbyItems,
  getItemDetails,
  checkCanAcquireItem,
  startItemAcquisition,
  getActiveAcquisitions,
  claimAcquisition,
  cancelAcquisition,
  adminSpawnItem
};
