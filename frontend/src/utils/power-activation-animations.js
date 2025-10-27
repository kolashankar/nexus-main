import React from "react";
/**
 * Superpower activation animation effects
 */

import { haptic } from './mobile-helpers';
import { createEnergyBurst, createCombatParticles } from './combat-animations';

/**
 * Power tier colors
 */
const TIER_COLORS = {
  1: '#10b981', // Green - Basic
  2: '#3b82f6', // Blue - Intermediate
  3: '#8b5cf6', // Purple - Advanced
  4: '#f59e0b', // Orange - Master
  5: '#ef4444', // Red - Legendary
};

/**
 * Main power activation effect
 */
export const activatePower = async ({ powerName, element, tier = 1 }) => {
  const color = TIER_COLORS[tier];

  // Add glow effect
  element.classList.add('animate-power-activate', 'glow-pulse');

  // Create energy burst
  createEnergyBurst(element, color);

  // Create particles
  createCombatParticles(element, 15 + tier * 5, color);

  // Haptic feedback
  if (tier >= 4) {
    haptic.heavy();
  } else {
    haptic.medium();
  }

  // Power-specific effects
  await playPowerSpecificEffect(powerName, element, color);

  // Cleanup
  setTimeout(() => {
    element.classList.remove('animate-power-activate', 'glow-pulse');
  }, 800);
};

/**
 * Power-specific visual effects
 */
const playPowerSpecificEffect = async (powerName, element, color) => {
  const effects = {
    // Tier 1
    mind_reading: () => createMindReadingEffect(element),
    enhanced_reflexes: () => createReflexEffect(element),
    persuasion_aura: () => createAuraEffect(element, color),
    danger_sense: () => createDangerSenseEffect(element),
    quick_heal: () => createHealEffect(element),

    // Tier 2
    telekinesis: () => createTelekinesisEffect(element),
    invisibility: () => createInvisibilityEffect(element),
    energy_shield: () => createShieldEffect(element, color),
    psychic_vision: () => createVisionEffect(element),
    tech_control: () => createTechEffect(element),

    // Tier 3
    time_slow: () => createTimeSlowEffect(element),
    healing_touch: () => createHealingTouchEffect(element),
    probability_manipulation: () => createProbabilityEffect(element),
    empathic_link: () => createEmpathicEffect(element, color),
    shadow_walk: () => createShadowWalkEffect(element),

    // Tier 4
    charm_mastery: () => createCharmEffect(element, color),
    combat_supremacy: () => createCombatSupremacyEffect(element),
    memory_vault: () => createMemoryEffect(element),
    future_glimpse: () => createFutureGlimpseEffect(element),
    reality_bend: () => createRealityBendEffect(element),

    // Tier 5
    karmic_transfer: () => createKarmaTransferEffect(element),
    soul_bond: () => createSoulBondEffect(element, color),
    temporal_echo: () => createTemporalEchoEffect(element),
    omniscience: () => createOmniscienceEffect(element),
    ascension: () => createAscensionEffect(element),
  };

  const effectFn = effects[powerName.toLowerCase().replace(/\s+/g, '_')];
  if (effectFn) {
    effectFn();
  }
};

// Individual power effects
const createMindReadingEffect = (element) => {
  const thoughtBubbles = 5;
  for (let i = 0; i < thoughtBubbles; i++) {
    setTimeout(() => {
      const bubble = document.createElement('div');
      bubble.textContent = '?';
      bubble.className = 'floating-text';
      bubble.style.color = '#3b82f6';
      bubble.style.fontSize = '1.5rem';

      const rect = element.getBoundingClientRect();
      bubble.style.left = `${rect.left + Math.random() * rect.width}px`;
      bubble.style.top = `${rect.top}px`;

      document.body.appendChild(bubble);
      setTimeout(() => document.body.removeChild(bubble), 2000);
    }, i * 200);
  }
};

const createReflexEffect = (element) => {
  element.style.transition = 'all 0.1s';
  element.style.filter = 'brightness(1.5)';
  setTimeout(() => {
    element.style.filter = '';
  }, 500);
};

const createAuraEffect = (element, color) => {
  const aura = document.createElement('div');
  aura.style.position = 'absolute';
  aura.style.inset = '-10px';
  aura.style.borderRadius = '50%';
  aura.style.background = `radial-gradient(circle, ${color}88, transparent)`;
  aura.style.animation = 'pulse 2s ease-in-out infinite';
  aura.style.pointerEvents = 'none';

  element.style.position = 'relative';
  element.appendChild(aura);

  setTimeout(() => element.removeChild(aura), 3000);
};

