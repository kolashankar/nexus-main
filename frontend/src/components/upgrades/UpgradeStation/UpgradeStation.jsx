import React, { useState, useEffect } from 'react';
import { Zap, Bot, Gem, Cpu, TrendingUp, Coins } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import TraitUpgrader from './TraitUpgrader';
import RobotUpgrader from './RobotUpgrader';
import OrnamentUpgrader from './OrnamentUpgrader';
import ChipUpgrader from './ChipUpgrader';
import { useUpgrades } from '@/hooks/useUpgrades';
import './UpgradeStation.css';

/**
 * UpgradeStation - Main upgrade hub component
 * Allows players to upgrade traits, robots, ornaments, and chips
 */
const UpgradeStation = () => {
  const [activeTab, setActiveTab] = useState('traits');
  const { player, currencies, loading, refreshPlayer } = useUpgrades();

  useEffect(() => {
    refreshPlayer();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="upgrade-loading">
          <Zap className="w-16 h-16 text-purple-400 animate-pulse" />
          <p className="text-white mt-4">Loading Upgrade Station...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="upgrade-station">
      {/* Header */}
      <div className="upgrade-station-header">
        <div className="flex items-center gap-3">
          <div className="upgrade-icon-wrapper">
            <TrendingUp className="w-8 h-8 text-purple-400" />
          </div>
          <div>
            <h1 className="text-4xl font-bold text-white upgrade-title">Upgrade Station</h1>
            <p className="text-gray-300 mt-1">Enhance your abilities and equipment</p>
          </div>
        </div>

        {/* Currency Display */}
        <Card className="bg-gray-900/50 border-purple-500/30 p-4">
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center">
              <Coins className="w-5 h-5 text-yellow-400 mx-auto mb-1" />
              <p className="text-xs text-gray-400">Credits</p>
              <p className="text-lg font-bold text-white">{currencies?.credits?.toLocaleString() || 0}</p>
            </div>
            <div className="text-center">
              <Zap className="w-5 h-5 text-purple-400 mx-auto mb-1" />
              <p className="text-xs text-gray-400">Karma Tokens</p>
              <p className="text-lg font-bold text-white">{currencies?.karma_tokens?.toLocaleString() || 0}</p>
            </div>
            <div className="text-center">
              <Gem className="w-5 h-5 text-blue-400 mx-auto mb-1" />
              <p className="text-xs text-gray-400">Dark Matter</p>
              <p className="text-lg font-bold text-white">{currencies?.dark_matter?.toLocaleString() || 0}</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Upgrade Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="mt-8">
        <TabsList className="grid w-full grid-cols-4 bg-gray-900/50">
          <TabsTrigger value="traits" className="flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Traits
          </TabsTrigger>
          <TabsTrigger value="robots" className="flex items-center gap-2">
            <Bot className="w-4 h-4" />
            Robots
          </TabsTrigger>
          <TabsTrigger value="ornaments" className="flex items-center gap-2">
            <Gem className="w-4 h-4" />
            Ornaments
          </TabsTrigger>
          <TabsTrigger value="chips" className="flex items-center gap-2">
            <Cpu className="w-4 h-4" />
            Chips
          </TabsTrigger>
        </TabsList>

        <TabsContent value="traits" className="mt-6">
          <TraitUpgrader player={player} currencies={currencies} onUpgrade={refreshPlayer} />
        </TabsContent>

        <TabsContent value="robots" className="mt-6">
          <RobotUpgrader player={player} currencies={currencies} onUpgrade={refreshPlayer} />
        </TabsContent>

        <TabsContent value="ornaments" className="mt-6">
          <OrnamentUpgrader player={player} currencies={currencies} onUpgrade={refreshPlayer} />
        </TabsContent>

        <TabsContent value="chips" className="mt-6">
          <ChipUpgrader player={player} currencies={currencies} onUpgrade={refreshPlayer} />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default UpgradeStation;