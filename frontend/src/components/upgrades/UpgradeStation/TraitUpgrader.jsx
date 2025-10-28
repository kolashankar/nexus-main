import React, { useState } from 'react';
import { Zap, TrendingUp, Lock, CheckCircle, AlertCircle } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { upgradeService } from '@/services/upgradeService';
import { toast } from 'react-hot-toast';

/**
 * TraitUpgrader - Upgrade player traits (strength, hacking, charisma, etc.)
 */
const TraitUpgrader = ({ player, currencies, onUpgrade }) => {
  const [upgrading, setUpgrading] = useState(null);

  const traits = [
    { id: 'strength', name: 'Strength', icon: '💪', description: 'Physical power and combat effectiveness', color: 'red' },
    { id: 'hacking', name: 'Hacking', icon: '💻', description: 'Digital infiltration and system manipulation', color: 'green' },
    { id: 'charisma', name: 'Charisma', icon: '🎭', description: 'Social influence and persuasion', color: 'purple' },
    { id: 'stealth', name: 'Stealth', icon: '🥷', description: 'Covert operations and evasion', color: 'blue' },
    { id: 'intelligence', name: 'Intelligence', icon: '🧠', description: 'Problem solving and strategy', color: 'cyan' },
    { id: 'luck', name: 'Luck', icon: '🍀', description: 'Random event outcomes and critical chances', color: 'yellow' }
  ];

  const getTraitLevel = (traitId) => {
    return player?.traits?.[traitId] || 1;
  };

  const handleUpgrade = async (traitId) => {
    setUpgrading(traitId);
    try {
      const result = await upgradeService.upgradeTrait(traitId);
      toast.success(`${traitId.charAt(0).toUpperCase() + traitId.slice(1)} upgraded to level ${result.new_level}!`);
      onUpgrade();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upgrade trait');
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
        <h2 className="text-2xl font-bold text-white mb-2">Trait Upgrades</h2>
        <p className="text-gray-400">Enhance your character's core abilities and attributes</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {traits.map((trait) => {
          const level = getTraitLevel(trait.id);
          const isMaxLevel = level >= 100;
          const cost = upgradeService.calculateUpgradeCost(level, 'trait');
          const canAfford = canAffordUpgrade(cost);

          return (
            <Card key={trait.id} className="upgrade-card p-4">
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{trait.icon}</div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{trait.name}</h3>
                    <p className="text-sm text-gray-400">{trait.description}</p>
                  </div>
                </div>
                <div className="upgrade-level-badge">
                  Lv {level}
                </div>
              </div>

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
                    onClick={() => handleUpgrade(trait.id)}
                    disabled={!canAfford || upgrading === trait.id}
                    className="w-full upgrade-button"
                  >
                    {upgrading === trait.id ? (
                      <>
                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                        Upgrading...
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
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default TraitUpgrader;