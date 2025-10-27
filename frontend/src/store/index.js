import React from "react";
/**
 * Main Zustand store configuration
 */
import { create } from 'zustand';
import { devtools, persist } from 'zustand/middleware';
import { authSlice } from './slices/authSlice';
import { playerSlice } from './slices/playerSlice';

export const useStore = create(
  devtools(
    persist(
      (...args) => ({
        ...authSlice(...args),
        ...playerSlice(...args),
      }),
      {
        name: 'karma-nexus-storage',
        partialize: (state) => ({
          // Persist auth tokens and authentication state
          accessToken: state.accessToken,
          refreshToken: state.refreshToken,
          isAuthenticated: state.isAuthenticated,
        }),
      }
    )
  )
);

export default useStore;
