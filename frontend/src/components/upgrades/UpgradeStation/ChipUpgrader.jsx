import React, { useState } from 'react';
import { Cpu, TrendingUp, Lock, CheckCircle, AlertCircle, Zap, BrainCircuit } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { upgradeService } from '@/services/upgradeService';
import { toast } from 'react-hot-toast';

/**
 * ChipUpgrader - Upgrade cyber chips and neural augmentations
 */
const ChipUpgrader = ({ player, currencies, onUpgrade }) => {
  const [upgrading, setUpgrading] = useState(null);

  const chips = [
    { 
      id: 'neural_enhancer', 
      name: 'Neural Enhancer', 
      icon: '🧠', 
      description: 'Boosts mental processing speed', 
      effect: '+5% XP gain per level',
      unlockLevel: 5 
    },
    { 
      id: 'combat_chip', 
      name: 'Combat Chip', 
      icon: '⚔️', 
      description: 'Enhances combat reflexes and damage', 
      effect: '+3% damage per level',
      unlockLevel: 10 
    },
    { 
      id: 'stealth_module', 
      name: 'Stealth Module', 
      icon: '👁️', 
      description: 'Improves stealth and evasion capabilities', 
      effect: '+4% evasion per level',
      unlockLevel: 15 
    },
    { 
      id: 'hacking_chip', 
      name: 'Hacking Chip', 
      icon: '💻', 
      description: 'Advanced hacking protocols', 
      effect: '+6% hack success rate per level',
      unlockLevel: 20 
    },
    { 
      id: 'resource_optimizer', 
      name: 'Resource Optimizer', 
      icon: '💰', 
      description: 'Optimizes resource gathering', 
      effect: '+2% credits gain per level',
      unlockLevel: 25 
    },
    { 
      id: 'quantum_processor', 
      name: 'Quantum Processor', 
      icon: '⚛️', 
      description: 'Ultimate computational power', 
      effect: '+10% all stats per level',
      unlockLevel: 40 
    }
  ];

  const getChipLevel = (chipId) => {
    return player?.chips?.[chipId]?.level || 0;
  };

  const isChipUnlocked = (chipId, unlockLevel) => {
    const hasChip = player?.chips?.[chipId];
    return hasChip || (player?.level || 1) >= unlockLevel;
  };

  const handleUpgrade = async (chipId) => {
    setUpgrading(chipId);
    try {
      const result = await upgradeService.upgradeChip(chipId);
      toast.success(`${result.chip_name} upgraded to level ${result.new_level}!`, {
        icon: '⚡',
      });
      onUpgrade();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upgrade chip');
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
          <BrainCircuit className="w-6 h-6 text-cyan-400" />
          Chip Upgrades
        </h2>
        <p className="text-gray-400">Enhance your neural implants and cyber augmentations</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {chips.map((chip) => {
          const level = getChipLevel(chip.id);
          const unlocked = isChipUnlocked(chip.id, chip.unlockLevel);
          const isMaxLevel = level >= 100;
          const cost = upgradeService.calculateUpgradeCost(level || 1, 'chip');
          const canAfford = canAffordUpgrade(cost);

          return (
            <Card key={chip.id} className={`upgrade-card p-4 ${!unlocked ? 'opacity-60' : ''}`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{chip.icon}</div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{chip.name}</h3>
                    <p className="text-sm text-gray-400">{chip.description}</p>
                    <div className="flex items-center gap-1 mt-1">
                      <Zap className="w-3 h-3 text-cyan-400" />
                      <span className="text-xs text-cyan-400 font-semibold">{chip.effect}</span>
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
                    Lv {chip.unlockLevel}
                  </div>
                )}
              </div>

              {!unlocked ? (
                <div className="unlock-requirement">
                  <Lock className="w-5 h-5" />
                  <div>
                    <p className="font-semibold">Locked</p>
                    <p className="text-sm">Reach player level {chip.unlockLevel} to unlock</p>
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
                        onClick={() => handleUpgrade(chip.id)}
                        disabled={!canAfford || upgrading === chip.id}
                        className="w-full upgrade-button"
                      >
                        {upgrading === chip.id ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                            Upgrading...
                          </>
                        ) : level === 0 ? (
                          <>
                            <Cpu className="w-4 h-4 mr-2" />
                            Install {chip.name}
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

export default ChipUpgrader;