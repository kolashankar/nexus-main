import React, { useState, useEffect } from 'react';
import './TraitActionPanel.css';

const TraitActionPanel = ({ player, onUseAbility }) => {
  const [selectedTrait, setSelectedTrait] = useState(null);
  const [selectedAbility, setSelectedAbility] = useState(null);
  const [targetSelection, setTargetSelection] = useState(false);
  const [cooldowns, setCooldowns] = useState({});

  // Group traits by category
  const groupedTraits = {
    skills: player?.traits?.skills || [],
    superpower_tools: player?.traits?.superpower_tools || [],
    meta: player?.traits?.meta || [],
    good: player?.traits?.good || [],
    bad: player?.traits?.bad || []
  };

  // Ability definitions for each trait
  const abilityMap = {
    // Skills
    'Hacking': ['system_breach', 'data_extraction', 'disable_security'],
    'Negotiation': ['persuade', 'broker_deal', 'resolve_conflict'],
    'Stealth': ['shadow_blend', 'silent_movement'],
    'Leadership': ['rally_troops', 'inspire_courage', 'tactical_command'],
    
    // Superpower Tools
    'Meditation Superpower': ['inner_peace', 'energy_recovery', 'clarity_boost'],
    'Telekinesis': ['force_push', 'force_field', 'object_manipulation', 'levitate'],
    'Pyrokinesis': ['flame_burst', 'inferno_shield', 'pyroclasm', 'heat_generation'],
    'Cryokinesis': ['ice_blast', 'frozen_armor', 'deep_freeze', 'ice_construct', 'blizzard'],
    
    // Good Traits
    'Empathy': ['emotional_insight', 'soothe_emotions', 'share_burden'],
    'Integrity': ['truth_aura', 'resist_corruption'],
    'Compassion': ['healing_touch'],
    'Honesty': ['truth_reveal'],
    
    // Bad Traits
    'Envy': ['stat_drain'],
    'Wrath': ['berserker_rage'],
    'Sloth': ['energy_siphon', 'lazy_dodge'],
    'Pride': ['superior_presence'],
    
    // Meta Traits
    'Luck': ['fortunes_favor', 'lucky_escape', 'treasure_sense'],
    'Resilience': ['unbreakable_will', 'damage_threshold'],
    'Wisdom': ['sage_insight', 'learning_acceleration'],
    'Adaptability': ['quick_adaptation', 'environment_mastery', 'copy_ability']
  };

  const handleTraitSelect = (trait) => {
    setSelectedTrait(trait);
    setSelectedAbility(null);
  };

  const handleAbilitySelect = (ability) => {
    setSelectedAbility(ability);
  };

  const handleUseAbility = async () => {
    if (!selectedTrait || !selectedAbility) return;

    const abilityKey = `${selectedTrait.name}_${selectedAbility}`;
    
    // Check cooldown
    if (cooldowns[abilityKey]) {
      alert('Ability is on cooldown!');
      return;
    }

    try {
      await onUseAbility({
        traitName: selectedTrait.name,
        abilityName: selectedAbility,
        traitLevel: selectedTrait.level
      });

      // Set cooldown (30 seconds for most abilities)
      setCooldowns(prev => ({ ...prev, [abilityKey]: true }));
      setTimeout(() => {
        setCooldowns(prev => ({ ...prev, [abilityKey]: false }));
      }, 30000);
    } catch (error) {
      console.error('Failed to use ability:', error);
    }
  };

  const formatAbilityName = (ability) => {
    return ability.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const getCategoryColor = (category) => {
    const colors = {
      skills: '#3b82f6',
      superpower_tools: '#a855f7',
      meta: '#f59e0b',
      good: '#10b981',
      bad: '#ef4444'
    };
    return colors[category] || '#6b7280';
  };

  return (
    <div className="trait-action-panel">
      <div className="panel-header">
        <h3>Trait Abilities</h3>
        <div className="energy-display">
          <span>Energy: {player?.energy?.current || 0}/{player?.energy?.max || 100}</span>
        </div>
      </div>

      <div className="panel-content">
        {/* Trait Categories */}
        <div className="trait-categories">
          {Object.entries(groupedTraits).map(([category, traits]) => (
            traits.length > 0 && (
              <div key={category} className="trait-category">
                <h4 style={{ color: getCategoryColor(category) }}>
                  {category.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                </h4>
                <div className="trait-list">
                  {traits.map((trait, idx) => (
                    <div
                      key={idx}
                      className={`trait-item ${selectedTrait?.name === trait.name ? 'selected' : ''}`}
                      onClick={() => handleTraitSelect(trait)}
                      style={{ borderColor: getCategoryColor(category) }}
                    >
                      <div className="trait-name">{trait.name}</div>
                      <div className="trait-level">Lv {trait.level}</div>
                    </div>
                  ))}
                </div>
              </div>
            )
          ))}
        </div>

        {/* Ability Selection */}
        {selectedTrait && (
          <div className="ability-selection">
            <h4>{selectedTrait.name} Abilities</h4>
            <div className="ability-list">
              {(abilityMap[selectedTrait.name] || []).map((ability) => {
                const abilityKey = `${selectedTrait.name}_${ability}`;
                const onCooldown = cooldowns[abilityKey];

                return (
                  <div
                    key={ability}
                    className={`ability-item ${selectedAbility === ability ? 'selected' : ''} ${onCooldown ? 'cooldown' : ''}`}
                    onClick={() => !onCooldown && handleAbilitySelect(ability)}
                  >
                    <div className="ability-name">{formatAbilityName(ability)}</div>
                    {onCooldown && <div className="cooldown-badge">Cooldown</div>}
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* Use Button */}
        {selectedAbility && (
          <div className="action-buttons">
            <button
              className="use-ability-btn"
              onClick={handleUseAbility}
              disabled={!player?.energy?.current || player.energy.current < 10}
            >
              Use {formatAbilityName(selectedAbility)}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default TraitActionPanel;