import React from "react";
import { apiClient } from '../api/client';

export const actionsService = {
  async hack(targetId) {
    const response = await apiClient.post('/api/actions/hack', { target_id: targetId });
    return response.data;
  },

  async help(targetId) {
    const response = await apiClient.post('/api/actions/help', { target_id: targetId });
    return response.data;
  },

  async steal(targetId) {
    const response = await apiClient.post('/api/actions/steal', { target_id: targetId });
    return response.data;
  },

  async donate(targetId, amount) {
    const response = await apiClient.post('/api/actions/donate', {
      target_id: targetId,
      amount,
    });
    return response.data;
  },

  async trade(targetId, offer, request) {
    const response = await apiClient.post('/api/actions/trade', {
      target_id: targetId,
      offer,
      request,
    });
    return response.data;
  },

  async getHistory() {
    const response = await apiClient.get('/api/actions/history');
    return response.data;
  },

  async getRecent() {
    const response = await apiClient.get('/api/actions/recent');
    return response.data;
  },
};
