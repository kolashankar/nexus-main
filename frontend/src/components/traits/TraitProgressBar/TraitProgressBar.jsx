"""Trait progress bar component."""

import React from 'react';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const TraitProgressBar = ({ trait, value, maxValue = 100, showLabel = true, showTrend = false, previousValue = null, size = 'medium' }) => {
  const percentage = Math.min(100, Math.max(0, (value / maxValue) * 100));
  const change = previousValue !== null ? value - previousValue : 0;
  
  const getTraitColor = (traitName) => {
    const virtues = ['kindness', 'compassion', 'honesty', 'courage', 'wisdom', 'patience', 'loyalty', 'humility'];
    const vices = ['greed', 'wrath', 'envy', 'sloth', 'pride', 'gluttony', 'lust'];
    
    if (virtues.includes(traitName.toLowerCase())) {
      return 'from-blue-500 to-cyan-500';
    } else if (vices.includes(traitName.toLowerCase())) {
      return 'from-red-500 to-orange-500';
    }
    return 'from-purple-500 to-pink-500';
  };

  const getMilestoneThresholds = () => {
    return [25, 50, 75, 100];
  };

  const getCurrentMilestone = () => {
    const thresholds = getMilestoneThresholds();
    for (let i = 0; i < thresholds.length; i++) {
      if (value < thresholds[i]) {
        return { current: i, threshold: thresholds[i], previous: i > 0 ? thresholds[i - 1] : 0 };
      }
    }
    return { current: 4, threshold: 100, previous: 75 };
  };

  const milestone = getCurrentMilestone();
  const sizeClasses = {
    small: 'h-2',
    medium: 'h-4',
    large: 'h-6'
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-white capitalize">
              {trait.replace(/_/g, ' ')}
            </span>
            {showTrend && change !== 0 && (
              <span className={`flex items-center gap-1 text-xs ${
                change > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {change > 0 ? (
                  <TrendingUp className="w-3 h-3" />
                ) : change < 0 ? (
                  <TrendingDown className="w-3 h-3" />
                ) : (
                  <Minus className="w-3 h-3" />
                )}
                {Math.abs(change)}
              </span>
            )}
          </div>
          <span className="text-sm font-bold text-gray-300">
            {Math.round(value)}/{maxValue}
          </span>
        </div>
      )}

      <div className="relative">
        {/* Background */}
        <div className={`${sizeClasses[size]} w-full bg-slate-700 rounded-full overflow-hidden`}>
          {/* Progress Fill */}
          <div
            className={`h-full bg-gradient-to-r ${getTraitColor(trait)} transition-all duration-500 ease-out relative`}
            style={{ width: `${percentage}%` }}
          >
            {/* Shine Effect */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer" />
          </div>
        </div>

        {/* Milestone Markers */}
        <div className="absolute top-0 left-0 w-full h-full flex justify-between px-[1px]">
          {getMilestoneThresholds().slice(0, -1).map((threshold, idx) => (
            <div
              key={threshold}
              className="relative"
              style={{ left: `${threshold}%` }}
            >
              <div className={`absolute top-0 w-0.5 ${sizeClasses[size]} ${
                value >= threshold ? 'bg-yellow-400' : 'bg-slate-600'
              }`} />
            </div>
          ))}
        </div>
      </div>

      {/* Milestone Info */}
      {showLabel && (
        <div className="mt-1 text-xs text-gray-400">
          Level {milestone.current}/4 • Next milestone at {milestone.threshold}
        </div>
      )}
    </div>
  );
};

export default TraitProgressBar;
