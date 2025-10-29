import React, { useState } from 'react';
import { Info } from 'lucide-react';
import './TraitToggleIcon.css';

/**
 * Trait Toggle Icon Component
 * Displays a floating icon above characters that shows their traits when clicked
 * Now properly handles array of trait objects
 */
const TraitToggleIcon = ({ traits = [], playerName = 'Player', position = 'top' }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleTraits = () => {
    setIsOpen(!isOpen);
  };

  // Ensure traits is an array
  const traitsArray = Array.isArray(traits) ? traits : [];

  // Categorize traits
  const goodTraits = traitsArray.filter(t => t.type === 'virtue' || t.category === 'good');
  const badTraits = traitsArray.filter(t => t.type === 'vice' || t.category === 'bad');
  const metaTraits = traitsArray.filter(t => t.type === 'meta' || t.category === 'meta');
  const skillTraits = traitsArray.filter(t => t.type === 'skill' || t.category === 'skill');

  return (
    <div className={`trait-toggle-container position-${position}`}>
      {/* Toggle Button */}
      <button
        className="trait-toggle-button"
        onClick={toggleTraits}
        title={`View ${playerName}'s traits`}
      >
        <Info className="w-4 h-4" />
        {traitsArray.length > 0 && (
          <span className="trait-count-badge">{traitsArray.length}</span>
        )}
      </button>

      {/* Traits Panel */}
      {isOpen && (
        <div className="traits-panel">
          <div className="traits-panel-header">
            <h3 className="traits-panel-title">{playerName}'s Traits</h3>
            <button 
              className="traits-panel-close"
              onClick={toggleTraits}
              aria-label="Close"
            >
              ×
            </button>
          </div>

          <div className="traits-panel-content">
            {traitsArray.length === 0 ? (
              <div className="no-traits-message">
                <p>No distinctive traits yet</p>
                <p className="text-sm text-gray-400 mt-2">
                  Complete tasks and actions to develop your character's traits.
                </p>
              </div>
            ) : (
              <>
                {/* Good Traits */}
                {goodTraits.length > 0 && (
                  <div className="trait-section">
                    <h4 className="trait-section-title good">Virtues</h4>
                    <div className="trait-list">
                      {goodTraits.map((trait, index) => (
                        <div key={index} className="trait-item good">
                          <span className="trait-name">{trait.name}</span>
                          <span className="trait-level">Lv.{trait.level || 50}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Bad Traits */}
                {badTraits.length > 0 && (
                  <div className="trait-section">
                    <h4 className="trait-section-title bad">Vices</h4>
                    <div className="trait-list">
                      {badTraits.map((trait, index) => (
                        <div key={index} className="trait-item bad">
                          <span className="trait-name">{trait.name}</span>
                          <span className="trait-level">Lv.{trait.level || 50}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skills */}
                {skillTraits.length > 0 && (
                  <div className="trait-section">
                    <h4 className="trait-section-title skill">Skills</h4>
                    <div className="trait-list">
                      {skillTraits.map((trait, index) => (
                        <div key={index} className="trait-item skill">
                          <span className="trait-name">{trait.name}</span>
                          <span className="trait-level">Lv.{trait.level || 50}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Meta Traits */}
                {metaTraits.length > 0 && (
                  <div className="trait-section">
                    <h4 className="trait-section-title meta">Meta Traits</h4>
                    <div className="trait-list">
                      {metaTraits.map((trait, index) => (
                        <div key={index} className="trait-item meta">
                          <span className="trait-name">{trait.name}</span>
                          <span className="trait-level">Lv.{trait.level || 50}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default TraitToggleIcon;
