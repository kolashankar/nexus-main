"""Enhanced task list component."""

import React, { useState, useEffect } from 'react';
import { Clock, Star, Award, MapPin, Lock, TrendingUp } from 'lucide-react';
import TaskFilters from '../TaskFilters/TaskFilters';

const EnhancedTaskList = ({ tasks, onTaskSelect, showFilters = true }) => {
  const [filteredTasks, setFilteredTasks] = useState(tasks);
  const [filters, setFilters] = useState({
    type: null,
    difficulty: null,
    category: null
  });

  useEffect(() => {
    applyFilters();
  }, [tasks, filters]);

  const applyFilters = () => {
    let filtered = [...tasks];

    if (filters.type) {
      filtered = filtered.filter(task => task.type === filters.type);
    }

    if (filters.difficulty) {
      filtered = filtered.filter(task => task.difficulty === filters.difficulty);
    }

    if (filters.category) {
      filtered = filtered.filter(task => task.category === filters.category);
    }

    setFilteredTasks(filtered);
  };

  const clearFilters = () => {
    setFilters({
      type: null,
      difficulty: null,
      category: null
    });
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      tutorial: 'text-gray-400',
      easy: 'text-green-400',
      medium: 'text-yellow-400',
      hard: 'text-red-400',
      expert: 'text-purple-400',
      legendary: 'text-amber-400'
    };
    return colors[difficulty] || 'text-gray-400';
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
      social: '👥'
    };
    return icons[type] || '❔';
  };

  const formatTimeRemaining = (expiresAt) => {
    if (!expiresAt) return null;
    
    const now = new Date();
    const expiry = new Date(expiresAt);
    const diff = expiry - now;
    
    if (diff <= 0) return 'Expired';
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 0) {
      return `${hours}h ${minutes}m remaining`;
    }
    return `${minutes}m remaining`;
  };

  return (
    <div className="space-y-6">
      {showFilters && (
        <TaskFilters 
          filters={filters} 
          onFilterChange={setFilters} 
          onClearFilters={clearFilters} 
        />
      )}

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredTasks.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <p className="text-gray-400 text-lg">No tasks match your filters</p>
            {Object.values(filters).some(v => v !== null) && (
              <button
                onClick={clearFilters}
                className="mt-4 px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
              >
                Clear Filters
              </button>
            )}
          </div>
        ) : (
          filteredTasks.map(task => (
            <div
              key={task.task_id || task.id}
              onClick={() => onTaskSelect(task)}
              className="bg-slate-800/70 backdrop-blur-sm rounded-lg p-4 border border-purple-500/20 hover:border-purple-500/50 cursor-pointer transition-all hover:shadow-lg hover:shadow-purple-500/20"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{getTypeIcon(task.type)}</span>
                  <div>
                    <h3 className="font-semibold text-white">{task.title}</h3>
                    <span className="text-xs text-gray-400">
                      {task.type.replace(/_/g, ' ')}
                    </span>
                  </div>
                </div>
                <span className={`text-xs font-bold uppercase ${getDifficultyColor(task.difficulty)}`}>
                  {task.difficulty}
                </span>
              </div>

              {/* Description */}
              <p className="text-sm text-gray-300 mb-3 line-clamp-2">
                {task.description}
              </p>

              {/* Location */}
              {task.location_requirement && (
                <div className="flex items-center gap-1 text-xs text-blue-400 mb-2">
                  <MapPin className="w-3 h-3" />
                  <span>{task.location_requirement.name}</span>
                </div>
              )}

              {/* Rewards */}
              <div className="flex items-center gap-3 text-sm mb-3">
                <div className="flex items-center gap-1 text-yellow-400">
                  <Award className="w-4 h-4" />
                  <span>{task.xp_reward || task.base_rewards?.xp || 0} XP</span>
                </div>
                <div className="flex items-center gap-1 text-green-400">
                  <Star className="w-4 h-4" />
                  <span>{task.credits_reward || task.base_rewards?.credits || 0}</span>
                </div>
              </div>

              {/* Requirements */}
              {task.skill_requirements && task.skill_requirements.length > 0 && (
                <div className="flex items-center gap-1 text-xs text-orange-400 mb-2">
                  <Lock className="w-3 h-3" />
                  <span>
                    Requires: {task.skill_requirements.map(req => req.skill_name).join(', ')}
                  </span>
                </div>
              )}

              {/* Footer */}
              <div className="flex items-center justify-between pt-2 border-t border-slate-700">
                <span className="text-xs text-gray-400">
                  {task.choices?.length || 0} choices
                </span>
                {task.expires_at && (
                  <div className="flex items-center gap-1 text-xs text-gray-400">
                    <Clock className="w-3 h-3" />
                    <span>{formatTimeRemaining(task.expires_at)}</span>
                  </div>
                )}
              </div>

              {/* Progression indicator */}
              {task.sequence_number && (
                <div className="flex items-center gap-1 mt-2 text-xs text-purple-400">
                  <TrendingUp className="w-3 h-3" />
                  <span>Part {task.sequence_number} of story</span>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default EnhancedTaskList;
