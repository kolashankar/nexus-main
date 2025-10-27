import React from "react";
import { create } from 'zustand';

export const useActionsStore = create((set) => ({
  recentActions: [],
  loading: false,
  error: null,
  addAction: (action) =>
    set((state) => ({
      recentActions: [action, ...state.recentActions].slice(0, 50),
    })),
  setRecentActions: (actions) => set({ recentActions: actions }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));
