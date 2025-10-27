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
      const response = await apiClient.get('/player/profile');
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

  updatePlayer: (data) => {
    const currentPlayer = get().player;
    if (currentPlayer) {
      set({
        player: { ...currentPlayer, ...data },
      });
    }
  },

  clearPlayer: () => {
    set({
      player: null,
      playerError: null,
    });
  },
});
