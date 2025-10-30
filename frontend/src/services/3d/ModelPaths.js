import React from "react";
/**
 * Centralized 3D model paths configuration
 */

export const MODEL_PATHS = {
  // Character Models
  characters: {
    male: {
      base: '/models/characters/male_base.glb',
      athletic: '/models/characters/male_athletic.glb',
      heavy: '/models/characters/male_heavy.glb',
    },
    female: {
      base: '/models/characters/female_base.glb',
      athletic: '/models/characters/female_athletic.glb',
      heavy: '/models/characters/female_heavy.glb',
    },
  },

  // Character Animations (FBX format)
  animations: {
    idle: '/models/animations/Stand_Idle.fbx',
    walk: '/models/animations/Walk.fbx',
    run: '/models/animations/Running.fbx',
    jump: '/models/animations/Jump.fbx',
    attack: '/models/animations/Attack.fbx',
    defend: '/models/animations/Defend.fbx',
    victory: '/models/animations/Victory.fbx',
    defeat: '/models/animations/Defeat.fbx',
    emotes: {
      wave: '/models/animations/emotes/Wave.fbx',
      dance: '/models/animations/emotes/Dance.fbx',
      laugh: '/models/animations/emotes/Laugh.fbx',
    },
  },

  // Robot Models
  robots: {
    combat: '/models/robots/combat.glb',
    scout: '/models/robots/scout.glb',
    guardian: '/models/robots/guardian.glb',
    assault: '/models/robots/assault.glb',
    tactical: '/models/robots/tactical.glb',
    hacker: '/models/robots/hacker.glb',
    medic: '/models/robots/medic.glb',
    harvester: '/models/robots/harvester.glb',
    trader: '/models/robots/trader.glb',
  },

  // Environment
  environment: {
    buildings: {
      warehouse: '/models/environment/warehouse.glb',
      shop: '/models/environment/shop.glb',
      headquarters: '/models/environment/headquarters.glb',
      tower: '/models/environment/tower.glb',
    },
    props: {
      container: '/models/environment/props/container.glb',
      vehicle: '/models/environment/props/vehicle.glb',
    },
    terrain: {
      platform: '/models/environment/terrain/platform.glb',
    },
  },

  // UI Elements
  ui: {
    hologram: '/models/ui/hologram.glb',
    interface: '/models/ui/interface.glb',
  },

  // Placeholder Models (simple geometries)
  placeholders: {
    character: '/models/placeholders/character_placeholder.glb',
    robot: '/models/placeholders/robot_placeholder.glb',
    building: '/models/placeholders/building_placeholder.glb',
  },
};

// Texture Paths
export const TEXTURE_PATHS = {
  characters: {
    skin: '/textures/characters/skin/',
    hair: '/textures/characters/hair/',
    clothing: '/textures/characters/clothing/',
  },
  robots: {
    metal: '/textures/robots/metal/',
    lights: '/textures/robots/lights/',
  },
  environment: {
    walls: '/textures/environment/walls/',
    floor: '/textures/environment/floor/',
    props: '/textures/environment/props/',
  },
  effects: {
    particles: '/textures/effects/particles/',
    glow: '/textures/effects/glow/',
  },
};

// Asset Collections for batch loading
export const ASSET_COLLECTIONS = {
  // Essential assets to load on startup
  essential: [
    MODEL_PATHS.placeholders.character,
    MODEL_PATHS.placeholders.robot,
    MODEL_PATHS.animations.idle,
    MODEL_PATHS.animations.walk,
  ],

  // Character creation assets
  characterCreation: [
    MODEL_PATHS.characters.male.base,
    MODEL_PATHS.characters.female.base,
    MODEL_PATHS.animations.idle,
    MODEL_PATHS.animations.walk,
    MODEL_PATHS.animations.emotes.wave,
  ],

  // Combat assets
  combat: [
    MODEL_PATHS.animations.attack,
    MODEL_PATHS.animations.defend,
    MODEL_PATHS.animations.victory,
    MODEL_PATHS.animations.defeat,
  ],

  // Robot marketplace assets
  robotMarketplace: [
    MODEL_PATHS.robots.combat,
    MODEL_PATHS.robots.scout,
    MODEL_PATHS.robots.guardian,
  ],

  // Environment assets
  worldEnvironment: [
    MODEL_PATHS.environment.terrain.platform,
    MODEL_PATHS.environment.buildings.tower,
  ],
};

/**
 * Get model path by category and type
 */
export function getModelPath(category, type) {
  const paths = MODEL_PATHS;
  return paths[category]?.[type];
}

/**
 * Get all paths in a category
 */
export function getCategoryPaths(category) {
  const paths = MODEL_PATHS;
  const categoryData = paths[category];

  if (!categoryData) return [];

  const result = [];

  function extractPaths(obj) {
    for (const key in obj) {
      if (typeof obj[key] === 'string') {
        result.push(obj[key]);
      } else if (typeof obj[key] === 'object') {
        extractPaths(obj[key]);
      }
    }
  }

  extractPaths(categoryData);
  return result;
}
