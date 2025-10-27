import React from "react";
import { useState } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

export const useTournaments = () => {
  const [tournaments, setTournaments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchActiveTournaments = async () => {
    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/tournaments/active`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setTournaments(response.data);
    } catch (err) {
      console.error('Error fetching tournaments', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchTournament = async (id) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/tournaments/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (err) {
      console.error('Error fetching tournament', err);
      return null;
    }
  };

  const registerForTournament = async (id) => {
    const token = localStorage.getItem('token');
    const response = await axios.post(
      `${API_URL}/api/tournaments/register`,
      { tournament_id: id },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  };

  const getMyTournaments = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/tournaments/my/tournaments`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      return response.data;
    } catch (err) {
      console.error('Error fetching my tournaments', err);
      return [];
    }
  };

  return {
    tournaments,
    loading,
    error,
    fetchActiveTournaments,
    fetchTournament,
    registerForTournament,
    getMyTournaments,
  };
};
