import React, { useState } from 'react';
import { Trophy, Star, Target, Lock, CheckCircle, Award, Crown } from 'lucide-react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

/**
 * AchievementsTab - Player achievements and progression milestones
 */
const AchievementsTab = ({ player }) => {
  const [filter, setFilter] = useState('all');

  // Sample achievements data
  const achievements = [
    {
      id: 1,
      name: 'First Steps',
      description: 'Complete your first task',
      category: 'progression',
      unlocked: true,
      progress: 1,
      required: 1,
      reward: '100 XP',
      rarity: 'common',
      icon: Target
    },
    {
      id: 2,
      name: 'Virtuous Path',
      description: 'Reach 500 positive karma',
      category: 'karma',
      unlocked: true,
      progress: 1250,
      required: 500,
      reward: '500 XP + Virtue Badge',
      rarity: 'rare',
      icon: Star
    },
    {
      id: 3,
      name: 'Wealthy Trader',
      description: 'Accumulate 10,000 credits',
      category: 'economy',
      unlocked: player?.currencies?.credits >= 10000,
      progress: player?.currencies?.credits || 0,
      required: 10000,
      reward: '1,000 XP',
      rarity: 'uncommon',
      icon: Trophy
    },
    {
      id: 4,
      name: 'Master Hacker',
      description: 'Reach 100% in Hacking trait',
      category: 'traits',
      unlocked: false,
      progress: player?.traits?.hacking || 50,
      required: 100,
      reward: 'Legendary Hacking Power',
      rarity: 'legendary',
      icon: Award
    },
    {
      id: 5,
      name: 'Guild Leader',
      description: 'Form or lead a guild',
      category: 'social',
      unlocked: false,
      progress: 0,
      required: 1,
      reward: 'Leadership Title',
      rarity: 'epic',
      icon: Crown
    },
    {
      id: 6,
      name: 'Combat Expert',
      description: 'Win 50 PvP battles',
      category: 'combat',
      unlocked: false,
      progress: player?.stats?.pvp_wins || 0,
      required: 50,
      reward: '2,000 XP + Combat Badge',
      rarity: 'rare',
      icon: Trophy
    }
  ];

  const categories = ['all', 'progression', 'karma', 'economy', 'traits', 'social', 'combat'];

  const getRarityColor = (rarity) => {
    switch (rarity) {
      case 'common': return 'text-gray-400 border-gray-600';
      case 'uncommon': return 'text-green-400 border-green-600';
      case 'rare': return 'text-blue-400 border-blue-600';
      case 'epic': return 'text-purple-400 border-purple-600';
      case 'legendary': return 'text-yellow-400 border-yellow-600';
      default: return 'text-gray-400 border-gray-600';
    }
  };

  const filteredAchievements = filter === 'all' 
    ? achievements 
    : achievements.filter(a => a.category === filter);

  const unlockedCount = achievements.filter(a => a.unlocked).length;
  const totalCount = achievements.length;
  const completionPercent = Math.round((unlockedCount / totalCount) * 100);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 mb-4">
        <Trophy className="w-5 h-5 text-yellow-400" />
        <h3 className="text-xl font-bold text-white">Achievements</h3>
      </div>

      {/* Progress Summary */}
      <Card className="bg-gradient-to-r from-purple-900/50 to-blue-900/50 border-purple-500/50 p-4">
        <div className="flex items-center justify-between mb-3">
          <div>
            <h4 className="text-lg font-semibold text-white">Overall Progress</h4>
            <p className="text-sm text-gray-300">{unlockedCount} of {totalCount} achievements unlocked</p>
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-yellow-400">{completionPercent}%</div>
            <p className="text-xs text-gray-400">Complete</p>
          </div>
        </div>
        <div className="w-full bg-gray-700 rounded-full h-3">
          <div 
            className="bg-gradient-to-r from-purple-500 to-blue-500 h-3 rounded-full transition-all duration-500"
            style={{ width: `${completionPercent}%` }}
          />
        </div>
      </Card>

      {/* Category Filters */}
      <div className="flex gap-2 overflow-x-auto pb-2">
        {categories.map((cat) => (
          <Button
            key={cat}
            onClick={() => setFilter(cat)}
            variant={filter === cat ? 'default' : 'outline'}
            size="sm"
            className="whitespace-nowrap capitalize"
          >
            {cat}
          </Button>
        ))}
      </div>

      {/* Achievements Grid */}
      <div className="space-y-3">
        {filteredAchievements.map((achievement) => {
          const Icon = achievement.icon;
          const progressPercent = Math.min((achievement.progress / achievement.required) * 100, 100);
          
          return (
            <Card 
              key={achievement.id} 
              className={`p-4 transition-all ${
                achievement.unlocked 
                  ? 'bg-gray-900/50 border-green-500/30' 
                  : 'bg-gray-900/30 border-gray-700/30 opacity-75'
              } hover:scale-[1.02]`}
            >
              <div className="flex items-start gap-4">
                {/* Icon */}
                <div className={`w-16 h-16 rounded-lg flex items-center justify-center border-2 ${
                  achievement.unlocked 
                    ? 'bg-gradient-to-br from-yellow-600 to-orange-600 border-yellow-500' 
                    : 'bg-gray-800 border-gray-700'
                }`}>
                  {achievement.unlocked ? (
                    <CheckCircle className="w-8 h-8 text-white" />
                  ) : (
                    <Lock className="w-8 h-8 text-gray-500" />
                  )}
                </div>

                {/* Content */}
                <div className="flex-1">
                  <div className="flex items-start justify-between mb-2">
                    <div>
                      <h5 className="font-bold text-white text-lg">{achievement.name}</h5>
                      <p className="text-sm text-gray-400">{achievement.description}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-semibold capitalize ${
                      getRarityColor(achievement.rarity)
                    } border`}>
                      {achievement.rarity}
                    </span>
                  </div>

                  {/* Progress Bar */}
                  <div className="mb-2">
                    <div className="flex items-center justify-between text-xs text-gray-400 mb-1">
                      <span>Progress</span>
                      <span>{achievement.progress} / {achievement.required}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div 
                        className={`h-2 rounded-full transition-all duration-300 ${
                          achievement.unlocked 
                            ? 'bg-gradient-to-r from-green-500 to-emerald-500' 
                            : 'bg-gradient-to-r from-blue-500 to-purple-500'
                        }`}
                        style={{ width: `${progressPercent}%` }}
                      />
                    </div>
                  </div>

                  {/* Reward */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2 text-sm">
                      <Award className="w-4 h-4 text-yellow-400" />
                      <span className="text-gray-300">Reward: <span className="text-yellow-400">{achievement.reward}</span></span>
                    </div>
                    {achievement.unlocked && (
                      <span className="text-xs text-green-400 flex items-center gap-1">
                        <CheckCircle className="w-3 h-3" />
                        Unlocked
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {filteredAchievements.length === 0 && (
        <Card className="bg-gray-900/50 p-8 text-center">
          <Trophy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400 text-lg">No achievements in this category yet</p>
          <p className="text-sm text-gray-500 mt-2">Keep playing to unlock more achievements!</p>
        </Card>
      )}
    </div>
  );
};

export default AchievementsTab;
