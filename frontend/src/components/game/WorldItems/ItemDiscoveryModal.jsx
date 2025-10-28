/**
 * ItemDiscoveryModal - Modal shown when player discovers/clicks an item
 */

import React from 'react';

const ItemDiscoveryModal = ({ item, onClose, onAcquire, canAcquire = true, playerLevel, playerCredits }) => {
  if (!item) return null;

  const getItemTypeIcon = () => {
    switch (item.item_type) {
      case 'skill':
        return '🎯';
      case 'superpower_tool':
        return '⚡';
      case 'meta_trait':
        return '✨';
      default:
        return '📦';
    }
  };

  const getRarityColor = () => {
    switch (item.rarity) {
      case 'common':
        return 'text-gray-400';
      case 'uncommon':
        return 'text-green-400';
      case 'rare':
        return 'text-blue-400';
      case 'epic':
        return 'text-purple-400';
      case 'legendary':
        return 'text-yellow-400';
      default:
        return 'text-gray-400';
    }
  };

  const canPlayerAcquire = playerLevel >= item.required_level && playerCredits >= item.cost;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
      <div className="bg-gray-900 border-2 border-cyan-500 rounded-xl p-6 max-w-md w-full mx-4 shadow-2xl">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-center space-x-3">
            <span className="text-4xl">{getItemTypeIcon()}</span>
            <div>
              <h2 className="text-2xl font-bold text-white">{item.item_name}</h2>
              <p className={`text-sm font-semibold ${getRarityColor()}`}>
                {item.rarity.toUpperCase()} {item.item_type.replace('_', ' ').toUpperCase()}
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            ✕
          </button>
        </div>

        {/* Details */}
        <div className="space-y-4">
          {/* Cost */}
          <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
            <span className="text-gray-400">Cost:</span>
            <span className="text-yellow-400 font-bold text-lg">
              {item.cost} credits
            </span>
          </div>

          {/* Level Requirement */}
          <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
            <span className="text-gray-400">Required Level:</span>
            <span className={`font-bold ${
              playerLevel >= item.required_level ? 'text-green-400' : 'text-red-400'
            }`}>
              Level {item.required_level}
            </span>
          </div>

          {/* Time Remaining */}
          {item.time_remaining && (
            <div className="flex items-center justify-between p-3 bg-gray-800 rounded-lg">
              <span className="text-gray-400">Available for:</span>
              <span className="text-cyan-400 font-bold">
                {Math.floor(item.time_remaining / 60)}m {item.time_remaining % 60}s
              </span>
            </div>
          )}

          {/* Player Status */}
          <div className="space-y-2 p-3 bg-gray-800/50 rounded-lg">
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Your Level:</span>
              <span className="text-white font-semibold">{playerLevel}</span>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-gray-400">Your Credits:</span>
              <span className="text-yellow-400 font-semibold">{playerCredits}</span>
            </div>
          </div>

          {/* Warnings */}
          {!canPlayerAcquire && (
            <div className="p-3 bg-red-900/30 border border-red-500 rounded-lg">
              <p className="text-red-400 text-sm">
                {playerLevel < item.required_level && (
                  <span>❌ You need to be level {item.required_level}</span>
                )}
                {playerLevel >= item.required_level && playerCredits < item.cost && (
                  <span>❌ You need {item.cost - playerCredits} more credits</span>
                )}
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex space-x-3 pt-4">
            <button
              onClick={onClose}
              className="flex-1 px-4 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg transition-colors font-semibold"
            >
              Cancel
            </button>
            <button
              onClick={() => canPlayerAcquire && onAcquire(item)}
              disabled={!canPlayerAcquire}
              className={`flex-1 px-4 py-3 rounded-lg font-semibold transition-all ${
                canPlayerAcquire
                  ? 'bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-600 hover:to-blue-700 text-white shadow-lg'
                  : 'bg-gray-600 text-gray-400 cursor-not-allowed'
              }`}
            >
              {canPlayerAcquire ? 'Acquire' : 'Cannot Acquire'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ItemDiscoveryModal;
