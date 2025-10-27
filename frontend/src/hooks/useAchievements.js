import React from "react";
import { useState, useEffect } from 'react';
import achievementsService from '../services/achievements/achievementsService';

export const useAchievements = () => {
  const [achievements, setAchievements] = useState(null);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchAchievements = async () => {
    try {
      setLoading(true);
      const data = await achievementsService.getAchievements();
      setAchievements(data);
      setError(null);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSummary = async () => {
    try {
      const data = await achievementsService.getAchievementSummary();
      setSummary(data);
    } catch (err) {
      console.error('Failed to fetch summary', err);
    }
  };

  useEffect(() => {
    fetchAchievements();
    fetchSummary();
  }, []);

  return {
    achievements,
    summary,
    loading,
    error,
    refetch: fetchAchievements,
  };
};
