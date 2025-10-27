import React from "react";
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

export const useWorldEvents = () => {
  const [worldState, setWorldState] = useState(null);
  const [activeEvents, setActiveEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchWorldState = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/world/state`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setWorldState(response.data);
    } catch (err) {
      console.error('Error fetching world state', err);
      setError(err.message);
    }
  };

  const fetchActiveEvents = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/world/events`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setActiveEvents(response.data);
    } catch (err) {
      console.error('Error fetching active events', err);
      setError(err.message);
    }
  };

  const refreshWorldState = async () => {
    setLoading(true);
    await fetchWorldState();
    setLoading(false);
  };

  const refreshActiveEvents = async () => {
    await fetchActiveEvents();
  };

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      await Promise.all([fetchWorldState(), fetchActiveEvents()]);
      setLoading(false);
    };

    loadData();

    // Refresh every 30 seconds
    const interval = setInterval(() => {
      fetchWorldState();
      fetchActiveEvents();
    }, 30000);

    return () => clearInterval(interval);
     
  }, []);

  return {
    worldState,
    activeEvents,
    loading,
    error,
    refreshWorldState,
    refreshActiveEvents,
  };
};
