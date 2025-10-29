"""React hook for trait progress tracking."""

import { useState, useEffect, useCallback } from 'react';
import { toast } from 'react-hot-toast';

export const useTraitProgress = (playerTraits = {}) => {
  const [previousTraits, setPreviousTraits] = useState(playerTraits);
  const [traitChanges, setTraitChanges] = useState({});
  const [milestones, setMilestones] = useState([]);
  const [unlocks, setUnlocks] = useState([]);

  // Track trait changes
  useEffect(() => {
    if (Object.keys(playerTraits).length > 0 && Object.keys(previousTraits).length > 0) {
      const changes = {};
      Object.keys(playerTraits).forEach(trait => {
        const oldValue = previousTraits[trait] || 0;
        const newValue = playerTraits[trait] || 0;
        if (oldValue !== newValue) {
          changes[trait] = newValue - oldValue;
        }
      });
      
      if (Object.keys(changes).length > 0) {
        setTraitChanges(changes);
        checkForMilestones(changes, playerTraits);
        checkForUnlocks(changes, playerTraits);
      }
    }
  }, [playerTraits]);

  // Check for milestone achievements
  const checkForMilestones = useCallback((changes, currentTraits) => {
    const newMilestones = [];
    const milestoneThresholds = [25, 50, 75, 100];

    Object.keys(changes).forEach(trait => {
      const oldValue = previousTraits[trait] || 0;
      const newValue = currentTraits[trait] || 0;

      milestoneThresholds.forEach(threshold => {
        // Check if we crossed a milestone
        if (oldValue < threshold && newValue >= threshold) {
          newMilestones.push({
            trait,
            value: newValue,
            threshold,
            rewards: calculateMilestoneRewards(trait, threshold)
          });
        }
      });
    });

    if (newMilestones.length > 0) {
      setMilestones(prev => [...prev, ...newMilestones]);
      // Show first milestone notification
      if (newMilestones.length > 0) {
        toast.success(`🎉 ${newMilestones[0].trait.replace(/_/g, ' ')} milestone reached!`, {
          duration: 3000
        });
      }
    }
  }, [previousTraits]);

  // Check for trait unlocks
  const checkForUnlocks = useCallback((changes, currentTraits) => {
    const newUnlocks = [];

    Object.keys(changes).forEach(trait => {
      const value = currentTraits[trait] || 0;
      const unlock = getTraitUnlock(trait, value);
      if (unlock) {
        newUnlocks.push(unlock);
      }
    });

    if (newUnlocks.length > 0) {
      setUnlocks(prev => [...prev, ...newUnlocks]);
    }
  }, []);

  // Calculate milestone rewards
  const calculateMilestoneRewards = (trait, threshold) => {
    const baseXP = threshold * 2;
    const baseCredits = threshold * 5;

    const rewards = {
      xp: baseXP,
      credits: baseCredits
    };

    // Special unlocks at major milestones
    if (threshold === 50) {
      rewards.unlocks = [`${trait}_intermediate_ability`];
    } else if (threshold === 75) {
      rewards.unlocks = [`${trait}_advanced_ability`];
    } else if (threshold === 100) {
      rewards.unlocks = [`${trait}_master_ability`];
    }

    return rewards;
  };

  // Get trait unlock information
  const getTraitUnlock = (trait, value) => {
    const unlockThresholds = [
      { value: 50, level: 'intermediate' },
      { value: 75, level: 'advanced' },
      { value: 100, level: 'master' }
    ];

    for (const threshold of unlockThresholds) {
      if (value === threshold.value) {
        return {
          type: 'ability',
          name: `${trait.replace(/_/g, ' ')} ${threshold.level}`.replace(/\b\w/g, l => l.toUpperCase()),
          description: `You've unlocked a ${threshold.level} ability for ${trait.replace(/_/g, ' ')}!`,
          trait,
          level: threshold.level,
          requirement: `Reach ${threshold.value} in ${trait.replace(/_/g, ' ')}`,
          effects: getAbilityEffects(trait, threshold.level),
          howToUse: `Use this ability in combat or tasks to gain advantages related to ${trait.replace(/_/g, ' ')}.`
        };
      }
    }

    return null;
  };

  // Get ability effects based on trait and level
  const getAbilityEffects = (trait, level) => {
    const effectMultiplier = level === 'intermediate' ? 1 : level === 'advanced' ? 1.5 : 2;
    
    const baseEffects = {
      courage: [`+${Math.round(20 * effectMultiplier)}% combat effectiveness`, `Unlock brave choices in tasks`],
      wisdom: [`+${Math.round(15 * effectMultiplier)}% XP gain`, `Better decision insights`],
      compassion: [`Healing abilities`, `Positive karma bonuses`],
      strength: [`+${Math.round(25 * effectMultiplier)}% physical damage`, `Intimidation options`],
      intelligence: [`+${Math.round(20 * effectMultiplier)}% skill learning`, `Hacking abilities`],
      charisma: [`Better trading prices`, `Persuasion options`],
      luck: [`+${Math.round(10 * effectMultiplier)}% critical chance`, `Random bonus rewards`]
    };

    return baseEffects[trait] || [`Enhanced ${trait.replace(/_/g, ' ')} abilities`];
  };

  // Update previous traits after processing
  const updatePreviousTraits = useCallback(() => {
    setPreviousTraits(playerTraits);
    setTraitChanges({});
  }, [playerTraits]);

  // Dismiss milestone notification
  const dismissMilestone = useCallback((index) => {
    setMilestones(prev => prev.filter((_, idx) => idx !== index));
  }, []);

  // Dismiss unlock notification
  const dismissUnlock = useCallback((index) => {
    setUnlocks(prev => prev.filter((_, idx) => idx !== index));
  }, []);

  // Get trait level name
  const getTraitLevel = useCallback((value) => {
    if (value >= 100) return 'Master';
    if (value >= 75) return 'Expert';
    if (value >= 50) return 'Proficient';
    if (value >= 25) return 'Apprentice';
    return 'Novice';
  }, []);

  // Calculate next milestone
  const getNextMilestone = useCallback((value) => {
    const thresholds = [25, 50, 75, 100];
    for (const threshold of thresholds) {
      if (value < threshold) {
        return threshold;
      }
    }
    return null; // Max level reached
  }, []);

  return {
    traitChanges,
    milestones,
    unlocks,
    previousTraits,
    updatePreviousTraits,
    dismissMilestone,
    dismissUnlock,
    getTraitLevel,
    getNextMilestone
  };
};
