/**
 * Helper functions for trait management
 */

/**
 * Convert traits object to array format for UI components
 * @param {Object} traitsObj - Traits object with trait names as keys and values as levels
 * @returns {Array} Array of trait objects with name, level, type, and category
 */
export const convertTraitsToArray = (traitsObj) => {
  if (!traitsObj || typeof traitsObj !== 'object') {
    return [];
  }

  // Define trait categories
  const virtues = [
    'empathy', 'integrity', 'discipline', 'creativity', 'resilience',
    'curiosity', 'kindness', 'courage', 'patience', 'adaptability',
    'wisdom', 'humility', 'vision', 'honesty', 'loyalty',
    'generosity', 'self_awareness', 'gratitude', 'optimism', 'loveability'
  ];

  const vices = [
    'greed', 'arrogance', 'deceit', 'cruelty', 'selfishness',
    'envy', 'wrath', 'cowardice', 'laziness', 'gluttony',
    'paranoia', 'impulsiveness', 'vengefulness', 'manipulation', 'prejudice',
    'betrayal', 'stubbornness', 'pessimism', 'recklessness', 'vanity'
  ];

  const skills = [
    'hacking', 'negotiation', 'stealth', 'leadership', 'technical_knowledge',
    'physical_strength', 'speed', 'intelligence', 'charisma', 'perception',
    'endurance', 'dexterity', 'memory', 'focus', 'networking',
    'strategy', 'trading', 'engineering', 'medicine', 'meditation'
  ];

  const traitsArray = [];

  // Convert object to array
  Object.entries(traitsObj).forEach(([key, value]) => {
    // Determine type and category
    let type = 'skill';
    let category = 'skill';

    if (virtues.includes(key)) {
      type = 'virtue';
      category = 'good';
    } else if (vices.includes(key)) {
      type = 'vice';
      category = 'bad';
    }

    // Only include traits that have meaningful values (not default 50.0 or very low)
    if (value > 55 || value < 45) {
      traitsArray.push({
        name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        originalName: key,
        level: Math.round(value),
        value: value,
        type: type,
        category: category
      });
    }
  });

  return traitsArray;
};

/**
 * Convert meta traits object to array format
 * @param {Object} metaTraitsObj - Meta traits object
 * @returns {Array} Array of meta trait objects
 */
export const convertMetaTraitsToArray = (metaTraitsObj) => {
  if (!metaTraitsObj || typeof metaTraitsObj !== 'object') {
    return [];
  }

  const metaTraitsArray = [];

  Object.entries(metaTraitsObj).forEach(([key, value]) => {
    // Only include meta traits with meaningful values
    if (value > 55 || value < 45) {
      metaTraitsArray.push({
        name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        originalName: key,
        level: Math.round(value),
        value: value,
        type: 'meta',
        category: 'meta'
      });
    }
  });

  return metaTraitsArray;
};

/**
 * Get all traits as array (both regular and meta)
 * @param {Object} traitsObj - Regular traits object
 * @param {Object} metaTraitsObj - Meta traits object
 * @returns {Array} Combined array of all traits
 */
export const getAllTraitsArray = (traitsObj, metaTraitsObj) => {
  const regularTraits = convertTraitsToArray(traitsObj);
  const metaTraits = convertMetaTraitsToArray(metaTraitsObj);
  return [...regularTraits, ...metaTraits];
};

/**
 * Check if player is new (has default traits)
 * @param {Object} traitsObj - Traits object
 * @returns {Boolean} True if player has mostly default traits (50.0)
 */
export const isNewPlayer = (traitsObj) => {
  if (!traitsObj || typeof traitsObj !== 'object') {
    return true;
  }

  const values = Object.values(traitsObj);
  const defaultCount = values.filter(v => v === 50.0).length;
  
  // If more than 80% of traits are at default value, consider new player
  return defaultCount > (values.length * 0.8);
};
