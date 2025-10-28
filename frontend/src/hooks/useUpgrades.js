import { useState, useCallback } from 'react';
import { useAuth } from '@/contexts/AuthContext';
import api from '@/services/api';

/**
 * useUpgrades Hook
 * Manages upgrade-related state and API calls
 */
export const useUpgrades = () => {
  const { user } = useAuth();
  const [player, setPlayer] = useState(null);
  const [currencies, setCurrencies] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch player data including upgrades
  const refreshPlayer = useCallback(async () => {
    if (!user) {
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);

      // Fetch player profile
      const profileResponse = await api.get('/api/player/profile');
      setPlayer(profileResponse.data);

      // Fetch currencies
      const currenciesResponse = await api.get('/api/player/currencies');
      setCurrencies(currenciesResponse.data);

    } catch (err) {
      console.error('Failed to fetch player data:', err);
      setError(err.response?.data?.detail || 'Failed to load player data');
    } finally {
      setLoading(false);
    }
  }, [user]);

  // Get upgrade history
  const getUpgradeHistory = useCallback(async (upgradeType = null, limit = 10) => {
    try {
      const params = new URLSearchParams();
      if (upgradeType) params.append('upgrade_type', upgradeType);
      params.append('limit', limit);

      const response = await api.get(`/api/upgrades/history?${params}`);
      return response.data;
    } catch (err) {
      console.error('Failed to fetch upgrade history:', err);
      throw err;
    }
  }, []);

  // Get upgrade statistics
  const getUpgradeStats = useCallback(async () => {
    try {
      const response = await api.get('/api/upgrades/stats');
      return response.data;
    } catch (err) {
      console.error('Failed to fetch upgrade stats:', err);
      throw err;
    }
  }, []);

  return {
    player,
    currencies,
    loading,
    error,
    refreshPlayer,
    getUpgradeHistory,
    getUpgradeStats
  };
};