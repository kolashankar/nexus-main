import React from "react";
/**
 * Combat animation utilities for Karma Nexus
 */

import { haptic } from './mobile-helpers';

/**
 * Execute combat animation
 */
export const playCombatAnimation = ({ type, element, duration = 500 }) => {
  return new Promise((resolve) => {
    const animations = {
      attack: 'animate-attack',
      defend: 'animate-defend',
      power: 'animate-power',
      damage: 'animate-damage',
      heal: 'animate-heal',
      miss: 'animate-miss',
    };

    const animationClass = animations[type] || 'animate-fade-in';
    element.classList.add(animationClass);

    // Add haptic feedback for actions
    if (type === 'attack') {
      haptic.medium();
    } else if (type === 'damage') {
      haptic.heavy();
    } else if (type === 'power') {
      haptic.success();
    }

    setTimeout(() => {
      element.classList.remove(animationClass);
      resolve();
    }, duration);
  });
};

/**
 * Create damage number popup
 */
export const showDamageNumber = (targetElement, damage, type = 'damage') => {
  const damageEl = document.createElement('div');
  damageEl.className = `floating-text ${type}`;
  damageEl.textContent = type === 'heal' ? `+${damage}` : `-${damage}`;

  const colors = {
    damage: '#ef4444',
    heal: '#10b981',
    crit: '#f59e0b',
  };

  damageEl.style.color = colors[type];
  damageEl.style.fontSize = type === 'crit' ? '2rem' : '1.5rem';

  const rect = targetElement.getBoundingClientRect();
  damageEl.style.left = `${rect.left + rect.width / 2}px`;
  damageEl.style.top = `${rect.top}px`;

  document.body.appendChild(damageEl);

  setTimeout(() => {
    document.body.removeChild(damageEl);
  }, 2000);
};

/**
 * Create combat effect particles
 */
export const createCombatParticles = (targetElement, count = 10, color = '#3b82f6') => {
  const rect = targetElement.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;

  for (let i = 0; i < count; i++) {
    setTimeout(() => {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${centerX}px`;
      particle.style.top = `${centerY}px`;
      particle.style.backgroundColor = color;

      document.body.appendChild(particle);

      setTimeout(() => {
        document.body.removeChild(particle);
      }, 800);
    }, i * 20);
  }
};

/**
 * Create energy burst effect
 */
export const createEnergyBurst = (targetElement, color = '#3b82f6') => {
  const burst = document.createElement('div');
  burst.className = 'energy-burst';
  burst.style.color = color;

  const rect = targetElement.getBoundingClientRect();
  burst.style.left = `${rect.left + rect.width / 2 - 50}px`;
  burst.style.top = `${rect.top + rect.height / 2 - 50}px`;

  document.body.appendChild(burst);

  setTimeout(() => {
    document.body.removeChild(burst);
  }, 600);
};

/**
 * Screen shake effect
 */
export const shakeScreen = (intensity = 'medium') => {
  const intensityValues = {
    light: 5,
    medium: 10,
    heavy: 20,
  };

  const value = intensityValues[intensity];
  const body = document.body;

  const originalTransform = body.style.transform;

  let frame = 0;
  const maxFrames = 10;

  const shake = () => {
    if (frame >= maxFrames) {
      body.style.transform = originalTransform;
      return;
    }

    const x = (Math.random() - 0.5) * value;
    const y = (Math.random() - 0.5) * value;
    body.style.transform = `translate(${x}px, ${y}px)`;

    frame++;
    requestAnimationFrame(shake);
  };

  shake();
  haptic.heavy();
};

/**
 * Flash effect for critical hits
 */
export const flashScreen = (color = '#ff0000', duration = 200) => {
  const flash = document.createElement('div');
  flash.style.position = 'fixed';
  flash.style.top = '0';
  flash.style.left = '0';
  flash.style.width = '100%';
  flash.style.height = '100%';
  flash.style.backgroundColor = color;
  flash.style.opacity = '0.5';
  flash.style.pointerEvents = 'none';
  flash.style.zIndex = '9999';
  flash.style.transition = `opacity ${duration}ms`;

  document.body.appendChild(flash);

  setTimeout(() => {
    flash.style.opacity = '0';
    setTimeout(() => {
      document.body.removeChild(flash);
    }, duration);
  }, 50);
};

/**
 * Lightning strike effect
 */
export const createLightningStrike = (startElement, endElement) => {
  const startRect = startElement.getBoundingClientRect();
  const endRect = endElement.getBoundingClientRect();

  const lightning = document.createElement('div');
  lightning.className = 'lightning-effect';

  const startX = startRect.left + startRect.width / 2;
  const startY = startRect.top + startRect.height / 2;
  const endX = endRect.left + endRect.width / 2;
  const endY = endRect.top + endRect.height / 2;

  const angle = Math.atan2(endY - startY, endX - startX);
  const length = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));

  lightning.style.left = `${startX}px`;
  lightning.style.top = `${startY}px`;
  lightning.style.width = '2px';
  lightning.style.height = `${length}px`;
  lightning.style.transform = `rotate(${angle + Math.PI / 2}rad)`;
  lightning.style.transformOrigin = 'top';

  document.body.appendChild(lightning);

  setTimeout(() => {
    document.body.removeChild(lightning);
  }, 200);
};

/**
 * Slow motion effect
 */
export const slowMotion = (duration = 1000) => {
  const root = document.documentElement;
  root.style.setProperty('--animation-speed', '0.3');

  setTimeout(() => {
    root.style.setProperty('--animation-speed', '1');
  }, duration);
};

/**
 * Victory celebration effect
 */
export const celebrateVictory = () => {
  // Create confetti
  const colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff'];

  for (let i = 0; i < 50; i++) {
    setTimeout(() => {
      const confetti = document.createElement('div');
      confetti.className = 'confetti';
      confetti.style.left = `${Math.random() * 100}%`;
      confetti.style.top = '-10px';
      confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
      confetti.style.animationDelay = `${Math.random() * 0.5}s`;

      document.body.appendChild(confetti);

      setTimeout(() => {
        document.body.removeChild(confetti);
      }, 3000);
    }, i * 50);
  }

  haptic.success();
};

/**
 * Combo counter animation
 */
export const showComboCounter = (count, targetElement) => {
  const comboEl = document.createElement('div');
  comboEl.className = 'floating-text';
  comboEl.textContent = `${count}x COMBO!`;
  comboEl.style.color = '#f59e0b';
  comboEl.style.fontSize = `${1.5 + count * 0.1}rem`;
  comboEl.style.fontWeight = 'bold';

  const rect = targetElement.getBoundingClientRect();
  comboEl.style.left = `${rect.left + rect.width / 2}px`;
  comboEl.style.top = `${rect.top - 50}px`;

  document.body.appendChild(comboEl);

  setTimeout(() => {
    document.body.removeChild(comboEl);
  }, 2000);

  if (count % 5 === 0) {
    haptic.success();
  }
};
