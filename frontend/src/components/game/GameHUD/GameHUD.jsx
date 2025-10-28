/**
 * GameHUD - Game Heads-Up Display overlay
 */
import React, { useState } from 'react';
import { 
  Heart, 
  Zap, 
  Star, 
  DollarSign, 
  Shield,
  Menu,
  X,
  Map,
  Users,
  MessageSquare,
  Settings
} from 'lucide-react';
import { Card } from '../../ui/card';
import TraitActionPanel from '../../traits/TraitActionPanel';
import TraitEffectsDisplay from '../../traits/TraitEffectsDisplay';
import { useTraitAbilities } from '../../../hooks/useTraitAbilities';

const GameHUD = ({ player }) => {
  const [showMenu, setShowMenu] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [showTraitPanel, setShowTraitPanel] = useState(true);
  const [showEffectsPanel, setShowEffectsPanel] = useState(true);

  // Trait abilities hook
  const { useAbility, isUsing } = useTraitAbilities(player);

  // Calculate percentages for progress bars
  const healthPercent = ((player?.stats?.health || 100) / (player?.stats?.max_health || 100)) * 100;
  const energyPercent = ((player?.stats?.energy || 100) / (player?.stats?.max_energy || 100)) * 100;

  const handleUseAbility = async (abilityData) => {
    try {
      await useAbility(abilityData);
    } catch (error) {
      console.error('Failed to use ability:', error);
    }
  };

  return (
    <>
      {/* Top Left - Player Stats */}
      <div className="absolute top-4 left-4 space-y-2">
        {/* Player Info Card */}
        <Card className="bg-black/70 backdrop-blur-sm border-purple-500/30 p-3 min-w-[250px]">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-white font-bold text-lg">{player?.username || 'Player'}</h3>
            <span className="text-purple-400 text-sm">Lvl {player?.level || 1}</span>
          </div>
          
          {/* Health Bar */}
          <div className="mb-2">
            <div className="flex items-center justify-between text-xs text-gray-300 mb-1">
              <div className="flex items-center gap-1">
                <Heart className="w-3 h-3 text-red-500" />
                <span>Health</span>
              </div>
              <span>{player?.stats?.health || 100}/{player?.stats?.max_health || 100}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${healthPercent}%` }}
              />
            </div>
          </div>

          {/* Energy Bar */}
          <div className="mb-2">
            <div className="flex items-center justify-between text-xs text-gray-300 mb-1">
              <div className="flex items-center gap-1">
                <Zap className="w-3 h-3 text-yellow-500" />
                <span>Energy</span>
              </div>
              <span>{player?.stats?.energy || 100}/{player?.stats?.max_energy || 100}</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div 
                className="bg-yellow-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${energyPercent}%` }}
              />
            </div>
          </div>

          {/* Karma Points */}
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-1 text-orange-400">
              <Star className="w-4 h-4" />
              <span>Karma</span>
            </div>
            <span className="text-white font-semibold">{player?.karma_points || 0}</span>
          </div>
        </Card>

        {/* XP Progress */}
        <Card className="bg-black/70 backdrop-blur-sm border-purple-500/30 p-2">
          <div className="flex items-center justify-between text-xs text-gray-300 mb-1">
            <span>XP Progress</span>
            <span>{player?.xp || 0} / {(player?.level || 1) * 1000}</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-1.5">
            <div 
              className="bg-purple-500 h-1.5 rounded-full transition-all duration-300"
              style={{ width: `${((player?.xp || 0) / ((player?.level || 1) * 1000)) * 100}%` }}
            />
          </div>
        </Card>
      </div>

      {/* Top Right - Currencies & Quick Stats */}
      <div className="absolute top-4 right-4 space-y-2">
        <Card className="bg-black/70 backdrop-blur-sm border-purple-500/30 p-3 min-w-[200px]">
          <div className="space-y-2">
            {/* Credits */}
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-1 text-blue-400">
                <DollarSign className="w-4 h-4" />
                <span>Credits</span>
              </div>
              <span className="text-white font-semibold">
                {player?.currencies?.credits?.toLocaleString() || 0}
              </span>
            </div>

            {/* Karma Tokens */}
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-1 text-green-400">
                <Star className="w-4 h-4" />
                <span>Tokens</span>
              </div>
              <span className="text-white font-semibold">
                {player?.currencies?.karma_tokens?.toLocaleString() || 0}
              </span>
            </div>

            {/* Dark Matter */}
            <div className="flex items-center justify-between text-sm">
              <div className="flex items-center gap-1 text-purple-400">
                <Shield className="w-4 h-4" />
                <span>Dark Matter</span>
              </div>
              <span className="text-white font-semibold">
                {player?.currencies?.dark_matter?.toLocaleString() || 0}
              </span>
            </div>
          </div>
        </Card>

        {/* Class Badges */}
        <Card className="bg-black/70 backdrop-blur-sm border-purple-500/30 p-2">
          <div className="flex gap-2">
            <span className="px-2 py-1 bg-purple-500/30 text-purple-300 text-xs rounded">
              {player?.moral_class || 'Neutral'}
            </span>
            <span className="px-2 py-1 bg-blue-500/30 text-blue-300 text-xs rounded">
              {player?.economic_class || 'Middle'}
            </span>
          </div>
        </Card>
      </div>

      {/* Bottom Right - Action Buttons */}
      <div className="absolute bottom-4 right-4 flex flex-col gap-2">
        <button
          onClick={() => setShowMenu(!showMenu)}
          className="w-12 h-12 bg-purple-600 hover:bg-purple-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
          title="Menu"
        >
          {showMenu ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
        </button>

        <button
          onClick={() => setShowChat(!showChat)}
          className="w-12 h-12 bg-blue-600 hover:bg-blue-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
          title="Chat"
        >
          <MessageSquare className="w-6 h-6" />
        </button>

        <button
          className="w-12 h-12 bg-green-600 hover:bg-green-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
          title="Map"
        >
          <Map className="w-6 h-6" />
        </button>

        <button
          className="w-12 h-12 bg-orange-600 hover:bg-orange-700 text-white rounded-full flex items-center justify-center shadow-lg transition-colors"
          title="Players"
        >
          <Users className="w-6 h-6" />
        </button>
      </div>

      {/* Quick Menu Overlay */}
      {showMenu && (
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <Card className="bg-black/90 backdrop-blur-sm border-purple-500/30 p-6 min-w-[400px]">
            <h2 className="text-2xl font-bold text-white mb-4">Game Menu</h2>
            <div className="space-y-2">
              <button className="w-full bg-purple-600 hover:bg-purple-700 text-white px-4 py-3 rounded-lg transition-colors text-left">
                Continue Game
              </button>
              <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors text-left">
                Inventory
              </button>
              <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors text-left">
                Skills & Abilities
              </button>
              <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors text-left">
                Quests
              </button>
              <button className="w-full bg-gray-700 hover:bg-gray-600 text-white px-4 py-3 rounded-lg transition-colors text-left flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Settings
              </button>
              <button 
                onClick={() => window.location.href = '/dashboard'}
                className="w-full bg-red-600 hover:bg-red-700 text-white px-4 py-3 rounded-lg transition-colors text-left"
              >
                Exit to Dashboard
              </button>
            </div>
          </Card>
        </div>
      )}

      {/* Chat Overlay */}
      {showChat && (
        <div className="absolute bottom-20 right-4">
          <Card className="bg-black/90 backdrop-blur-sm border-purple-500/30 p-4 w-[350px]">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-white font-bold">Chat</h3>
              <button onClick={() => setShowChat(false)} className="text-gray-400 hover:text-white">
                <X className="w-4 h-4" />
              </button>
            </div>
            <div className="bg-black/50 rounded p-2 h-[200px] overflow-y-auto mb-2">
              <p className="text-gray-400 text-sm">Chat messages will appear here...</p>
            </div>
            <input
              type="text"
              placeholder="Type a message..."
              className="w-full bg-gray-800 text-white px-3 py-2 rounded border border-gray-700 focus:border-purple-500 focus:outline-none text-sm"
            />
          </Card>
        </div>
      )}

      {/* Minimap */}
      <div className="absolute bottom-4 left-4">
        <Card className="bg-black/70 backdrop-blur-sm border-purple-500/30 p-2">
          <div className="w-[150px] h-[150px] bg-gray-900 rounded relative">
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" />
            </div>
            <div className="absolute top-1 left-1 text-white text-xs">Map</div>
          </div>
        </Card>
      </div>

      {/* Center Crosshair */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div className="w-4 h-4 border-2 border-white rounded-full opacity-50" />
      </div>

      {/* Trait Action Panel - Right Side */}
      {showTraitPanel && player && (
        <TraitActionPanel player={player} onUseAbility={handleUseAbility} />
      )}

      {/* Trait Effects Display - Left Side */}
      {showEffectsPanel && player && (
        <TraitEffectsDisplay player={player} />
      )}
    </>
  );
};

export default GameHUD;
