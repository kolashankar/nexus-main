import React from "react";
/**
 * Custom hook for game actions.
 */

import { useState, useCallback } from 'react';
import { actionService } from '../services/action/actionService';
import { toast } from 'sonner';

export const useActions = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [actionHistory, setActionHistory] = useState([]);

  /**
   * Perform hack action.
   */
  const performHack = useCallback(async (targetPlayerId, onSuccess) => {
    setLoading(true);
    setError(null);

    try {
      const result = await actionService.performHack(targetPlayerId);

      if (result.success) {
        toast.success('Hack successful!', {
          description: result.message || 'You successfully hacked the target',
        });
        onSuccess?.(result);
      } else {
        toast.error('Hack failed', {
          description: result.message || 'The hack attempt failed',
        });
      }

      return result;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to perform hack';
      setError(errorMsg);
      toast.error('Action failed', { description: errorMsg });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Perform help action.
   */
  const performHelp = useCallback(async (targetPlayerId, helpType, amount, onSuccess) => {
    setLoading(true);
    setError(null);

    try {
      const result = await actionService.performHelp(targetPlayerId, helpType, amount);

      if (result.success) {
        toast.success('Help provided!', {
          description: result.message || 'You successfully helped the player',
        });
        onSuccess?.(result);
      }

      return result;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to help player';
      setError(errorMsg);
      toast.error('Action failed', { description: errorMsg });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Perform steal action.
   */
  const performSteal = useCallback(async (targetPlayerId, stealType, targetItemId, onSuccess) => {
    setLoading(true);
    setError(null);

    try {
      const result = await actionService.performSteal(targetPlayerId, stealType, targetItemId);

      if (result.success) {
        toast.success('Steal successful!', {
          description: result.message || 'You successfully stole from the target',
        });
        onSuccess?.(result);
      } else {
        toast.warning('Steal failed', {
          description: result.message || 'The steal attempt failed',
        });
      }

      return result;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to steal';
      setError(errorMsg);
      toast.error('Action failed', { description: errorMsg });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Perform donate action.
   */
  const performDonate = useCallback(async (targetPlayerId, amount, message, onSuccess) => {
    setLoading(true);
    setError(null);

    try {
      const result = await actionService.performDonate(targetPlayerId, amount, message);

      if (result.success) {
        toast.success('Donation sent!', {
          description: result.message || `You donated ${amount} to the player`,
        });
        onSuccess?.(result);
      }

      return result;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to donate';
      setError(errorMsg);
      toast.error('Action failed', { description: errorMsg });
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Load action history.
   */
  const loadHistory = useCallback(async (limit = 50, offset = 0) => {
    setLoading(true);
    setError(null);

    try {
      const history = await actionService.getActionHistory(limit, offset);
      setActionHistory(history);
      return history;
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Failed to load action history';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  /**
   * Check action cooldown.
   */
  const checkCooldown = useCallback(async (actionType) => {
    try {
      return await actionService.checkCooldown(actionType);
    } catch (err) {
      console.error('Failed to check cooldown:', err);
      return { on_cooldown: false, can_perform: true, remaining_time: 0 };
    }
  }, []);

  return {
    loading,
    error,
    actionHistory,
    performHack,
    performHelp,
    performSteal,
    performDonate,
    loadHistory,
    checkCooldown,
  };
};
