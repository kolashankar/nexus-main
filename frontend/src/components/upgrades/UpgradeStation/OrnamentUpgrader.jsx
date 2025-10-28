import React, { useState } from 'react';
import { Gem, TrendingUp, Lock, CheckCircle, AlertCircle, Zap, Sparkles } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { upgradeService } from '@/services/upgradeService';
import { toast } from 'react-hot-toast';

/**
 * OrnamentUpgrader - Upgrade decorative items and cosmetic enhancements
 */
const OrnamentUpgrader = ({ player, currencies, onUpgrade }) => {
  const [upgrading, setUpgrading] = useState(null);

  const ornaments = [
    { id: 'avatar_frame', name: 'Avatar Frame', icon: '🖼️', description: 'Decorative border for your profile picture', bonus: 'Prestige +10', unlockLevel: 5 },
    { id: 'title_banner', name: 'Title Banner', icon: '📜', description: 'Custom title display banner', bonus: 'Reputation +5', unlockLevel: 10 },
    { id: 'emote_pack', name: 'Emote Pack', icon: '😎', description: 'Exclusive emote animations', bonus: 'Social +15', unlockLevel: 15 },
    { id: 'victory_effect', name: 'Victory Effect', icon: '✨', description: 'Special effects for victories', bonus: 'Morale +20', unlockLevel: 20 },
    { id: 'nameplate', name: 'Custom Nameplate', icon: '💠', description: 'Personalized name display', bonus: 'Recognition +12', unlockLevel: 25 },
    { id: 'aura', name: 'Character Aura', icon: '🌟', description: 'Glowing aura effect around character', bonus: 'Intimidation +25', unlockLevel: 30 }
  ];

  const getOrnamentLevel = (ornamentId) => {
    return player?.ornaments?.[ornamentId]?.level || 0;
  };

  const isOrnamentUnlocked = (ornamentId, unlockLevel) => {
    const hasOrnament = player?.ornaments?.[ornamentId];
    return hasOrnament || (player?.level || 1) >= unlockLevel;
  };

  const handleUpgrade = async (ornamentId) => {
    setUpgrading(ornamentId);
    try {
      const result = await upgradeService.upgradeOrnament(ornamentId);
      toast.success(`${result.ornament_name} upgraded to level ${result.new_level}!`, {
        icon: '✨',
      });
      onUpgrade();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upgrade ornament');
    } finally {
      setUpgrading(null);
    }
  };

  const canAffordUpgrade = (cost) => {
    return currencies?.credits >= cost.credits &&
           currencies?.karma_tokens >= cost.karma_tokens &&
           currencies?.dark_matter >= cost.dark_matter;
  };

  return (
    <div className="space-y-4">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-white mb-2 flex items-center gap-2">
          <Sparkles className="w-6 h-6 text-purple-400" />
          Ornament Upgrades
        </h2>
        <p className="text-gray-400">Enhance your cosmetic items and show off your style</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {ornaments.map((ornament) => {
          const level = getOrnamentLevel(ornament.id);
          const unlocked = isOrnamentUnlocked(ornament.id, ornament.unlockLevel);
          const isMaxLevel = level >= 100;
          const cost = upgradeService.calculateUpgradeCost(level || 1, 'ornament');
          const canAfford = canAffordUpgrade(cost);

          return (
            <Card key={ornament.id} className={`upgrade-card p-4 ${!unlocked ? 'opacity-60' : ''}`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{ornament.icon}</div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{ornament.name}</h3>
                    <p className="text-sm text-gray-400">{ornament.description}</p>
                    <div className="flex items-center gap-1 mt-1">
                      <Sparkles className="w-3 h-3 text-yellow-400" />
                      <span className="text-xs text-yellow-400 font-semibold">{ornament.bonus}</span>
                    </div>
                  </div>
                </div>
                {unlocked ? (
                  <div className="upgrade-level-badge">
                    Lv {level}
                  </div>
                ) : (
                  <div className="flex items-center gap-1 text-xs text-red-400 bg-red-900/20 px-2 py-1 rounded">
                    <Lock className="w-3 h-3" />
                    Lv {ornament.unlockLevel}
                  </div>
                )}
              </div>

              {!unlocked ? (
                <div className="unlock-requirement">
                  <Lock className="w-5 h-5" />
                  <div>
                    <p className="font-semibold">Locked</p>
                    <p className="text-sm">Reach player level {ornament.unlockLevel} to unlock</p>
                  </div>
                </div>
              ) : (
                <>
                  {/* Progress Bar */}
                  <div className="mb-4">
                    <div className="flex justify-between text-xs text-gray-400 mb-2">
                      <span>Progress to Max</span>
                      <span>{level}/100</span>
                    </div>
                    <div className="upgrade-progress">
                      <div 
                        className="upgrade-progress-bar"
                        style={{ width: `${(level / 100) * 100}%` }}
                      />
                    </div>
                  </div>

                  {/* Upgrade Cost or Max Level */}
                  {isMaxLevel ? (
                    <div className="max-level-badge w-full justify-center">
                      <CheckCircle className="w-5 h-5" />
                      <span>MAX LEVEL</span>
                    </div>
                  ) : (
                    <>
                      <div className="space-y-2 mb-4">
                        <div className={`upgrade-cost ${!canAfford ? 'insufficient' : ''}`}>
                          <span className="text-yellow-400">💰</span>
                          <span className="text-white font-semibold">{cost.credits.toLocaleString()}</span>
                          <span className="text-gray-400">Credits</span>
                        </div>
                        <div className={`upgrade-cost ${!canAfford ? 'insufficient' : ''}`}>
                          <Zap className="w-4 h-4 text-purple-400" />
                          <span className="text-white font-semibold">{cost.karma_tokens.toLocaleString()}</span>
                          <span className="text-gray-400">Karma Tokens</span>
                        </div>
                        <div className={`upgrade-cost ${!canAfford ? 'insufficient' : ''}`}>
                          <span className="text-blue-400">💎</span>
                          <span className="text-white font-semibold">{cost.dark_matter.toLocaleString()}</span>
                          <span className="text-gray-400">Dark Matter</span>
                        </div>
                      </div>

                      <Button
                        onClick={() => handleUpgrade(ornament.id)}
                        disabled={!canAfford || upgrading === ornament.id}
                        className="w-full upgrade-button"
                      >
                        {upgrading === ornament.id ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                            Upgrading...
                          </>
                        ) : level === 0 ? (
                          <>
                            <Gem className="w-4 h-4 mr-2" />
                            Unlock {ornament.name}
                          </>
                        ) : (
                          <>
                            <TrendingUp className="w-4 h-4 mr-2" />
                            Upgrade to Level {level + 1}
                          </>
                        )}
                      </Button>

                      {!canAfford && (
                        <div className="flex items-center gap-2 mt-2 text-sm text-red-400">
                          <AlertCircle className="w-4 h-4" />
                          <span>Insufficient resources</span>
                        </div>
                      )}
                    </>
                  )}
                </>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default OrnamentUpgrader;