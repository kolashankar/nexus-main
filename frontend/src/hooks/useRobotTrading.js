import { useState, useEffect, useCallback } from 'react';

/**
 * Custom hook for robot trading operations
 * Handles purchasing, selling, upgrading, and managing robots
 */
const useRobotTrading = () => {
  const [robots, setRobots] = useState([]);
  const [myRobots, setMyRobots] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const getAuthHeaders = () => ({
    'Authorization': `Bearer ${localStorage.getItem('token')}`,
    'Content-Type': 'application/json'
  });

  // Fetch all available robot types
  const fetchRobotTypes = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/robots/types', {
        headers: getAuthHeaders()
      });
      const data = await response.json();
      
      if (response.ok) {
        setRobots(data);
        return { success: true, data };
      } else {
        throw new Error(data.error || 'Failed to fetch robot types');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  // Fetch player's robots
  const fetchMyRobots = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/robots/my-robots', {
        headers: getAuthHeaders()
      });
      const data = await response.json();
      
      if (response.ok) {
        setMyRobots(data.robots || data);
        return { success: true, data: data.robots || data };
      } else {
        throw new Error(data.error || 'Failed to fetch your robots');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  // Purchase a robot
  const purchaseRobot = useCallback(async (robotType, customName = null) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/robots/purchase', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ 
          robot_type: robotType,
          custom_name: customName
        })
      });
      const data = await response.json();
      
      if (response.ok && data.success) {
        // Refresh my robots list
        await fetchMyRobots();
        return { 
          success: true, 
          message: `Successfully purchased ${robotType}!`,
          data 
        };
      } else {
        throw new Error(data.error || 'Purchase failed');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [fetchMyRobots]);

  // Sell a robot
  const sellRobot = useCallback(async (robotId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/robots/sell', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ robot_id: robotId })
      });
      const data = await response.json();
      
      if (response.ok && data.success) {
        // Refresh my robots list
        await fetchMyRobots();
        return { 
          success: true, 
          message: 'Robot sold successfully!',
          data 
        };
      } else {
        throw new Error(data.error || 'Sale failed');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [fetchMyRobots]);

  // Upgrade a robot
  const upgradeRobot = useCallback(async (robotId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/robots/upgrade', {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ robot_id: robotId })
      });
      const data = await response.json();
      
      if (response.ok && data.success) {
        // Refresh my robots list
        await fetchMyRobots();
        return { 
          success: true, 
          message: 'Robot upgraded successfully!',
          data 
        };
      } else {
        throw new Error(data.error || 'Upgrade failed');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [fetchMyRobots]);

  // Delete/scrap a robot
  const deleteRobot = useCallback(async (robotId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`/api/robots/${robotId}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      });
      const data = await response.json();
      
      if (response.ok && data.success) {
        // Refresh my robots list
        await fetchMyRobots();
        return { 
          success: true, 
          message: 'Robot scrapped successfully!',
          data 
        };
      } else {
        throw new Error(data.error || 'Delete failed');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [fetchMyRobots]);

  // Rename a robot
  const renameRobot = useCallback(async (robotId, newName) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`/api/robots/${robotId}/name`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: JSON.stringify({ new_name: newName })
      });
      const data = await response.json();
      
      if (response.ok && data.success) {
        // Refresh my robots list
        await fetchMyRobots();
        return { 
          success: true, 
          message: 'Robot renamed successfully!',
          data 
        };
      } else {
        throw new Error(data.error || 'Rename failed');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, [fetchMyRobots]);

  // Get robot details
  const getRobotDetails = useCallback(async (robotId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`/api/robots/${robotId}`, {
        headers: getAuthHeaders()
      });
      const data = await response.json();
      
      if (response.ok) {
        return { success: true, data };
      } else {
        throw new Error(data.error || 'Failed to fetch robot details');
      }
    } catch (err) {
      setError(err.message);
      return { success: false, error: err.message };
    } finally {
      setLoading(false);
    }
  }, []);

  return {
    // State
    robots,
    myRobots,
    loading,
    error,
    
    // Actions
    fetchRobotTypes,
    fetchMyRobots,
    purchaseRobot,
    sellRobot,
    upgradeRobot,
    deleteRobot,
    renameRobot,
    getRobotDetails
  };
};

export default useRobotTrading;