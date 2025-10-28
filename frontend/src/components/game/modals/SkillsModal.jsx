import React from 'react';
import { Card } from '../ui/card';
import { X, Zap, Shield, Target, Heart, Sword, Brain } from 'lucide-react';

/**
 * Skills & Abilities Modal Component
 */
const SkillsModal = ({ onClose, player }) => {
  const skills = [
    { 
      id: 1, 
      name: 'Combat Mastery', 
      icon: Sword, 
      level: 5, 
      maxLevel: 10,
      description: 'Increases damage dealt in combat',
      type: 'combat'
    },
    { 
      id: 2, 
      name: 'Energy Shield', 
      icon: Shield, 
      level: 3, 
      maxLevel: 10,
      description: 'Temporary shield that absorbs damage',
      type: 'defense'
    },
    { 
      id: 3, 
      name: 'Precision Strike', 
      icon: Target, 
      level: 4, 
      maxLevel: 10,
      description: 'Critical hit chance increased',
      type: 'combat'
    },
    { 
      id: 4, 
      name: 'Rapid Healing', 
      icon: Heart, 
      level: 2, 
      maxLevel: 10,
      description: 'Faster health regeneration',
      type: 'support'
    },
    { 
      id: 5, 
      name: 'Energy Efficiency', 
      icon: Zap, 
      level: 6, 
      maxLevel: 10,
      description: 'Reduced energy cost for abilities',
      type: 'utility'
    },
    { 
      id: 6, 
      name: 'Tactical Mind', 
      icon: Brain, 
      level: 3, 
      maxLevel: 10,
      description: 'Increased XP gain from quests',
      type: 'utility'
    },
  ];

  const typeColors = {
    combat: 'border-red-500 bg-red-500/10',
    defense: 'border-blue-500 bg-blue-500/10',
    support: 'border-green-500 bg-green-500/10',
    utility: 'border-purple-500 bg-purple-500/10',
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="bg-gray-900 border-purple-500/30 p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white flex items-center gap-2">
            <Zap className="w-8 h-8 text-yellow-500" />
            Skills & Abilities
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Available Skill Points */}
        <div className="mb-6 p-4 bg-purple-900/30 rounded-lg border border-purple-500/50">
          <div className="flex items-center justify-between">
            <span className="text-white font-semibold">Available Skill Points:</span>
            <span className="text-3xl font-bold text-purple-400">{player?.skill_points || 0}</span>
          </div>
        </div>

        {/* Skills Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {skills.map((skill) => {
            const Icon = skill.icon;
            const progressPercent = (skill.level / skill.maxLevel) * 100;
            
            return (
              <div
                key={skill.id}
                className={`p-4 rounded-lg border-2 ${typeColors[skill.type]} hover:scale-[1.02] transition-transform`}
              >
                <div className="flex items-start gap-4">
                  <div className="p-3 bg-black/30 rounded-lg">
                    <Icon className="w-8 h-8 text-white" />
                  </div>
                  <div className="flex-1">
                    <div className="flex items-start justify-between mb-2">
                      <div>
                        <h3 className="text-white font-semibold">{skill.name}</h3>
                        <p className="text-gray-400 text-xs capitalize">{skill.type}</p>
                      </div>
                      <span className="text-purple-400 text-sm font-semibold">
                        Lv {skill.level}/{skill.maxLevel}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm mb-3">{skill.description}</p>
                    
                    {/* Progress Bar */}
                    <div className="w-full bg-gray-700 rounded-full h-2 mb-2">
                      <div
                        className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progressPercent}%` }}
                      />
                    </div>
                    
                    {/* Upgrade Button */}
                    <button
                      className={`w-full mt-2 py-2 rounded text-sm font-semibold transition-colors ${
                        skill.level < skill.maxLevel && (player?.skill_points || 0) > 0
                          ? 'bg-purple-600 hover:bg-purple-700 text-white'
                          : 'bg-gray-700 text-gray-400 cursor-not-allowed'
                      }`}
                      disabled={skill.level >= skill.maxLevel || (player?.skill_points || 0) === 0}
                    >
                      {skill.level >= skill.maxLevel ? 'Max Level' : 'Upgrade (1 SP)'}
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
};

export default SkillsModal;
