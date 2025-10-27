import React from "react";
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

export const useBattlePass = () => {
  const [battlePass, setBattlePass] = useState(null);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchBattlePass = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/seasonal/battle-pass/active`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setBattlePass(response.data);
    } catch (err) {
      console.error('Error fetching battle pass', err);
      setError(err.response?.data?.detail || err.message);
    }
  };

  const fetchProgress = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/seasonal/battle-pass/progress`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProgress(response.data);
    } catch (err) {
      console.error('Error fetching battle pass progress', err);
      setError(err.response?.data?.detail || err.message);
    }
  };

  const refreshProgress = async () => {
    setLoading(true);
    await Promise.all([fetchBattlePass(), fetchProgress()]);
    setLoading(false);
  };

  const claimRewards = async (tier) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/seasonal/battle-pass/claim-rewards`,
      { tier },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  };

  const purchasePremium = async () => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/seasonal/battle-pass/purchase-premium`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  };

  useEffect(() => {
    refreshProgress();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return {
    battlePass,
    progress,
    loading,
    error,
    claimRewards,
    purchasePremium,
    refreshProgress,
  };
};