const createDangerSenseEffect = (element) => {
  const pulseCount = 3;
  for (let i = 0; i < pulseCount; i++) {
    setTimeout(() => {
      element.style.boxShadow = '0 0 20px #ef4444';
      setTimeout(() => {
        element.style.boxShadow = '';
      }, 200);
    }, i * 400);
  }
};

const createHealEffect = (element) => {
  createCombatParticles(element, 20, '#10b981');
  element.classList.add('animate-glow');
  setTimeout(() => element.classList.remove('animate-glow'), 1000);
};

const createTelekinesisEffect = (element) => {
  element.style.transform = 'translateY(-20px)';
  element.style.transition = 'transform 0.5s ease-out';
  setTimeout(() => {
    element.style.transform = '';
  }, 500);
};

const createInvisibilityEffect = (element) => {
  element.style.opacity = '0.3';
  element.style.transition = 'opacity 0.5s';
  setTimeout(() => {
    element.style.opacity = '1';
  }, 2000);
};

const createShieldEffect = (element, color) => {
  const shield = document.createElement('div');
  shield.style.position = 'absolute';
  shield.style.inset = '-5px';
  shield.style.border = `3px solid ${color}`;
  shield.style.borderRadius = '50%';
  shield.style.animation = 'glow 1s ease-in-out';
  shield.style.pointerEvents = 'none';

  element.style.position = 'relative';
  element.appendChild(shield);

  setTimeout(() => element.removeChild(shield), 1000);
};

const createVisionEffect = (element) => {
  const eye = document.createElement('div');
  eye.textContent = '👁️';
  eye.style.fontSize = '3rem';
  eye.className = 'floating-text';

  const rect = element.getBoundingClientRect();
  eye.style.left = `${rect.left + rect.width / 2}px`;
  eye.style.top = `${rect.top}px`;

  document.body.appendChild(eye);
  setTimeout(() => document.body.removeChild(eye), 2000);
};

const createTechEffect = (element) => {
  // Binary rain effect
  for (let i = 0; i < 10; i++) {
    setTimeout(() => {
      const binary = document.createElement('div');
      binary.textContent = Math.random() > 0.5 ? '1' : '0';
      binary.className = 'floating-text';
      binary.style.color = '#10b981';
      binary.style.fontFamily = 'monospace';

      const rect = element.getBoundingClientRect();
      binary.style.left = `${rect.left + Math.random() * rect.width}px`;
      binary.style.top = `${rect.top}px`;

      document.body.appendChild(binary);
      setTimeout(() => document.body.removeChild(binary), 1000);
    }, i * 50);
  }
};

const createTimeSlowEffect = (element) => {
  // Slow down all animations temporarily
  document.documentElement.style.setProperty('--animation-speed', '0.3');
  setTimeout(() => {
    document.documentElement.style.setProperty('--animation-speed', '1');
  }, 2000);
};

const createHealingTouchEffect = (element) => {
  createCombatParticles(element, 30, '#10b981');
  createAuraEffect(element, '#10b981');
};

const createProbabilityEffect = (element) => {
  // Show dice or probability symbols
  const symbols = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
  symbols.forEach((symbol, i) => {
    setTimeout(() => {
      const die = document.createElement('div');
      die.textContent = symbol;
      die.className = 'floating-text';
      die.style.fontSize = '2rem';

      const rect = element.getBoundingClientRect();
      die.style.left = `${rect.left + rect.width / 2}px`;
      die.style.top = `${rect.top}px`;

      document.body.appendChild(die);
      setTimeout(() => document.body.removeChild(die), 1500);
    }, i * 150);
  });
};

const createEmpathicEffect = (element, color) => {
  // Heart particles
  for (let i = 0; i < 10; i++) {
    setTimeout(() => {
      const heart = document.createElement('div');
      heart.textContent = '❤️';
      heart.className = 'floating-text';

      const rect = element.getBoundingClientRect();
      heart.style.left = `${rect.left + Math.random() * rect.width}px`;
      heart.style.top = `${rect.top}px`;

      document.body.appendChild(heart);
      setTimeout(() => document.body.removeChild(heart), 2000);
    }, i * 200);
  }
};

const createShadowWalkEffect = (element) => {
  element.style.transition = 'all 0.3s';
  element.style.opacity = '0';
  element.style.transform = 'scale(0.5)';

  setTimeout(() => {
    element.style.opacity = '1';
    element.style.transform = 'scale(1)';
  }, 300);
};

const createCharmEffect = (element, color) => {
  createAuraEffect(element, color);
  createCombatParticles(element, 20, '#ec4899');
};

