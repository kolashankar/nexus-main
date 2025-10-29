"""Trait calculation utilities."""

/**
 * Calculate trait level based on value
 */
export const calculateTraitLevel = (value) => {
  if (value >= 100) return { level: 5, name: 'Master', color: 'amber' };
  if (value >= 75) return { level: 4, name: 'Expert', color: 'purple' };
  if (value >= 50) return { level: 3, name: 'Proficient', color: 'blue' };
  if (value >= 25) return { level: 2, name: 'Apprentice', color: 'green' };
  return { level: 1, name: 'Novice', color: 'gray' };
};

/**
 * Calculate progress to next milestone
 */
export const calculateProgressToNextMilestone = (value) => {
  const milestones = [25, 50, 75, 100];
  const currentMilestone = milestones.find(m => value < m);
  
  if (!currentMilestone) {
    return { current: 100, next: 100, progress: 100 };
  }
  
  const previousMilestone = milestones[milestones.indexOf(currentMilestone) - 1] || 0;
  const progress = ((value - previousMilestone) / (currentMilestone - previousMilestone)) * 100;
  
  return {
    current: value,
    next: currentMilestone,
    previous: previousMilestone,
    progress: Math.max(0, Math.min(100, progress)),
    remaining: currentMilestone - value
  };
};

/**
 * Categorize traits as virtues or vices
 */
export const categorizeTraits = (traits) => {
  const virtues = ['kindness', 'compassion', 'honesty', 'courage', 'wisdom', 'patience', 'loyalty', 'humility', 'generosity', 'trust'];
  const vices = ['greed', 'wrath', 'envy', 'sloth', 'pride', 'gluttony', 'lust', 'vanity', 'cruelty', 'deceit'];
  
  const categorized = {
    virtues: {},
    vices: {},
    neutral: {}
  };
  
  Object.entries(traits).forEach(([trait, value]) => {
    const traitLower = trait.toLowerCase();
    if (virtues.includes(traitLower)) {
      categorized.virtues[trait] = value;
    } else if (vices.includes(traitLower)) {
      categorized.vices[trait] = value;
    } else {
      categorized.neutral[trait] = value;
    }
  });
  
  return categorized;
};

/**
 * Calculate trait balance (virtue vs vice)
 */
export const calculateTraitBalance = (traits) => {
  const categorized = categorizeTraits(traits);
  
  const virtueAvg = Object.values(categorized.virtues).length > 0
    ? Object.values(categorized.virtues).reduce((a, b) => a + b, 0) / Object.values(categorized.virtues).length
    : 50;
    
  const viceAvg = Object.values(categorized.vices).length > 0
    ? Object.values(categorized.vices).reduce((a, b) => a + b, 0) / Object.values(categorized.vices).length
    : 50;
  
  const balance = virtueAvg - viceAvg;
  
  return {
    virtue_score: Math.round(virtueAvg),
    vice_score: Math.round(viceAvg),
    balance: Math.round(balance),
    alignment: balance > 20 ? 'Virtuous' : balance < -20 ? 'Vice-inclined' : 'Balanced'
  };
};

/**
 * Get top traits
 */
export const getTopTraits = (traits, count = 5) => {
  return Object.entries(traits)
    .sort(([, a], [, b]) => b - a)
    .slice(0, count)
    .map(([trait, value]) => ({
      trait,
      value,
      level: calculateTraitLevel(value)
    }));
};

/**
 * Calculate trait evolution rate
 */
export const calculateEvolutionRate = (previousTraits, currentTraits, timespan = 'week') => {
  const changes = {};
  Object.keys(currentTraits).forEach(trait => {
    const prev = previousTraits[trait] || 0;
    const curr = currentTraits[trait] || 0;
    changes[trait] = curr - prev;
  });
  
  return {
    changes,
    fastest_growing: Object.entries(changes).sort(([, a], [, b]) => b - a)[0],
    fastest_declining: Object.entries(changes).sort(([, a], [, b]) => a - b)[0],
    total_change: Object.values(changes).reduce((a, b) => a + Math.abs(b), 0),
    timespan
  };
};

/**
 * Predict trait milestone
 */
export const predictNextMilestone = (trait, currentValue, recentChanges = []) => {
  const nextMilestone = [25, 50, 75, 100].find(m => currentValue < m);
  
  if (!nextMilestone) {
    return { reached: true, message: 'Maximum level reached!' };
  }
  
  const remaining = nextMilestone - currentValue;
  
  // Calculate average change rate
  const avgChange = recentChanges.length > 0
    ? recentChanges.reduce((a, b) => a + b, 0) / recentChanges.length
    : 0;
  
  if (avgChange <= 0) {
    return {
      milestone: nextMilestone,
      remaining,
      estimated_tasks: null,
      message: 'No recent progress detected'
    };
  }
  
  const estimatedTasks = Math.ceil(remaining / avgChange);
  
  return {
    milestone: nextMilestone,
    remaining,
    avg_change: Math.round(avgChange * 10) / 10,
    estimated_tasks: estimatedTasks,
    message: `Approximately ${estimatedTasks} similar tasks to reach next milestone`
  };
};

/**
 * Format trait name for display
 */
export const formatTraitName = (trait) => {
  return trait
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
};

/**
 * Get trait description
 */
export const getTraitDescription = (trait) => {
  const descriptions = {
    courage: 'Your bravery in the face of danger',
    wisdom: 'Your knowledge and insight',
    compassion: 'Your empathy and kindness towards others',
    strength: 'Your physical and mental fortitude',
    intelligence: 'Your analytical and problem-solving abilities',
    charisma: 'Your ability to influence and lead others',
    luck: 'Your fortune in random events',
    greed: 'Your desire for wealth and possessions',
    wrath: 'Your tendency towards anger and aggression',
    envy: 'Your jealousy of others success',
    sloth: 'Your laziness and lack of motivation',
    pride: 'Your sense of superiority',
    trust: 'Your faith in others',
    cunning: 'Your craftiness and strategic thinking',
    resilience: 'Your ability to recover from setbacks'
  };
  
  return descriptions[trait] || `Your ${formatTraitName(trait)} trait`;
};
