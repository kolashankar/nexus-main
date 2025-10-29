import React from 'react';
import { Camera, Eye, Maximize } from 'lucide-react';
import './CameraViewToggle.css';

/**
 * Camera View Toggle Component
 * Allows player to switch between different camera views
 */
const CameraViewToggle = ({ currentView, onViewChange, className = '' }) => {
  const views = [
    { id: 'third-person', label: 'Third Person', icon: Camera, shortLabel: '3rd' },
    { id: 'top-down', label: 'Top Down', icon: Maximize, shortLabel: 'Top' },
    { id: 'front', label: 'Front View', icon: Eye, shortLabel: 'Front' },
    { id: 'side', label: 'Side View', icon: Eye, shortLabel: 'Side' },
  ];

  const currentViewData = views.find(v => v.id === currentView) || views[0];
  const CurrentIcon = currentViewData.icon;

  const handleCycleView = () => {
    const currentIndex = views.findIndex(v => v.id === currentView);
    const nextIndex = (currentIndex + 1) % views.length;
    onViewChange(views[nextIndex].id);
  };

  return (
    <div className={`camera-view-toggle ${className}`}>
      <button
        onClick={handleCycleView}
        className="camera-toggle-btn"
        title={`Current: ${currentViewData.label} (Click to switch)`}
      >
        <CurrentIcon className="camera-icon" />
        <span className="camera-label">{currentViewData.shortLabel}</span>
        <span className="camera-hint">📷</span>
      </button>

      {/* View indicator */}
      <div className="view-indicator">
        {views.map((view) => (
          <div
            key={view.id}
            className={`view-dot ${view.id === currentView ? 'active' : ''}`}
            title={view.label}
          />
        ))}
      </div>
    </div>
  );
};

export default CameraViewToggle;
