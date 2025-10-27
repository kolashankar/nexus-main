import React from "react";
import { create } from 'zustand';

export const useKarmaStore = create((set) => ({
  karmaScore: 0,
  karmaHistory: [],
  worldKarma: { good: 0, evil: 0, neutral: 0 },
  loading: false,
  setKarmaScore: (score) => set({ karmaScore: score }),
  setKarmaHistory: (history) => set({ karmaHistory: history }),
  setWorldKarma: (worldKarma) => set({ worldKarma }),
  setLoading: (loading) => set({ loading }),
}));
