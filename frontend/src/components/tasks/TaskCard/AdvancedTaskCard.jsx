"""Advanced task card component."""

import React from 'react';
import { 
  Award, 
  Coins, 
  Star, 
  MapPin, 
  Clock, 
  Shield, 
  Zap,
  Users,
  Lock,
  Unlock,
  TrendingUp
} from 'lucide-react';

const AdvancedTaskCard = ({ task, onSelect, isSelected = false }) => {
  const getDifficultyColor = (difficulty) => {
    const colors = {
      tutorial: 'border-gray-500 bg-gray-500/10',
      easy: 'border-green-500 bg-green-500/10',
      medium: 'border-yellow-500 bg-yellow-500/10',
      hard: 'border-red-500 bg-red-500/10',
      expert: 'border-purple-500 bg-purple-500/10',
      legendary: 'border-amber-500 bg-amber-500/10'
    };
    return colors[difficulty] || colors.easy;
  };

  const getTypeIcon = (type) => {
    const icons = {
      combat: '⚔️',
      economic: '💰',
      relationship: '🤝',
      guild: '🏰',
      ethical_dilemma: '⚖️',
      moral_choice: '🧐',
      exploration: '🧭',
      skill_based: '🛠️',
      social: '👥',
      coop: '🤜🤛',
      competitive: '🏆'
    };
    return icons[type] || '❔';
  };

  const formatExpiry = (expiresAt) => {
    if (!expiresAt) return null;
    
    const now = new Date();
    const expiry = new Date(expiresAt);
    const diff = expiry - now;
    
    if (diff <= 0) return { text: 'Expired', urgent: true };
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    const urgent = hours < 1;
    const text = hours > 0 ? `${hours}h ${minutes}m` : `${minutes}m`;
    
    return { text, urgent };
  };

  const expiry = formatExpiry(task.expires_at);
  const rewards = task.base_rewards || {
    xp: task.xp_reward || 0,
    credits: task.credits_reward || 0,
    karma: task.karma_reward || 0
  };

  return (
    <div
      onClick={() => onSelect(task)}
      className={`relative rounded-lg p-5 border-2 cursor-pointer transition-all duration-300 ${
        isSelected 
          ? 'ring-4 ring-purple-500 border-purple-500 shadow-lg shadow-purple-500/50 scale-105' 
          : `${getDifficultyColor(task.difficulty)} hover:scale-102 hover:shadow-xl`
      }`}
    >
      {/* Difficulty Badge */}
      <div className="absolute top-3 right-3 px-2 py-1 rounded-full text-xs font-bold uppercase backdrop-blur-sm bg-black/40">
        {task.difficulty}
      </div>

      {/* Multiplayer Badge */}
      {task.is_multiplayer && (
        <div className="absolute top-3 left-3 px-2 py-1 rounded-full text-xs font-semibold bg-blue-600/80 backdrop-blur-sm flex items-center gap-1">
          <Users className="w-3 h-3" />
          {task.required_players || 2}+
        </div>
      )}

      {/* Type Icon */}
      <div className="text-4xl mb-3">{getTypeIcon(task.type)}</div>

      {/* Title */}
      <h3 className="text-xl font-bold text-white mb-2">{task.title}</h3>

      {/* Type Label */}
      <div className="text-sm text-gray-400 mb-3">
        {task.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
      </div>

      {/* Description */}
      <p className="text-gray-300 text-sm mb-4 line-clamp-3">
        {task.description}
      </p>

      {/* Location */}
      {task.location_requirement && (
        <div className="flex items-center gap-2 text-sm text-blue-400 mb-3 bg-blue-500/10 rounded p-2">
          <MapPin className="w-4 h-4" />
          <div>
            <div className="font-medium">{task.location_requirement.name}</div>
            <div className="text-xs text-blue-300">{task.location_requirement.zone}</div>
          </div>
        </div>
      )}

      {/* Skill Requirements */}
      {task.skill_requirements && task.skill_requirements.length > 0 && (
        <div className="mb-3 p-2 bg-orange-500/10 rounded border border-orange-500/30">
          <div className="flex items-center gap-1 text-xs text-orange-400 mb-1">
            <Lock className="w-3 h-3" />
            <span className="font-semibold">Requirements:</span>
          </div>
          <div className="space-y-1">
            {task.skill_requirements.map((req, idx) => (
              <div key={idx} className="text-xs text-orange-300 flex items-center gap-2">
                <span className="font-medium">{req.skill_name}:</span>
                <span>{req.min_level}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Rewards */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        <div className="bg-yellow-500/10 rounded p-2 text-center">
          <Award className="w-4 h-4 text-yellow-400 mx-auto mb-1" />
          <div className="text-xs text-yellow-400 font-semibold">{rewards.xp}</div>
          <div className="text-xs text-gray-400">XP</div>
        </div>
        <div className="bg-green-500/10 rounded p-2 text-center">
          <Coins className="w-4 h-4 text-green-400 mx-auto mb-1" />
          <div className="text-xs text-green-400 font-semibold">{rewards.credits}</div>
          <div className="text-xs text-gray-400">Credits</div>
        </div>
        {rewards.karma !== 0 && (
          <div className={`${rewards.karma > 0 ? 'bg-blue-500/10' : 'bg-red-500/10'} rounded p-2 text-center`}>
            <Star className={`w-4 h-4 ${rewards.karma > 0 ? 'text-blue-400' : 'text-red-400'} mx-auto mb-1`} />
            <div className={`text-xs ${rewards.karma > 0 ? 'text-blue-400' : 'text-red-400'} font-semibold`}>
              {rewards.karma > 0 ? '+' : ''}{rewards.karma}
            </div>
            <div className="text-xs text-gray-400">Karma</div>
          </div>
        )}
      </div>

      {/* Additional Rewards */}
      {(rewards.items?.length > 0 || rewards.skills?.length > 0 || rewards.titles?.length > 0) && (
        <div className="mb-3 p-2 bg-purple-500/10 rounded border border-purple-500/30">
          <div className="flex items-center gap-1 text-xs text-purple-400 mb-1">
            <Zap className="w-3 h-3" />
            <span className="font-semibold">Bonus Rewards:</span>
          </div>
          <div className="text-xs text-purple-300 space-y-1">
            {rewards.items?.length > 0 && <div>🎁 {rewards.items.length} items</div>}
            {rewards.skills?.length > 0 && <div>⚡ {rewards.skills.length} skills</div>}
            {rewards.titles?.length > 0 && <div>🏆 {rewards.titles.length} titles</div>}
          </div>
        </div>
      )}

      {/* Story Progress */}
      {task.story_arc && (
        <div className="flex items-center gap-2 text-xs text-purple-400 mb-3">
          <TrendingUp className="w-3 h-3" />
          <span>
            {task.story_arc} {task.sequence_number && `(Part ${task.sequence_number})`}
          </span>
        </div>
      )}

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-700">
        <div className="flex items-center gap-1 text-xs text-gray-400">
          <span>{task.choices?.length || 0} choices</span>
        </div>
        {expiry && (
          <div className={`flex items-center gap-1 text-xs ${expiry.urgent ? 'text-red-400' : 'text-gray-400'}`}>
            <Clock className="w-3 h-3" />
            <span>{expiry.text}</span>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdvancedTaskCard;
