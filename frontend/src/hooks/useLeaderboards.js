import React from "react";
import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

export const useLeaderboards = () => {
  const [leaderboards, setLeaderboards] = useState({});
  const [myRanks, setMyRanks] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchLeaderboard = async (type, limit = 50) => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/leaderboards/${type}`, {
        headers: { Authorization: `Bearer ${token}` },
        params: { limit },
      });

      setLeaderboards((prev) => ({
        ...prev,
        [type]: response.data,
      }));
    } catch (err) {
      console.error(`Error fetching ${type} leaderboard`, err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchMyRank = async (type) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/leaderboards/my-rank/${type}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setMyRanks((prev) => ({
        ...prev,
        [type]: response.data,
      }));
    } catch (err) {
      console.error(`Error fetching my rank for ${type}:`, err);
      // Don't set error - it's not critical
    }
  };

  return {
    leaderboards,
    myRanks,
    loading,
    error,
    fetchLeaderboard,
    fetchMyRank,
  };
};
