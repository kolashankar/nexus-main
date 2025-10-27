import React from "react";
/**
 * Action service for game actions API.
 */

import { apiClient } from '../api/client';

/**
 * Perform a hack action on another player.
 */
export const performHack = async (targetPlayerId, actionData) => {
  const response = await apiClient.post('/api/actions/hack', {
    target_player_id: targetPlayerId,
    ...actionData,
  });
  return response.data;
};

/**
 * Perform a help action on another player.
 */
export const performHelp = async (targetPlayerId, helpType, amount) => {
  const response = await apiClient.post('/api/actions/help', {
    target_player_id: targetPlayerId,
    help_type: helpType,
    amount,
  });
  return response.data;
};

/**
 * Perform a steal action on another player.
 */
export const performSteal = async (targetPlayerId, stealType, targetItemId) => {
  const response = await apiClient.post('/api/actions/steal', {
    target_player_id: targetPlayerId,
    steal_type: stealType,
    target_item_id: targetItemId,
  });
  return response.data;
};

/**
 * Perform a donate action to another player.
 */
export const performDonate = async (targetPlayerId, amount, message) => {
  const response = await apiClient.post('/api/actions/donate', {
    target_player_id: targetPlayerId,
    amount,
    message,
  });
  return response.data;
};

/**
 * Perform a trade action with another player.
 */
export const performTrade = async (
  targetPlayerId,
  offerItems,
  requestItems,
  offerCredits,
  requestCredits
) => {
  const response = await apiClient.post('/api/actions/trade', {
    target_player_id: targetPlayerId,
    offer_items: offerItems,
    request_items: requestItems,
    offer_credits: offerCredits,
    request_credits: requestCredits,
  });
  return response.data;
};

/**
 * Get action history for current player.
 */
export const getActionHistory = async (limit = 50, offset = 0) => {
  const response = await apiClient.get('/api/actions/history', {
    params: { limit, offset },
  });
  return response.data;
};

/**
 * Get recent actions (last 24 hours).
 */
export const getRecentActions = async () => {
  const response = await apiClient.get('/api/actions/recent');
  return response.data;
};

/**
 * Get available actions for a target player.
 */
export const getAvailableActions = async (targetPlayerId) => {
  const response = await apiClient.get(`/api/actions/available/${targetPlayerId}`);
  return response.data;
};

/**
 * Check cooldown status for an action.
 */
export const checkCooldown = async (actionType) => {
  const response = await apiClient.get(`/api/actions/cooldown/${actionType}`);
  return response.data;
};

/**
 * Cancel a pending trade.
 */
export const cancelTrade = async (tradeId) => {
  const response = await apiClient.delete(`/api/actions/trade/${tradeId}`);
  return response.data.success;
};

/**
 * Accept a pending trade.
 */
export const acceptTrade = async (tradeId) => {
  const response = await apiClient.post(`/api/actions/trade/${tradeId}/accept`);
  return response.data;
};

/**
 * Decline a pending trade.
 */
export const declineTrade = async (tradeId) => {
  const response = await apiClient.post(`/api/actions/trade/${tradeId}/decline`);
  return response.data.success;
};

export const actionService = {
  performHack,
  performHelp,
  performSteal,
  performDonate,
  performTrade,
  getActionHistory,
  getRecentActions,
  getAvailableActions,
  checkCooldown,
  cancelTrade,
  acceptTrade,
  declineTrade,
};
