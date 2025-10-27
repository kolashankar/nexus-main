import React from "react";
/**
 * Karma service for karma system API.
 */

import { apiClient } from '../api/client';

/**
 * Get current karma score.
 */
export const getKarmaScore = async () => {
  const response = await apiClient.get('/api/karma/score');
  return response.data;
};

/**
 * Get karma history.
 */
export const getKarmaHistory = async (limit = 50) => {
  const response = await apiClient.get('/api/karma/history', {
    params: { limit },
  });
  return response.data;
};

/**
 * Get karma events (triggered events).
 */
export const getKarmaEvents = async () => {
  const response = await apiClient.get('/api/karma/events');
  return response.data;
};

/**
 * Respond to a karma event.
 */
export const respondToKarmaEvent = async (eventId, response) => {
  const res = await apiClient.post(`/api/karma/events/${eventId}/respond`, {
    response,
  });
  return res.data;
};

/**
 * Get world karma state.
 */
export const getWorldKarmaState = async () => {
  const response = await apiClient.get('/api/karma/world-state');
  return response.data;
};

/**
 * Get collective karma.
 */
export const getCollectiveKarma = async () => {
  const response = await apiClient.get('/api/karma/collective');
  return response.data;
};

export const karmaService = {
  getKarmaScore,
  getKarmaHistory,
  getKarmaEvents,
  respondToKarmaEvent,
  getWorldKarmaState,
  getCollectiveKarma,
};
