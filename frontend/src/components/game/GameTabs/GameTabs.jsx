import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { X, Target, Package, Settings, Map, Users, Trophy } from 'lucide-react';
import QuestsTab from './QuestsTab';
import InventoryTab from './InventoryTab';
import SettingsTab from './SettingsTab';
import MapTab from './MapTab';
import SocialTab from './SocialTab';
import AchievementsTab from './AchievementsTab';
import './GameTabs.css';

/**
 * GameTabs Component
 * Tabbed navigation system for game interface
 * Accessible via Tab key or button
 */
const GameTabs = ({ player, isOpen, onClose }) => {
  const [activeTab, setActiveTab] = useState('quests');

  const tabs = [
    { id: 'quests', label: 'Quests', icon: Target },
    { id: 'inventory', label: 'Inventory', icon: Package },
    { id: 'map', label: 'Map', icon: Map },
    { id: 'social', label: 'Social', icon: Users },
    { id: 'achievements', label: 'Achievements', icon: Trophy },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  if (!isOpen) return null;

  const renderTabContent = () => {
    switch (activeTab) {
      case 'quests':
        return <QuestsTab player={player} />;
      case 'inventory':
        return <InventoryTab player={player} />;
      case 'map':
        return <MapTab player={player} />;
      case 'social':
        return <SocialTab player={player} />;
      case 'achievements':
        return <AchievementsTab player={player} />;
      case 'settings':
        return <SettingsTab player={player} />;
      default:
        return <QuestsTab player={player} />;
    }
  };

  return (
    <div className="game-tabs-overlay" onClick={onClose}>
      <div className="game-tabs-container" onClick={(e) => e.stopPropagation()}>
        <Card className="game-tabs-modal">
          {/* Header */}
          <div className="tabs-header">
            <h2 className="tabs-title">Game Menu</h2>
            <button className="tabs-close-btn" onClick={onClose}>
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Tab Navigation */}
          <div className="tabs-navigation">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  <Icon className="w-5 h-5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Content */}
          <div className="tabs-content">
            {renderTabContent()}
          </div>

          {/* Footer Hint */}
          <div className="tabs-footer">
            <p className="text-gray-400 text-sm">Press <kbd>Tab</kbd> or <kbd>Esc</kbd> to close</p>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default GameTabs;