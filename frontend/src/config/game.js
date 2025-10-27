import React from "react";
/**
 * Game configuration
 */

export const GAME_CONFIG = {
  // Player defaults
  DEFAULT_LEVEL: 1,
  DEFAULT_XP: 0,
  DEFAULT_KARMA: 0,
  DEFAULT_CREDITS: 1000,

  // Trait defaults
  DEFAULT_TRAIT_VALUE: 50,
  MIN_TRAIT_VALUE: 0,
  MAX_TRAIT_VALUE: 100,

  // Combat
  BASE_HP: 100,
  BASE_ATTACK: 10,
  BASE_DEFENSE: 5,

  // Economy
  CURRENCIES: [
    'credits',
    'karma_tokens',
    'dark_matter',
    'prestige_points',
    'guild_coins',
    'legacy_shards',
  ],

  // Leveling
  XP_PER_LEVEL: 100,
  MAX_LEVEL: 100,

  // Karma thresholds
  GOOD_KARMA_THRESHOLD: 500,
  BAD_KARMA_THRESHOLD: -500,

  // Economic class thresholds
  RICH_THRESHOLD: 100000,
  MIDDLE_THRESHOLD: 10000,

  // 3D Settings
  ENABLE_3D: true,
  ENABLE_SHADOWS: true,
  ENABLE_PARTICLES: true,

  // WebSocket
  WS_RECONNECT_ATTEMPTS: 5,
  WS_RECONNECT_DELAY: 3000,
};

export default GAME_CONFIG;
