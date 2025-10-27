/**
 * Play/Game page - Full 3D game environment
 */
import React, { useEffect, useState } from 'react';
import GameWorld from '../../components/game/GameWorld/GameWorld';
import GameHUD from '../../components/game/GameHUD/GameHUD';
import TaskPanel from '../../components/game/TaskPanel/TaskPanel';
import Marketplace from '../../components/game/Marketplace/Marketplace';
import useStore from '../../store';
import { Loader2 } from 'lucide-react';

const Play = () => {
  const { player, fetchPlayer, isLoadingPlayer } = useStore();
  const [gameReady, setGameReady] = useState(false);
  const [showMarketplace, setShowMarketplace] = useState(false);

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
      <GameWorld player={player} />
      
      {/* Game HUD Overlay */}
      <GameHUD player={player} />
      
      {/* Game Instructions (can be toggled) */}
      <div className="absolute bottom-4 left-4 bg-black/70 text-white px-4 py-2 rounded-lg text-sm">
        <p className="font-semibold mb-1">Controls:</p>
        <p>WASD - Move | Mouse - Look | Space - Jump | E - Interact</p>
      </div>
    </div>
  );
};

export default Play;