const createCombatSupremacyEffect = (element) => {
  element.classList.add('animate-shake');
  createCombatParticles(element, 40, '#ef4444');
  setTimeout(() => element.classList.remove('animate-shake'), 500);
};

const createMemoryEffect = (element) => {
  // Book or brain icon effect
  const brain = document.createElement('div');
  brain.textContent = '🧠';
  brain.style.fontSize = '3rem';
  brain.className = 'floating-text';

  const rect = element.getBoundingClientRect();
  brain.style.left = `${rect.left + rect.width / 2}px`;
  brain.style.top = `${rect.top}px`;

  document.body.appendChild(brain);
  setTimeout(() => document.body.removeChild(brain), 2000);
};

const createFutureGlimpseEffect = (element) => {
  // Clock or crystal ball effect
  const crystal = document.createElement('div');
  crystal.textContent = '🔮';
  crystal.style.fontSize = '3rem';
  crystal.className = 'floating-text';
  crystal.style.animation = 'spin 1s linear';

  const rect = element.getBoundingClientRect();
  crystal.style.left = `${rect.left + rect.width / 2}px`;
  crystal.style.top = `${rect.top}px`;

  document.body.appendChild(crystal);
  setTimeout(() => document.body.removeChild(crystal), 2000);
};

const createRealityBendEffect = (element) => {
  // Reality distortion effect
  element.style.filter = 'hue-rotate(180deg)';
  element.style.transform = 'rotateY(180deg)';
  element.style.transition = 'all 0.5s';

  setTimeout(() => {
    element.style.filter = '';
    element.style.transform = '';
  }, 1000);
};

const createKarmaTransferEffect = (element) => {
  // Karma symbol and energy flow
  createCombatParticles(element, 50, '#8b5cf6');
  createEnergyBurst(element, '#8b5cf6');
};

const createSoulBondEffect = (element, color) => {
  // Connection lines and hearts
  createAuraEffect(element, color);
  for (let i = 0; i < 10; i++) {
    setTimeout(() => {
      const heart = document.createElement('div');
      heart.textContent = '💕';
      heart.className = 'floating-text';

      const rect = element.getBoundingClientRect();
      heart.style.left = `${rect.left + Math.random() * rect.width}px`;
      heart.style.top = `${rect.top}px`;

      document.body.appendChild(heart);
      setTimeout(() => document.body.removeChild(heart), 2000);
    }, i * 150);
  }
};

const createTemporalEchoEffect = (element) => {
  // Create ghost copies
  for (let i = 0; i < 3; i++) {
    setTimeout(() => {
      const echo = element.cloneNode(true);
      echo.style.position = 'absolute';
      echo.style.opacity = '0.3';
      echo.style.pointerEvents = 'none';

      const rect = element.getBoundingClientRect();
      echo.style.left = `${rect.left}px`;
      echo.style.top = `${rect.top}px`;

      document.body.appendChild(echo);
      setTimeout(() => document.body.removeChild(echo), 1000);
    }, i * 300);
  }
};

const createOmniscienceEffect = (element) => {
  // All-seeing eye with intense glow
  const eye = document.createElement('div');
  eye.textContent = '👁️';
  eye.style.fontSize = '5rem';
  eye.className = 'floating-text';
  eye.style.textShadow = '0 0 30px #fff, 0 0 60px #3b82f6';

  const rect = element.getBoundingClientRect();
  eye.style.left = `${rect.left + rect.width / 2}px`;
  eye.style.top = `${rect.top}px`;

  document.body.appendChild(eye);
  createCombatParticles(element, 100, '#fff');
  setTimeout(() => document.body.removeChild(eye), 3000);
};

const createAscensionEffect = (element) => {
  // Ultimate power effect
  element.style.filter = 'brightness(2)';
  element.style.transform = 'scale(1.2)';
  element.style.transition = 'all 1s';

  createEnergyBurst(element, '#ffd700');
  createCombatParticles(element, 150, '#ffd700');

  // Screen flash
  const flash = document.createElement('div');
  flash.style.position = 'fixed';
  flash.style.inset = '0';
  flash.style.background = 'radial-gradient(circle, #ffd700, transparent)';
  flash.style.opacity = '0.8';
  flash.style.pointerEvents = 'none';
  flash.style.zIndex = '9999';
  flash.style.animation = 'fadeOut 2s forwards';

  document.body.appendChild(flash);

  setTimeout(() => {
    element.style.filter = '';
    element.style.transform = '';
    document.body.removeChild(flash);
  }, 2000);

  haptic.success();
};
