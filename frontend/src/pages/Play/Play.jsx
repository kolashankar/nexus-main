/**
 * Play/Game page - Full 3D game environment with fullscreen mode and mobile support
 */
import React, { useEffect, useState } from 'react';
import GameWorldEnhanced from '../../components/game/GameWorld/GameWorldEnhanced';
import GameHUD from '../../components/game/GameHUD/GameHUD';
import TaskPanel from '../../components/game/TaskPanel/TaskPanel';
import Marketplace from '../../components/game/Marketplace/Marketplace';
import MobileMenu from '../../components/mobile/MobileMenu';
import { isMobileDevice } from '../../utils/mobileDetection';
import useStore from '../../store';
import { Loader2, Maximize2, Minimize2 } from 'lucide-react';
import './PlayMobile.css';

const Play = () => {
  const { player, fetchPlayer, isLoadingPlayer } = useStore();
  const [gameReady, setGameReady] = useState(false);
  const [showMarketplace, setShowMarketplace] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [showTaskPanel, setShowTaskPanel] = useState(false);
  const [currentMobileTab, setCurrentMobileTab] = useState(null);

  useEffect(() => {
    if (!player) {
      fetchPlayer();
    }
  }, [player, fetchPlayer]);

  useEffect(() => {
    // Game is ready when player data is loaded
    if (player && !isLoadingPlayer) {
      setGameReady(true);
    }
  }, [player, isLoadingPlayer]);

  useEffect(() => {
    // Detect mobile device
    setIsMobile(isMobileDevice());
  }, []);

  const handleTaskComplete = (rewardData) => {
    // Refresh player data to update coin balance
    fetchPlayer();
  };

  const handlePurchase = (purchaseData) => {
    // Refresh player data to update coin balance and inventory
    fetchPlayer();
  };

  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
  };

  const handleMobileMenuClick = (menuItem) => {
    setCurrentMobileTab(menuItem);
    
    switch (menuItem) {
      case 'marketplace':
        setShowMarketplace(true);
        break;
      case 'tasks':
        setShowTaskPanel(!showTaskPanel);
        break;
      case 'inventory':
      case 'quests':
      case 'map':
      case 'social':
      case 'achievements':
      case 'settings':
        // These would open their respective modals/panels
        console.log(`Opening ${menuItem}`);
        break;
      default:
        break;
    }
  };

  if (isLoadingPlayer || !player || !gameReady) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="w-16 h-16 text-purple-500 animate-spin mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-white mb-2">Loading Game...</h2>
          <p className="text-gray-400">Initializing Karma Nexus world</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative w-full h-screen overflow-hidden bg-black">
      {/* 3D Game World */}
      <GameWorldEnhanced player={player} isFullscreen={isFullscreen} />
      
      {/* Mobile Menu - Only on mobile */}
      {isMobile && !isFullscreen && (
        <MobileMenu 
          onMenuItemClick={handleMobileMenuClick}
          currentTab={currentMobileTab}
        />
      )}
      
      {/* Fullscreen Toggle Button - Top Right */}
      <button
        className={`absolute ${isMobile ? 'top-4 right-4' : 'top-4 right-4'} bg-purple-600/80 hover:bg-purple-700 text-white p-3 rounded-lg transition-all duration-300 hover:scale-105 shadow-lg backdrop-blur-sm z-[100]`}
        onClick={toggleFullscreen}
        title={isFullscreen ? "Exit Fullscreen" : "Enter Fullscreen"}
      >
        {isFullscreen ? <Minimize2 className="w-5 h-5" /> : <Maximize2 className="w-5 h-5" />}
      </button>

      {/* Hide UI elements in fullscreen mode */}
      {!isFullscreen && (
        <>
          {/* Game HUD Overlay - Responsive */}
          <div className={isMobile ? 'mobile-hud' : ''}>
            <GameHUD player={player} />
          </div>
          
          {/* Task Panel - Desktop or Mobile Toggle */}
          {!isMobile ? (
            <TaskPanel 
              player={player} 
              onTaskComplete={handleTaskComplete}
            />
          ) : showTaskPanel && (
            <div className="mobile-task-panel">
              <TaskPanel 
                player={player} 
                onTaskComplete={handleTaskComplete}
              />
              <button 
                className="absolute top-2 right-2 bg-red-500/80 text-white px-3 py-1 rounded"
                onClick={() => setShowTaskPanel(false)}
              >
                Close
              </button>
            </div>
          )}
          
          {/* Marketplace Button - Desktop only (mobile uses hamburger menu) */}
          {!isMobile && (
            <button
              className="absolute bottom-20 right-4 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg font-bold transition-all duration-300 hover:scale-105 shadow-lg"
              onClick={() => setShowMarketplace(true)}
              style={{ zIndex: 90 }}
            >
              🏪 Marketplace
            </button>
          )}
          
          {/* Game Instructions - Responsive */}
          <div className={`absolute ${isMobile ? 'bottom-2 left-2' : 'bottom-4 left-4'} bg-black/70 text-white px-4 py-2 rounded-lg text-sm backdrop-blur-sm ${isMobile ? 'text-xs' : ''}`}>
            <p className="font-semibold mb-2 text-cyan-400">Controls:</p>
            <div className="space-y-1 text-xs">
              {!isMobile ? (
                <>
                  <p><span className="text-green-400">↑↓←→ or WASD</span> - Walk</p>
                  <p><span className="text-yellow-400">Shift + Arrows</span> - Run</p>
                  <p><span className="text-blue-400">Ctrl + L / Ctrl + R</span> - Rotate View</p>
                  <p><span className="text-purple-400">Space</span> - Jump</p>
                  <p><span className="text-pink-400">E</span> - Interact</p>
                </>
              ) : (
                <>
                  <p><span className="text-green-400">Joystick</span> - Move</p>
                  <p><span className="text-yellow-400">Run Button</span> - Toggle Run</p>
                  <p><span className="text-purple-400">Jump Button</span> - Jump</p>
                  <p><span className="text-pink-400">Interact Button</span> - Interact</p>
                  <p><span className="text-blue-400">Swipe Screen</span> - Rotate Camera</p>
                </>
              )}
            </div>
          </div>
        </>
      )}

      {/* Fullscreen Mode Instructions */}
      {isFullscreen && (
        <div className="absolute bottom-4 left-4 bg-black/80 text-white px-4 py-2 rounded-lg text-xs backdrop-blur-sm">
          <p className="text-cyan-400 font-semibold">Fullscreen Mode</p>
          <p className="text-gray-300">Press <span className="text-green-400">ESC</span> or click <span className="text-purple-400">⊟</span> to exit</p>
        </div>
      )}

      {/* Marketplace Modal */}
      <Marketplace
        player={player}
        isOpen={showMarketplace}
        onClose={() => setShowMarketplace(false)}
        onPurchase={handlePurchase}
      />
    </div>
  );
};

export default Play;
