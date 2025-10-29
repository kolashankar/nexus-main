import React from "react";
/**
 * Player state slice
 */
import apiClient from '../../services/api/client';

export const playerSlice = (set, get) => ({
  player: null,
  isLoadingPlayer: false,
  playerError: null,

  fetchPlayer: async () => {
    set({ isLoadingPlayer: true, playerError: null });
    try {
      const response = await apiClient.get('/api/player/profile');
      set({
        player: response.data,
        isLoadingPlayer: false,
      });
    } catch (error) {
      set({
        playerError: error.message,
        isLoadingPlayer: false,
      });
    }
  },

  updatePlayer: async (data) => {
    const currentPlayer = get().player;
    if (!currentPlayer) return;
    
    try {
      // Update on backend
      const response = await apiClient.put('/api/player/profile', data);
      
      // Update local state with response data
      set({
        player: { ...currentPlayer, ...response.data },
      });
      
      return response.data;
    } catch (error) {
      console.error('Failed to update player:', error);
      throw error;
    }
  },

  clearPlayer: () => {
    set({
      player: null,
      playerError: null,
    });
  },
});
