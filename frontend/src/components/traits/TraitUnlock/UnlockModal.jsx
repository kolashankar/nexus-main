"""Trait unlock modal component."""

import React from 'react';
import { Unlock, Zap, Star, Award, X } from 'lucide-react';

const UnlockModal = ({ unlock, onClose, isOpen = true }) => {
  if (!isOpen || !unlock) return null;

  const getUnlockTypeIcon = (type) => {
    switch (type) {
      case 'ability':
        return <Zap className="w-8 h-8 text-yellow-400" />;
      case 'trait':
        return <Star className="w-8 h-8 text-purple-400" />;
      case 'skill':
        return <Award className="w-8 h-8 text-blue-400" />;
      default:
        return <Unlock className="w-8 h-8 text-green-400" />;
    }
  };

  const getUnlockTypeColor = (type) => {
    switch (type) {
      case 'ability':
        return 'from-yellow-500 to-amber-500';
      case 'trait':
        return 'from-purple-500 to-pink-500';
      case 'skill':
        return 'from-blue-500 to-cyan-500';
      default:
        return 'from-green-500 to-emerald-500';
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/80 backdrop-blur-sm animate-fadeIn"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative z-10 max-w-md w-full animate-scaleIn">
        <div className={`bg-gradient-to-br ${getUnlockTypeColor(unlock.type)} p-[3px] rounded-2xl shadow-2xl`}>
          <div className="bg-slate-900 rounded-2xl p-8 relative overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-purple-500/10 rounded-full blur-3xl animate-pulse" />
              <div className="absolute bottom-0 left-0 w-48 h-48 bg-blue-500/10 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }} />
            </div>

            {/* Content */}
            <div className="relative z-10">
              {/* Close Button */}
              <button
                onClick={onClose}
                className="absolute top-0 right-0 text-gray-400 hover:text-white transition-colors"
              >
                <X className="w-6 h-6" />
              </button>

              {/* Icon */}
              <div className="flex justify-center mb-6">
                <div className="relative">
                  <div className={`w-24 h-24 rounded-full bg-gradient-to-br ${getUnlockTypeColor(unlock.type)} flex items-center justify-center animate-bounce`}>
                    {getUnlockTypeIcon(unlock.type)}
                  </div>
                  {/* Glow Effect */}
                  <div className={`absolute inset-0 rounded-full bg-gradient-to-br ${getUnlockTypeColor(unlock.type)} blur-xl opacity-50 animate-pulse`} />
                </div>
              </div>

              {/* Title */}
              <div className="text-center mb-6">
                <div className="inline-flex items-center gap-2 px-4 py-1 bg-slate-800/50 rounded-full mb-3">
                  <Unlock className="w-4 h-4 text-green-400" />
                  <span className="text-sm font-semibold text-green-400 uppercase tracking-wider">
                    Unlocked!
                  </span>
                </div>
                <h2 className="text-3xl font-bold text-white mb-2">
                  {unlock.name}
                </h2>
                <p className="text-sm text-gray-400 uppercase tracking-wider">
                  {unlock.type}
                </p>
              </div>

              {/* Description */}
              <div className="bg-slate-800/50 rounded-lg p-4 mb-6">
                <p className="text-gray-300 text-center">
                  {unlock.description}
                </p>
              </div>

              {/* Stats/Effects */}
              {unlock.effects && unlock.effects.length > 0 && (
                <div className="bg-slate-800/30 rounded-lg p-4 mb-6">
                  <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
                    <Zap className="w-4 h-4 text-yellow-400" />
                    Effects
                  </h3>
                  <div className="space-y-2">
                    {unlock.effects.map((effect, idx) => (
                      <div key={idx} className="flex items-start gap-2 text-sm">
                        <span className="text-green-400 mt-0.5">✓</span>
                        <span className="text-gray-300">{effect}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Requirements Met */}
              {unlock.requirement && (
                <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-3 mb-6">
                  <div className="text-xs text-green-400 text-center">
                    <strong>Requirement Met:</strong> {unlock.requirement}
                  </div>
                </div>
              )}

              {/* How to Use */}
              {unlock.howToUse && (
                <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-3 mb-6">
                  <h3 className="text-sm font-semibold text-blue-400 mb-2">How to Use:</h3>
                  <p className="text-xs text-gray-300">{unlock.howToUse}</p>
                </div>
              )}

              {/* Action Button */}
              <button
                onClick={onClose}
                className={`w-full py-3 rounded-lg font-semibold text-white bg-gradient-to-r ${getUnlockTypeColor(unlock.type)} hover:shadow-lg transition-all transform hover:scale-105`}
              >
                Awesome!
              </button>

              {/* Related Unlocks Hint */}
              {unlock.relatedUnlocks && unlock.relatedUnlocks.length > 0 && (
                <div className="mt-4 text-center text-xs text-gray-500">
                  💡 Continue developing this trait to unlock {unlock.relatedUnlocks.length} more abilities
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UnlockModal;
