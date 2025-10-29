import React from 'react';
import './MobileControls.css';

/**
 * Mobile Action Buttons Component
 * Provides Jump, Run, and Interact buttons for mobile gameplay
 */
const MobileControls = ({ 
  onJump, 
  onRunToggle, 
  onInteract, 
  isRunning = false 
}) => {
  return (
    <div className="mobile-controls-container">
      {/* Jump Button */}
      <button
        className="mobile-control-button jump-button"
        onTouchStart={(e) => {
          e.preventDefault();
          onJump && onJump(true);
        }}
        onTouchEnd={(e) => {
          e.preventDefault();
          onJump && onJump(false);
        }}
        aria-label="Jump"
      >
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M12 19V5M5 12l7-7 7 7" />
        </svg>
        <span className="button-label">Jump</span>
      </button>

      {/* Run Toggle Button */}
      <button
        className={`mobile-control-button run-button ${isRunning ? 'active' : ''}`}
        onTouchStart={(e) => {
          e.preventDefault();
          onRunToggle && onRunToggle();
        }}
        aria-label="Run Toggle"
      >
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
        </svg>
        <span className="button-label">Run</span>
      </button>

      {/* Interact Button */}
      <button
        className="mobile-control-button interact-button"
        onTouchStart={(e) => {
          e.preventDefault();
          onInteract && onInteract(true);
        }}
        onTouchEnd={(e) => {
          e.preventDefault();
          onInteract && onInteract(false);
        }}
        aria-label="Interact"
      >
        <svg
          width="28"
          height="28"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2.5"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="10" />
          <path d="M12 8v8M8 12h8" />
        </svg>
        <span className="button-label">Interact</span>
      </button>
    </div>
  );
};

export default MobileControls;
