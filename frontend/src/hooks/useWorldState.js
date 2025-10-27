import React from "react";
import { useState, useEffect, useCallback } from 'react';
import { worldService } from '@/services/api/worldService';

/**
 * Custom hook for managing world state
 */
export const useWorldState = () => {
  const [worldState, setWorldState] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchWorldState = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const state = await worldService.getWorldState();
      setWorldState(state);
    } catch (err) {
      setError(err.message || 'Failed to fetch world state');
      console.error('Error fetching world state', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchWorldState();

    // Poll for updates every 60 seconds
    const interval = setInterval(fetchWorldState, 60000);

    return () => clearInterval(interval);
  }, [fetchWorldState]);

  return {
    worldState,
    loading,
    error,
    refetch: fetchWorldState,
  };
};
