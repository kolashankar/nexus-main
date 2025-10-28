import React, { useState } from 'react';
import { Bot, TrendingUp, Lock, CheckCircle, AlertCircle, Zap } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { upgradeService } from '@/services/upgradeService';
import { toast } from 'react-hot-toast';

/**
 * RobotUpgrader - Upgrade robot companions and their abilities
 */
const RobotUpgrader = ({ player, currencies, onUpgrade }) => {
  const [upgrading, setUpgrading] = useState(null);

  const robots = [
    { id: 'scout', name: 'Scout Bot', icon: '🤖', description: 'Reconnaissance and exploration specialist', unlockLevel: 1 },
    { id: 'combat', name: 'Combat Droid', icon: '⚔️', description: 'Battle companion with advanced weapons', unlockLevel: 10 },
    { id: 'hacker', name: 'Hacker Bot', icon: '💾', description: 'Digital warfare and system infiltration', unlockLevel: 15 },
    { id: 'medic', name: 'Medic Bot', icon: '🏥', description: 'Healing and support functions', unlockLevel: 20 },
    { id: 'trader', name: 'Trader Bot', icon: '💼', description: 'Automated trading and resource management', unlockLevel: 25 },
    { id: 'guardian', name: 'Guardian Mech', icon: '🛡️', description: 'Heavy defense and protection systems', unlockLevel: 35 }
  ];

  const getRobotLevel = (robotId) => {
    return player?.robots?.[robotId]?.level || 0;
  };

  const isRobotUnlocked = (robotId, unlockLevel) => {
    const hasRobot = player?.robots?.[robotId];
    return hasRobot || (player?.level || 1) >= unlockLevel;
  };

  const handleUpgrade = async (robotId) => {
    setUpgrading(robotId);
    try {
      const result = await upgradeService.upgradeRobot(robotId);
      toast.success(`${result.robot_name} upgraded to level ${result.new_level}!`);
      onUpgrade();
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Failed to upgrade robot');
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
        <h2 className="text-2xl font-bold text-white mb-2">Robot Upgrades</h2>
        <p className="text-gray-400">Enhance your robotic companions and unlock new abilities</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {robots.map((robot) => {
          const level = getRobotLevel(robot.id);
          const unlocked = isRobotUnlocked(robot.id, robot.unlockLevel);
          const isMaxLevel = level >= 100;
          const cost = upgradeService.calculateUpgradeCost(level || 1, 'robot');
          const canAfford = canAffordUpgrade(cost);

          return (
            <Card key={robot.id} className={`upgrade-card p-4 ${!unlocked ? 'opacity-60' : ''}`}>
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-3">
                  <div className="text-4xl">{robot.icon}</div>
                  <div>
                    <h3 className="text-lg font-bold text-white">{robot.name}</h3>
                    <p className="text-sm text-gray-400">{robot.description}</p>
                  </div>
                </div>
                {unlocked ? (
                  <div className="upgrade-level-badge">
                    Lv {level}
                  </div>
                ) : (
                  <div className="flex items-center gap-1 text-xs text-red-400 bg-red-900/20 px-2 py-1 rounded">
                    <Lock className="w-3 h-3" />
                    Lv {robot.unlockLevel}
                  </div>
                )}
              </div>

              {!unlocked ? (
                <div className="unlock-requirement">
                  <Lock className="w-5 h-5" />
                  <div>
                    <p className="font-semibold">Locked</p>
                    <p className="text-sm">Reach player level {robot.unlockLevel} to unlock</p>
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
                        onClick={() => handleUpgrade(robot.id)}
                        disabled={!canAfford || upgrading === robot.id}
                        className="w-full upgrade-button"
                      >
                        {upgrading === robot.id ? (
                          <>
                            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                            Upgrading...
                          </>
                        ) : level === 0 ? (
                          <>
                            <Bot className="w-4 h-4 mr-2" />
                            Unlock {robot.name}
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

export default RobotUpgrader;