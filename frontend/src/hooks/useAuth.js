import React from "react";
/**
 * Custom hook for authentication
 */
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import useStore from '../store';
import websocketService from '../services/websocket/websocketService';

export const useAuth = () => {
  const navigate = useNavigate();
  const { isAuthenticated, accessToken, login, register, logout, isLoading, error } = useStore();

  useEffect(() => {
    // Connect WebSocket when authenticated
    if (isAuthenticated && accessToken) {
      websocketService.connect(accessToken);
    }

    // Disconnect WebSocket when logging out
    return () => {
      if (!isAuthenticated) {
        websocketService.disconnect();
      }
    };
  }, [isAuthenticated, accessToken]);

  const handleLogin = async (username, password) => {
    try {
      await login({ username: 'testuser', password });
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed', err);
      throw err;
    }
  };

  const handleRegister = async (username, email, password) => {
    try {
      await register({ username: 'testuser', email, password });
      navigate('/dashboard');
    } catch (err) {
      console.error('Registration failed', err);
      throw err;
    }
  };

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (err) {
      console.error('Logout failed', err);
    }
  };

  return {
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
  };
};

export default useAuth;
