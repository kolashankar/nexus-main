import React, { useState } from 'react';
import { X, Menu } from 'lucide-react';
import './MobileMenu.css';

/**
 * Mobile Hamburger Menu Component
 * Provides navigation and access to game features on mobile
 */
const MobileMenu = ({ onMenuItemClick, currentTab }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleMenuClick = (item) => {
    onMenuItemClick && onMenuItemClick(item);
    setIsOpen(false);
  };

  const menuItems = [
    { id: 'inventory', label: 'Inventory', icon: '🎒' },
    { id: 'quests', label: 'Quests', icon: '📜' },
    { id: 'map', label: 'Map', icon: '🗺️' },
    { id: 'social', label: 'Social', icon: '👥' },
    { id: 'achievements', label: 'Achievements', icon: '🏆' },
    { id: 'settings', label: 'Settings', icon: '⚙️' },
    { id: 'marketplace', label: 'Marketplace', icon: '🏪' },
    { id: 'tasks', label: 'Tasks', icon: '📋' }
  ];

  return (
    <>
      {/* Hamburger Button */}
      <button
        className="mobile-menu-button"
        onClick={toggleMenu}
        aria-label="Menu"
      >
        {isOpen ? <X size={24} /> : <Menu size={24} />}
      </button>

      {/* Menu Overlay */}
      {isOpen && (
        <div className="mobile-menu-overlay" onClick={toggleMenu}>
          <div className="mobile-menu-content" onClick={(e) => e.stopPropagation()}>
            <div className="mobile-menu-header">
              <h3>Game Menu</h3>
              <button className="menu-close-button" onClick={toggleMenu}>
                <X size={20} />
              </button>
            </div>

            <div className="mobile-menu-items">
              {menuItems.map((item) => (
                <button
                  key={item.id}
                  className={`mobile-menu-item ${currentTab === item.id ? 'active' : ''}`}
                  onClick={() => handleMenuClick(item.id)}
                >
                  <span className="menu-item-icon">{item.icon}</span>
                  <span className="menu-item-label">{item.label}</span>
                </button>
              ))}
            </div>

            <div className="mobile-menu-footer">
              <p className="text-xs text-gray-400">Karma Nexus 2.0</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default MobileMenu;
