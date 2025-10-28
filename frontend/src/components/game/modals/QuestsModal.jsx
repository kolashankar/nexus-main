import React from 'react';
import { Card } from '../ui/card';
import { X, ScrollText, CheckCircle, Circle, Star, Trophy } from 'lucide-react';

/**
 * Quests Modal Component
 */
const QuestsModal = ({ onClose, player }) => {
  const quests = [
    {
      id: 1,
      title: 'Welcome to Karma Nexus',
      description: 'Complete your first mission and explore the city',
      status: 'active',
      progress: 75,
      rewards: { xp: 500, credits: 100 },
      objectives: [
        { id: 1, text: 'Visit the marketplace', completed: true },
        { id: 2, text: 'Talk to the trader NPC', completed: true },
        { id: 3, text: 'Complete a combat encounter', completed: true },
        { id: 4, text: 'Return to headquarters', completed: false },
      ]
    },
    {
      id: 2,
      title: 'Robot Uprising',
      description: 'Investigate the mysterious robot activity in the eastern district',
      status: 'active',
      progress: 30,
      rewards: { xp: 1000, credits: 250, karma: 50 },
      objectives: [
        { id: 1, text: 'Scout the eastern district', completed: true },
        { id: 2, text: 'Collect evidence (0/5)', completed: false },
        { id: 3, text: 'Report to commander', completed: false },
      ]
    },
    {
      id: 3,
      title: 'Karma Challenge',
      description: 'Make choices that affect your karma standing',
      status: 'available',
      progress: 0,
      rewards: { xp: 750, karma: 100 },
      objectives: [
        { id: 1, text: 'Make 5 moral choices', completed: false },
        { id: 2, text: 'Interact with NPCs', completed: false },
      ]
    },
    {
      id: 4,
      title: 'Master of Combat',
      description: 'Defeat 10 enemies in combat encounters',
      status: 'completed',
      progress: 100,
      rewards: { xp: 2000, credits: 500 },
      objectives: [
        { id: 1, text: 'Defeat 10 enemies', completed: true },
        { id: 2, text: 'Return for reward', completed: true },
      ]
    },
  ];

  const getStatusColor = (status) => {
    switch (status) {
      case 'active':
        return 'text-yellow-400 border-yellow-500/30 bg-yellow-500/10';
      case 'completed':
        return 'text-green-400 border-green-500/30 bg-green-500/10';
      case 'available':
        return 'text-blue-400 border-blue-500/30 bg-blue-500/10';
      default:
        return 'text-gray-400 border-gray-500/30 bg-gray-500/10';
    }
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="bg-gray-900 border-purple-500/30 p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white flex items-center gap-2">
            <ScrollText className="w-8 h-8 text-purple-400" />
            Quests
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Quest Stats */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="p-4 bg-yellow-900/20 rounded-lg border border-yellow-500/30">
            <div className="text-yellow-400 text-2xl font-bold">
              {quests.filter(q => q.status === 'active').length}
            </div>
            <div className="text-gray-300 text-sm">Active</div>
          </div>
          <div className="p-4 bg-green-900/20 rounded-lg border border-green-500/30">
            <div className="text-green-400 text-2xl font-bold">
              {quests.filter(q => q.status === 'completed').length}
            </div>
            <div className="text-gray-300 text-sm">Completed</div>
          </div>
          <div className="p-4 bg-blue-900/20 rounded-lg border border-blue-500/30">
            <div className="text-blue-400 text-2xl font-bold">
              {quests.filter(q => q.status === 'available').length}
            </div>
            <div className="text-gray-300 text-sm">Available</div>
          </div>
        </div>

        {/* Quests List */}
        <div className="space-y-4">
          {quests.map((quest) => (
            <div
              key={quest.id}
              className={`p-4 rounded-lg border-2 ${getStatusColor(quest.status)}`}
            >
              <div className="flex items-start justify-between mb-3">
                <div>
                  <h3 className="text-white font-semibold text-lg mb-1">{quest.title}</h3>
                  <p className="text-gray-300 text-sm">{quest.description}</p>
                </div>
                <span className="px-3 py-1 rounded-full text-xs font-semibold capitalize bg-black/30">
                  {quest.status}
                </span>
              </div>

              {/* Progress Bar */}
              {quest.status !== 'completed' && (
                <div className="mb-3">
                  <div className="flex justify-between text-xs text-gray-400 mb-1">
                    <span>Progress</span>
                    <span>{quest.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div
                      className="bg-purple-500 h-2 rounded-full transition-all duration-300"
                      style={{ width: `${quest.progress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Objectives */}
              <div className="mb-3">
                <h4 className="text-white text-sm font-semibold mb-2">Objectives:</h4>
                <div className="space-y-1">
                  {quest.objectives.map((obj) => (
                    <div key={obj.id} className="flex items-center gap-2 text-sm">
                      {obj.completed ? (
                        <CheckCircle className="w-4 h-4 text-green-400 flex-shrink-0" />
                      ) : (
                        <Circle className="w-4 h-4 text-gray-500 flex-shrink-0" />
                      )}
                      <span className={obj.completed ? 'text-gray-400 line-through' : 'text-gray-300'}>
                        {obj.text}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Rewards */}
              <div className="flex items-center gap-4 text-sm">
                <span className="text-gray-400">Rewards:</span>
                {quest.rewards.xp && (
                  <div className="flex items-center gap-1 text-purple-400">
                    <Star className="w-4 h-4" />
                    <span>{quest.rewards.xp} XP</span>
                  </div>
                )}
                {quest.rewards.credits && (
                  <div className="flex items-center gap-1 text-yellow-400">
                    <span>💰</span>
                    <span>{quest.rewards.credits}</span>
                  </div>
                )}
                {quest.rewards.karma && (
                  <div className="flex items-center gap-1 text-orange-400">
                    <span>⭐</span>
                    <span>{quest.rewards.karma} Karma</span>
                  </div>
                )}
              </div>

              {/* Action Button */}
              <button
                className={`w-full mt-3 py-2 rounded font-semibold transition-colors ${
                  quest.status === 'completed'
                    ? 'bg-green-600 hover:bg-green-700 text-white'
                    : quest.status === 'active'
                    ? 'bg-yellow-600 hover:bg-yellow-700 text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {quest.status === 'completed' ? (
                  <span className="flex items-center justify-center gap-2">
                    <Trophy className="w-4 h-4" />
                    Claim Rewards
                  </span>
                ) : quest.status === 'active' ? (
                  'Continue Quest'
                ) : (
                  'Accept Quest'
                )}
              </button>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};

export default QuestsModal;
