import React from "react";
import { useState, useEffect, useCallback } from 'react';
import combatService from '../services/combat/combatService';
import { Battle } from '../types/combat';

export const useCombat = (battleId?: string, playerId?: string) => {
  const [battle, setBattle] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadBattle = useCallback(async () => {
    if (!battleId) return;
    
    try {
      setLoading(true);
      const data = await combatService.getBattleState(battleId);
      setBattle(data);
      setError(null);
    } catch (err) {
      setError(err.message || 'Failed to load battle');
    } finally {
      setLoading(false);
    }
  }, [battleId]);

  const executeAction = useCallback(async (
    actionType,
    targetId?: string,
    abilityName?: string
  ) => {
    if (!battleId || !playerId) return;

    try {
      const result = await combatService.executeAction(
        battleId,
        playerId,
        actionType,
        targetId,
        abilityName
      );
      await loadBattle();
      return result;
    } catch (err) {
      setError(err.message || 'Action failed');
      throw err;
    }
  }, [battleId, playerId, loadBattle]);

  const flee = useCallback(async () => {
    if (!battleId || !playerId) return;

    try {
      const result = await combatService.fleeBattle(battleId, playerId);
      await loadBattle();
      return result;
    } catch (err) {
      setError(err.message || 'Failed to flee');
      throw err;
    }
  }, [battleId, playerId, loadBattle]);

  useEffect(() => {
    loadBattle();
  }, [loadBattle]);

  return {
    battle,
    loading,
    error,
    executeAction,
    flee,
    reload: loadBattle
  };
};
