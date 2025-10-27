import React from "react";
import { create } from 'zustand';

export const useGameStore = create((set) => ({
  // 3D scene state
  scene: {
    playerPosition: { x: 0, y: 0, z: 0 },
    cameraPosition: { x: 0, y: 5, z: 10 },
    nearbyPlayers: [],
  },

  // Online players
  onlinePlayers: [],

  // Current room/territory
  currentRoom: null,

  // WebSocket connection status
  wsConnected: false,

  // Actions
  updatePlayerPosition: (position) => {
    set((state) => ({
      scene: {
        ...state.scene,
        playerPosition: position,
      },
    }));
  },

  updateNearbyPlayers: (players) => {
    set((state) => ({
      scene: {
        ...state.scene,
        nearbyPlayers: players,
      },
    }));
  },

  setOnlinePlayers: (players) => {
    set({ onlinePlayers: players });
  },

  addOnlinePlayer: (player) => {
    set((state) => ({
      onlinePlayers: [...state.onlinePlayers, player],
    }));
  },

  removeOnlinePlayer: (playerId) => {
    set((state) => ({
      onlinePlayers: state.onlinePlayers.filter((p) => p.player_id !== playerId),
    }));
  },

  setCurrentRoom: (roomId) => {
    set({ currentRoom: roomId });
  },

  setWSConnected: (connected) => {
    set({ wsConnected: connected });
  },
}));
