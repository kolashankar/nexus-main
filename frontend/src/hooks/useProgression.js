import React from "react";
import { useState, useEffect, useCallback } from 'react';
import { progressionService } from '@/services/progression/progressionService';

export const useProgression = () => {
  const [progression, setProgression] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchProgression = useCallback(async () => {
    try {
      setLoading(true);
      const data = await progressionService.getProgressionData();
      setProgression(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch progression');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchProgression();
  }, [fetchProgression]);

  const gainXP = useCallback(async (amount) => {
    try {
      const result = await progressionService.gainXP(amount);
      setProgression((prev) => (prev ? { ...prev, xp: result.xp, level: result.level } : null));
      return result;
    } catch (err) {
      throw err;
    }
  }, []);

  const unlockSkillNode = useCallback(
    async (trait, nodeId) => {
      try {
        await progressionService.unlockSkillNode(trait, nodeId);
        await fetchProgression();
      } catch (err) {
        throw err;
      }
    },
    [fetchProgression]
  );

  const activateSuperpower = useCallback(async (powerId) => {
    try {
      const result = await progressionService.activateSuperpower(powerId);
      return result;
    } catch (err) {
      throw err;
    }
  }, []);

  const unlockAchievement = useCallback(async (achievementId) => {
    try {
      const result = await progressionService.unlockAchievement(achievementId);
      setProgression((prev) =>
        prev ? { ...prev, achievementsUnlocked: result.achievementsUnlocked } : null
      );
      return result;
    } catch (err) {
      throw err;
    }
  }, []);

  const prestige = useCallback(async () => {
    try {
      const result = await progressionService.prestige();
      await fetchProgression();
      return result;
    } catch (err) {
      throw err;
    }
  }, [fetchProgression]);

  return {
    progression,
    loading,
    error,
    gainXP,
    unlockSkillNode,
    activateSuperpower,
    unlockAchievement,
    prestige,
    refetch: fetchProgression,
  };
};
