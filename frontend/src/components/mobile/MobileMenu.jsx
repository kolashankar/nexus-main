import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  X, Menu, Home, User, Gamepad2, Swords, Zap, 
  Users, Trophy, BookOpen, Map, Settings, Store,
  ClipboardList, TrendingUp, Shield, Sparkles
} from 'lucide-react';
import './MobileMenu.css';

/**
 * Mobile Hamburger Menu Component
 * Provides navigation and access to game features on mobile
 */
const MobileMenu = ({ onMenuItemClick, currentTab }) => {
  const [isOpen, setIsOpen] = useState(false);
  const navigate = useNavigate();

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  const handleMenuClick = (item) => {
    // If item has a route, navigate to it
    if (item.route) {
      navigate(item.route);
      setIsOpen(false);
    } 
    // Otherwise, trigger the callback for in-game actions
    else {
      onMenuItemClick && onMenuItemClick(item.id);
      setIsOpen(false);
    }
  };

  const menuItems = [
    // Navigation Items
    { id: 'dashboard', label: 'Dashboard', icon: Home, route: '/dashboard' },
    { id: 'profile', label: 'Profile', icon: User, route: '/profile' },
    { id: 'play', label: 'Play Game', icon: Gamepad2, route: '/play' },
    
    // Game Features
    { id: 'tasks', label: 'Tasks', icon: ClipboardList },
    { id: 'quests', label: 'Quests', icon: BookOpen },
    { id: 'combat', label: 'Combat', icon: Swords, route: '/combat' },
    { id: 'marketplace', label: 'Marketplace', icon: Store },
    
    // Progression & Social
    { id: 'progression', label: 'Progression', icon: TrendingUp, route: '/progression' },
    { id: 'karma', label: 'Karma', icon: Sparkles, route: '/karma' },
    { id: 'skills', label: 'Skills', icon: Zap, route: '/skills' },
    { id: 'guild', label: 'Guild', icon: Shield, route: '/guild' },
    { id: 'social', label: 'Social Hub', icon: Users, route: '/social' },
    
    // Other Features
    { id: 'map', label: 'World Map', icon: Map, route: '/world' },
    { id: 'achievements', label: 'Achievements', icon: Trophy },
    { id: 'settings', label: 'Settings', icon: Settings }
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
              {menuItems.map((item) => {
                const IconComponent = item.icon;
                return (
                  <button
                    key={item.id}
                    className={`mobile-menu-item ${currentTab === item.id ? 'active' : ''}`}
                    onClick={() => handleMenuClick(item)}
                  >
                    <span className="menu-item-icon">
                      <IconComponent size={20} />
                    </span>
                    <span className="menu-item-label">{item.label}</span>
                  </button>
                );
              })}
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
