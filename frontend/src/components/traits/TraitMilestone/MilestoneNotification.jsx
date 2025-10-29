"""Trait milestone notification component."""

import React, { useEffect, useState } from 'react';
import { Trophy, Star, Sparkles, X } from 'lucide-react';

const MilestoneNotification = ({ milestone, onClose, autoClose = true }) => {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Fade in animation
    setTimeout(() => setIsVisible(true), 100);

    // Auto close after 5 seconds
    if (autoClose) {
      const timer = setTimeout(() => {
        handleClose();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [autoClose]);

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => onClose?.(), 300); // Wait for fade out
  };

  const getMilestoneLevel = (value) => {
    if (value >= 100) return { level: 'Master', color: 'amber', icon: '👑' };
    if (value >= 75) return { level: 'Expert', color: 'purple', icon: '⭐' };
    if (value >= 50) return { level: 'Proficient', color: 'blue', icon: '💎' };
    if (value >= 25) return { level: 'Apprentice', color: 'green', icon: '🌟' };
    return { level: 'Novice', color: 'gray', icon: '✨' };
  };

  if (!milestone) return null;

  const level = getMilestoneLevel(milestone.value);
  const colorClasses = {
    amber: 'from-amber-500 to-yellow-500 border-amber-500',
    purple: 'from-purple-500 to-pink-500 border-purple-500',
    blue: 'from-blue-500 to-cyan-500 border-blue-500',
    green: 'from-green-500 to-emerald-500 border-green-500',
    gray: 'from-gray-500 to-slate-500 border-gray-500'
  };

  return (
    <div className={`fixed bottom-6 right-6 z-50 transition-all duration-300 ${
      isVisible ? 'translate-y-0 opacity-100' : 'translate-y-4 opacity-0'
    }`}>
      <div className={`relative bg-gradient-to-br ${colorClasses[level.color]} p-[2px] rounded-lg shadow-2xl max-w-sm`}>
        <div className="bg-slate-900 rounded-lg p-6 relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 opacity-10">
            <div className="absolute top-0 right-0 w-32 h-32 bg-white rounded-full blur-3xl" />
            <div className="absolute bottom-0 left-0 w-24 h-24 bg-white rounded-full blur-2xl" />
          </div>

          {/* Content */}
          <div className="relative z-10">
            {/* Close Button */}
            <button
              onClick={handleClose}
              className="absolute top-0 right-0 text-gray-400 hover:text-white transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            {/* Icon */}
            <div className="flex items-center justify-center mb-4">
              <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${colorClasses[level.color]} flex items-center justify-center text-3xl animate-bounce`}>
                {level.icon}
              </div>
            </div>

            {/* Title */}
            <div className="text-center mb-2">
              <div className="flex items-center justify-center gap-2 mb-1">
                <Sparkles className="w-4 h-4 text-yellow-400" />
                <h3 className="text-lg font-bold text-white">Milestone Reached!</h3>
                <Sparkles className="w-4 h-4 text-yellow-400" />
              </div>
              <p className="text-sm text-gray-300">
                Your <span className="font-semibold text-white capitalize">{milestone.trait.replace(/_/g, ' ')}</span> has
                reached <span className={`font-bold text-${level.color}-400`}>{level.level}</span> level
              </p>
            </div>

            {/* Value Display */}
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="text-center">
                <div className="text-3xl font-bold text-white">
                  {Math.round(milestone.value)}
                </div>
                <div className="text-xs text-gray-400">Current Value</div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r ${colorClasses[level.color]} transition-all duration-1000`}
                  style={{ width: `${milestone.value}%` }}
                />
              </div>
            </div>

            {/* Rewards */}
            {milestone.rewards && (
              <div className="bg-slate-800/50 rounded-lg p-3">
                <div className="flex items-center gap-2 mb-2">
                  <Trophy className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-semibold text-white">Rewards</span>
                </div>
                <div className="space-y-1 text-xs text-gray-300">
                  {milestone.rewards.xp && (
                    <div>✨ +{milestone.rewards.xp} XP</div>
                  )}
                  {milestone.rewards.credits && (
                    <div>💰 +{milestone.rewards.credits} Credits</div>
                  )}
                  {milestone.rewards.unlocks && milestone.rewards.unlocks.length > 0 && (
                    <div>🔓 New abilities unlocked!</div>
                  )}
                </div>
              </div>
            )}

            {/* Next Milestone */}
            {milestone.value < 100 && (
              <div className="mt-3 text-center text-xs text-gray-400">
                Next milestone at {milestone.nextMilestone || (Math.floor(milestone.value / 25) + 1) * 25}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MilestoneNotification;
