/**
 * React hook for world items
 */

import { useState, useEffect, useCallback } from 'react';
import worldItemService from '../services/worldItemService';
import acquisitionService from '../services/acquisitionService';
import { useToast } from './useToast';

export const useWorldItems = (playerPosition = null, autoRefresh = true) => {
  const [activeItems, setActiveItems] = useState([]);
  const [nearbyItems, setNearbyItems] = useState([]);
  const [activeAcquisition, setActiveAcquisition] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { toast } = useToast();

  // Fetch all active items
  const fetchActiveItems = useCallback(async (region = null) => {
    try {
      setLoading(true);
      const data = await worldItemService.getActiveItems(region);
      setActiveItems(data.items || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching active items:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch nearby items based on player position
  const fetchNearbyItems = useCallback(async (position, radius = 50.0) => {
    if (!position) return;

    try {
      const data = await worldItemService.getNearbyItems(position, radius);
      setNearbyItems(data.items || []);
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching nearby items:', err);
    }
  }, []);

  // Fetch active acquisition
  const fetchActiveAcquisition = useCallback(async () => {
    try {
      const data = await acquisitionService.getActiveAcquisition();
      setActiveAcquisition(data.active_acquisition);
    } catch (err) {
      console.error('Error fetching active acquisition:', err);
    }
  }, []);

  // Start acquiring an item
  const startAcquisition = useCallback(async (worldItemId) => {
    try {
      setLoading(true);
      const data = await acquisitionService.startAcquisition(worldItemId);
      setActiveAcquisition(data.acquisition);
      toast({
        title: "Acquisition Started",
        description: data.message,
        variant: "success"
      });
      
      // Refresh items
      if (playerPosition) {
        await fetchNearbyItems(playerPosition);
      }
      return true;
    } catch (err) {
      toast({
        title: "Acquisition Failed",
        description: err.response?.data?.detail || err.message,
        variant: "destructive"
      });
      return false;
    } finally {
      setLoading(false);
    }
  }, [playerPosition, fetchNearbyItems, toast]);

  // Claim a completed acquisition
  const claimAcquisition = useCallback(async (acquisitionId) => {
    try {
      setLoading(true);
      const data = await acquisitionService.claimAcquisition(acquisitionId);
      setActiveAcquisition(null);
      toast({
        title: "Item Acquired!",
        description: data.message,
        variant: "success"
      });
      return true;
    } catch (err) {
      toast({
        title: "Claim Failed",
        description: err.response?.data?.detail || err.message,
        variant: "destructive"
      });
      return false;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  // Cancel an ongoing acquisition
  const cancelAcquisition = useCallback(async (acquisitionId) => {
    try {
      setLoading(true);
      const data = await acquisitionService.cancelAcquisition(acquisitionId);
      setActiveAcquisition(null);
      toast({
        title: "Acquisition Cancelled",
        description: data.message,
        variant: "warning"
      });
      return true;
    } catch (err) {
      toast({
        title: "Cancel Failed",
        description: err.response?.data?.detail || err.message,
        variant: "destructive"
      });
      return false;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  // Auto-refresh nearby items when player moves
  useEffect(() => {
    if (autoRefresh && playerPosition) {
      const intervalId = setInterval(() => {
        fetchNearbyItems(playerPosition);
      }, 5000); // Refresh every 5 seconds

      return () => clearInterval(intervalId);
    }
  }, [autoRefresh, playerPosition, fetchNearbyItems]);

  // Auto-refresh active acquisition
  useEffect(() => {
    if (autoRefresh) {
      fetchActiveAcquisition();
      const intervalId = setInterval(() => {
        fetchActiveAcquisition();
      }, 3000); // Refresh every 3 seconds

      return () => clearInterval(intervalId);
    }
  }, [autoRefresh, fetchActiveAcquisition]);

  return {
    activeItems,
    nearbyItems,
    activeAcquisition,
    loading,
    error,
    fetchActiveItems,
    fetchNearbyItems,
    fetchActiveAcquisition,
    startAcquisition,
    claimAcquisition,
    cancelAcquisition
  };
};
