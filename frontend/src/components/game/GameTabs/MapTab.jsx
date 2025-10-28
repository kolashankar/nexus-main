import React from 'react';
import { Map, MapPin, Flag, Users, Home } from 'lucide-react';
import { Card } from '@/components/ui/card';

/**
 * MapTab - World map and territory control display
 */
const MapTab = ({ player }) => {
  // Sample territories data
  const territories = [
    { id: 1, name: 'Central District', controlled_by: 'The Virtuous', players: 45, income: 1000 },
    { id: 2, name: 'Tech Quarter', controlled_by: 'Hackers Guild', players: 32, income: 800 },
    { id: 3, name: 'Trade Hub', controlled_by: 'Merchants Alliance', players: 28, income: 1200 },
    { id: 4, name: 'Combat Arena', controlled_by: 'Warriors Faction', players: 51, income: 600 },
    { id: 5, name: 'Neutral Zone', controlled_by: null, players: 15, income: 0 },
  ];

  const playerGuild = player?.guild_id;
  const playerTerritory = territories.find(t => t.controlled_by === player?.guild_name);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Map className="w-5 h-5 text-blue-400" />
        <h3 className="text-xl font-bold text-white">World Map</h3>
      </div>

      {/* Mini Map Visual */}
      <Card className="bg-gray-900/50 p-4">
        <div className="relative w-full h-64 bg-gray-800 rounded-lg overflow-hidden">
          {/* Grid Background */}
          <div className="absolute inset-0" style={{
            backgroundImage: 'linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)',
            backgroundSize: '20px 20px'
          }} />
          
          {/* Territory Markers */}
          {territories.map((territory, index) => (
            <div
              key={territory.id}
              className="absolute w-12 h-12 flex items-center justify-center"
              style={{
                top: `${20 + index * 15}%`,
                left: `${10 + (index % 3) * 30}%`
              }}
            >
              <div className={`w-10 h-10 rounded-full flex items-center justify-center ${
                territory.controlled_by ? 'bg-purple-600' : 'bg-gray-600'
              } border-2 border-white shadow-lg cursor-pointer hover:scale-110 transition-transform`}>
                {territory.controlled_by ? <Flag className="w-5 h-5" /> : <MapPin className="w-5 h-5" />}
              </div>
            </div>
          ))}

          {/* Player Position */}
          <div className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2">
            <div className="w-4 h-4 bg-green-500 rounded-full animate-pulse" />
            <span className="absolute top-6 left-1/2 transform -translate-x-1/2 text-xs text-white whitespace-nowrap">
              You
            </span>
          </div>
        </div>
      </Card>

      {/* Territory List */}
      <div className="space-y-2">
        <h4 className="text-lg font-semibold text-white mb-3">Territories</h4>
        {territories.map((territory) => (
          <Card key={territory.id} className="bg-gray-900/50 p-3 hover:bg-gray-800/50 transition-colors cursor-pointer">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Flag className={`w-5 h-5 ${
                  territory.controlled_by ? 'text-purple-400' : 'text-gray-500'
                }`} />
                <div>
                  <h5 className="font-semibold text-white">{territory.name}</h5>
                  <p className="text-sm text-gray-400">
                    {territory.controlled_by ? `Controlled by ${territory.controlled_by}` : 'Unclaimed'}
                  </p>
                </div>
              </div>
              <div className="text-right">
                <div className="flex items-center gap-1 text-sm text-gray-300">
                  <Users className="w-4 h-4" />
                  <span>{territory.players}</span>
                </div>
                <p className="text-xs text-green-400">+{territory.income}/day</p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Player Territory Info */}
      {playerTerritory && (
        <Card className="bg-purple-900/30 border-purple-500/50 p-4">
          <div className="flex items-center gap-2 mb-2">
            <Home className="w-5 h-5 text-purple-400" />
            <h4 className="font-semibold text-white">Your Territory</h4>
          </div>
          <p className="text-gray-300">
            Your guild controls <strong className="text-purple-400">{playerTerritory.name}</strong>
          </p>
          <p className="text-sm text-gray-400 mt-1">
            Daily income: <span className="text-green-400">+{playerTerritory.income} credits</span>
          </p>
        </Card>
      )}
    </div>
  );
};

export default MapTab;
