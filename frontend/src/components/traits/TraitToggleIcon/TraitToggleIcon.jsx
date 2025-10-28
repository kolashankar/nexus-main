import React, { useState } from 'react';
import { Info } from 'lucide-react';
import './TraitToggleIcon.css';

/**
 * Trait Toggle Icon Component
 * Displays a floating icon above characters that shows their traits when clicked
 */
const TraitToggleIcon = ({ traits = [], playerName = 'Player', position = 'top' }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleTraits = () => {
    setIsOpen(!isOpen);
  };

  // Categorize traits
  const goodTraits = traits.filter(t => t.type === 'virtue' || t.category === 'good');
  const badTraits = traits.filter(t => t.type === 'vice' || t.category === 'bad');
  const metaTraits = traits.filter(t => t.type === 'meta' || t.category === 'meta');

  return (
    <div className={`trait-toggle-container position-${position}`}>
      {/* Toggle Button */}
      <button
        className="trait-toggle-button"
        onClick={toggleTraits}
        title={`View ${playerName}'s traits`}
      >
        <Info className="w-4 h-4" />
        {traits.length > 0 && (
          <span className="trait-count-badge">{traits.length}</span>
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
            {traits.length === 0 ? (
              <p className="no-traits-message">No traits yet</p>
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
                          <span className="trait-level">Lv.{trait.level || 1}</span>
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
                          <span className="trait-level">Lv.{trait.level || 1}</span>
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
                          <span className="trait-level">Lv.{trait.level || 1}</span>
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
