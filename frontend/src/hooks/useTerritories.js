import React from "react";
import { useState, useEffect, useCallback } from 'react';
import { worldService } from '@/services/api/worldService';

/**
 * Custom hook for managing territories
 */
export const useTerritories = () => {
  const [territories, setTerritories] = useState([]);
  const [contested, setContested] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTerritories = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [allTerritories, contestedTerritories] = await Promise.all([
        worldService.getAllTerritories(),
        worldService.getContestedTerritories(),
      ]);

      setTerritories(allTerritories.territories);
      setContested(contestedTerritories.territories);
    } catch (err) {
      setError(err.message || 'Failed to fetch territories');
      console.error('Error fetching territories', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTerritories();

    // Poll for updates every 2 minutes
    const interval = setInterval(fetchTerritories, 120000);

    return () => clearInterval(interval);
  }, [fetchTerritories]);

  const getTerritoryById = useCallback(
    (id) => {
      return territories.find((t) => t.territory_id === id);
    },
    [territories]
  );

  return {
    territories,
    contested,
    loading,
    error,
    refetch: fetchTerritories,
    getTerritoryById,
  };
};
