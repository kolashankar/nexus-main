/**
 * AcquisitionTracker - Shows active acquisition progress with timer
 */

import React, { useState, useEffect } from 'react';

const AcquisitionTracker = ({ acquisition, onClaim, onCancel }) => {
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (!acquisition) return;

    const updateTimer = () => {
      const now = new Date().getTime();
      const completeTime = new Date(acquisition.completes_at).getTime();
      const startTime = new Date(acquisition.started_at).getTime();
      
      const totalTime = completeTime - startTime;
      const remaining = Math.max(0, completeTime - now);
      const elapsed = totalTime - remaining;
      
      setTimeRemaining(Math.ceil(remaining / 1000));
      setProgress(Math.min(100, (elapsed / totalTime) * 100));
    };

    updateTimer();
    const interval = setInterval(updateTimer, 1000);

    return () => clearInterval(interval);
  }, [acquisition]);

  if (!acquisition) return null;

  const isCompleted = acquisition.status === 'completed' || timeRemaining === 0;

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getItemTypeIcon = () => {
    switch (acquisition.item_type) {
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

  return (
    <div className="fixed bottom-24 right-4 z-40 w-80">
      <div className="bg-gray-900/95 border-2 border-cyan-500 rounded-xl p-4 shadow-2xl backdrop-blur-sm">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <span className="text-2xl">{getItemTypeIcon()}</span>
            <div>
              <h3 className="text-white font-bold text-sm">Acquiring Item</h3>
              <p className="text-cyan-400 text-xs">{acquisition.item_name}</p>
            </div>
          </div>
          {!isCompleted && (
            <button
              onClick={() => onCancel(acquisition.id)}
              className="text-gray-400 hover:text-red-400 transition-colors text-xs"
              title="Cancel (50% refund)"
            >
              ✕
            </button>
          )}
        </div>

        {/* Progress Bar */}
        <div className="mb-3">
          <div className="flex justify-between text-xs text-gray-400 mb-1">
            <span>Progress</span>
            <span>{Math.round(progress)}%</span>
          </div>
          <div className="w-full h-3 bg-gray-700 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all duration-1000 ${
                isCompleted
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600'
                  : 'bg-gradient-to-r from-cyan-500 to-blue-600'
              }`}
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        {/* Status */}
        <div className="space-y-2 mb-3">
          {isCompleted ? (
            <div className="text-center p-2 bg-green-900/30 border border-green-500 rounded-lg">
              <p className="text-green-400 font-bold text-sm">
                ✓ Ready to Claim!
              </p>
            </div>
          ) : (
            <div className="flex items-center justify-between p-2 bg-gray-800 rounded-lg">
              <span className="text-gray-400 text-xs">Time Remaining:</span>
              <span className="text-cyan-400 font-mono font-bold text-sm">
                {formatTime(timeRemaining)}
              </span>
            </div>
          )}

          <div className="flex items-center justify-between p-2 bg-gray-800 rounded-lg">
            <span className="text-gray-400 text-xs">Investment:</span>
            <span className="text-yellow-400 font-bold text-xs">
              {acquisition.cost_paid} credits
            </span>
          </div>
        </div>

        {/* Action Button */}
        {isCompleted && (
          <button
            onClick={() => onClaim(acquisition.id)}
            className="w-full py-3 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg font-bold transition-all shadow-lg hover:shadow-green-500/50 animate-pulse"
          >
            Claim Item
          </button>
        )}

        {!isCompleted && (
          <p className="text-xs text-gray-500 text-center italic">
            Wait for the timer to complete...
          </p>
        )}
      </div>
    </div>
  );
};

export default AcquisitionTracker;
