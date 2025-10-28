import React, { useState, useEffect } from 'react';
import './TraitEffectsDisplay.css';

const TraitEffectsDisplay = ({ player }) => {
  const [activeBuffs, setActiveBuffs] = useState([]);
  const [activeDebuffs, setActiveDebuffs] = useState([]);

  useEffect(() => {
    if (player) {
      setActiveBuffs(player.buffs || []);
      setActiveDebuffs(player.debuffs || []);
    }
  }, [player]);

  const getEffectColor = (type) => {
    const colors = {
      // Buffs
      'persuaded': '#10b981',
      'favorable_deal': '#3b82f6',
      'peaceful_resolution': '#60a5fa',
      'force_field': '#a855f7',
      'object_control': '#8b5cf6',
      'levitating': '#c084fc',
      'inferno_shield': '#f97316',
      'heat_aura': '#fb923c',
      'frozen_armor': '#06b6d4',
      'inner_peace': '#10b981',
      'energy_recovery': '#fbbf24',
      'clarity_boost': '#60a5fa',
      
      // Debuffs
      'stunned': '#ef4444',
      'burning': '#f97316',
      'slowed': '#06b6d4',
      'frozen': '#0ea5e9',
      'frostbite': '#0284c7',
      'blizzard_damage': '#0891b2',
      'blizzard_slow': '#06b6d4',
      'intimidated': '#dc2626',
      'demoralized': '#991b1b',
      'weakened': '#b91c1c'
    };
    return colors[type] || '#6b7280';
  };

  const getEffectIcon = (type) => {
    const icons = {
      'persuaded': '🗣️',
      'favorable_deal': '🤝',
      'peaceful_resolution': '☮️',
      'force_field': '🛡️',
      'levitating': '✨',
      'inferno_shield': '🔥',
      'heat_aura': '🌡️',
      'frozen_armor': '❄️',
      'stunned': '💫',
      'burning': '🔥',
      'slowed': '🐌',
      'frozen': '🧊',
      'inner_peace': '🧘',
      'energy_recovery': '⚡',
      'clarity_boost': '💡'
    };
    return icons[type] || '✨';
  };

  const formatEffectName = (type) => {
    return type.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ');
  };

  const getRemainingTime = (expiresAt) => {
    if (!expiresAt) return null;
    const now = new Date();
    const expires = new Date(expiresAt);
    const diff = Math.max(0, expires - now);
    return Math.ceil(diff / 1000); // seconds
  };

  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds}s`;
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds}s`;
  };

  return (
    <div className="trait-effects-display">
      {/* Active Buffs */}
      {activeBuffs.length > 0 && (
        <div className="effects-section buffs-section">
          <h4 className="effects-title">Active Buffs</h4>
          <div className="effects-list">
            {activeBuffs.map((buff, idx) => {
              const remainingTime = getRemainingTime(buff.expires_at);
              return (
                <div
                  key={idx}
                  className="effect-item buff-item"
                  style={{ borderColor: getEffectColor(buff.type) }}
                >
                  <div className="effect-icon">{getEffectIcon(buff.type)}</div>
                  <div className="effect-details">
                    <div className="effect-name" style={{ color: getEffectColor(buff.type) }}>
                      {formatEffectName(buff.type)}
                    </div>
                    {buff.value && (
                      <div className="effect-value">+{buff.value.toFixed(0)}%</div>
                    )}
                    {remainingTime && (
                      <div className="effect-timer">{formatTime(remainingTime)}</div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Active Debuffs */}
      {activeDebuffs.length > 0 && (
        <div className="effects-section debuffs-section">
          <h4 className="effects-title">Active Debuffs</h4>
          <div className="effects-list">
            {activeDebuffs.map((debuff, idx) => {
              const remainingTime = getRemainingTime(debuff.expires_at);
              return (
                <div
                  key={idx}
                  className="effect-item debuff-item"
                  style={{ borderColor: getEffectColor(debuff.type) }}
                >
                  <div className="effect-icon">{getEffectIcon(debuff.type)}</div>
                  <div className="effect-details">
                    <div className="effect-name" style={{ color: getEffectColor(debuff.type) }}>
                      {formatEffectName(debuff.type)}
                    </div>
                    {debuff.value && (
                      <div className="effect-value">-{debuff.value.toFixed(0)}%</div>
                    )}
                    {debuff.damage_per_tick && (
                      <div className="effect-value">{debuff.damage_per_tick.toFixed(0)} DMG/tick</div>
                    )}
                    {remainingTime && (
                      <div className="effect-timer">{formatTime(remainingTime)}</div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {activeBuffs.length === 0 && activeDebuffs.length === 0 && (
        <div className="no-effects">
          <p>No active effects</p>
        </div>
      )}
    </div>
  );
};

export default TraitEffectsDisplay;