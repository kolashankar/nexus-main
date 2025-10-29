"""Before/After trait comparison component."""

import React from 'react';
import { ArrowRight, TrendingUp, TrendingDown } from 'lucide-react';
import TraitProgressBar from '../TraitProgressBar/TraitProgressBar';

const BeforeAfter = ({ traitChanges, previousTraits, currentTraits }) => {
  const getChangedTraits = () => {
    const changed = [];
    Object.keys(traitChanges).forEach(trait => {
      if (trait !== 'karma_points' && traitChanges[trait] !== 0) {
        changed.push({
          name: trait,
          before: previousTraits?.[trait] || 0,
          after: currentTraits?.[trait] || 0,
          change: traitChanges[trait]
        });
      }
    });
    return changed.sort((a, b) => Math.abs(b.change) - Math.abs(a.change));
  };

  const changedTraits = getChangedTraits();

  if (changedTraits.length === 0) {
    return (
      <div className="text-center py-8 text-gray-400">
        <p>No trait changes to display</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-xl font-bold text-white mb-2">Trait Evolution</h3>
        <p className="text-sm text-gray-400">See how your choices shaped your character</p>
      </div>

      <div className="space-y-4">
        {changedTraits.map(trait => (
          <div
            key={trait.name}
            className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4 border border-purple-500/20"
          >
            {/* Trait Name */}
            <div className="flex items-center justify-between mb-3">
              <h4 className="text-lg font-semibold text-white capitalize">
                {trait.name.replace(/_/g, ' ')}
              </h4>
              <div className={`flex items-center gap-1 px-3 py-1 rounded-full text-sm font-bold ${
                trait.change > 0 
                  ? 'bg-green-500/20 text-green-400' 
                  : 'bg-red-500/20 text-red-400'
              }`}>
                {trait.change > 0 ? (
                  <TrendingUp className="w-4 h-4" />
                ) : (
                  <TrendingDown className="w-4 h-4" />
                )}
                {trait.change > 0 ? '+' : ''}{trait.change}
              </div>
            </div>

            {/* Comparison View */}
            <div className="grid grid-cols-[1fr,auto,1fr] gap-4 items-center">
              {/* Before */}
              <div>
                <div className="text-xs text-gray-400 mb-2">Before</div>
                <div className="bg-slate-900/50 rounded p-3">
                  <TraitProgressBar
                    trait={trait.name}
                    value={trait.before}
                    showLabel={false}
                    size="small"
                  />
                  <div className="text-center mt-2 text-sm font-bold text-gray-300">
                    {Math.round(trait.before)}
                  </div>
                </div>
              </div>

              {/* Arrow */}
              <div className="text-purple-400">
                <ArrowRight className="w-6 h-6" />
              </div>

              {/* After */}
              <div>
                <div className="text-xs text-gray-400 mb-2">After</div>
                <div className="bg-slate-900/50 rounded p-3">
                  <TraitProgressBar
                    trait={trait.name}
                    value={trait.after}
                    showLabel={false}
                    size="small"
                  />
                  <div className="text-center mt-2 text-sm font-bold text-white">
                    {Math.round(trait.after)}
                  </div>
                </div>
              </div>
            </div>

            {/* Impact Description */}
            <div className="mt-3 pt-3 border-t border-slate-700">
              <p className="text-xs text-gray-400">
                {trait.change > 0 ? (
                  <span>
                    Your <span className="text-white font-medium">{trait.name.replace(/_/g, ' ')}</span> has 
                    <span className="text-green-400 font-medium"> increased</span>, making you more aligned with this trait.
                  </span>
                ) : (
                  <span>
                    Your <span className="text-white font-medium">{trait.name.replace(/_/g, ' ')}</span> has 
                    <span className="text-red-400 font-medium"> decreased</span>, distancing you from this trait.
                  </span>
                )}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BeforeAfter;
