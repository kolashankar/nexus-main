"""Task filters component."""

import React from 'react';
import { Filter, X } from 'lucide-react';

const TaskFilters = ({ filters, onFilterChange, onClearFilters }) => {
  const taskTypes = [
    { value: 'combat', label: 'Combat', icon: '⚔️' },
    { value: 'economic', label: 'Economic', icon: '💰' },
    { value: 'relationship', label: 'Relationship', icon: '🤝' },
    { value: 'guild', label: 'Guild', icon: '🏰' },
    { value: 'ethical_dilemma', label: 'Ethical', icon: '⚖️' },
    { value: 'exploration', label: 'Exploration', icon: '🧭' },
    { value: 'skill_based', label: 'Skill', icon: '🛠️' },
    { value: 'social', label: 'Social', icon: '👥' },
  ];

  const difficulties = [
    { value: 'easy', label: 'Easy', color: 'green' },
    { value: 'medium', label: 'Medium', color: 'yellow' },
    { value: 'hard', label: 'Hard', color: 'red' },
    { value: 'expert', label: 'Expert', color: 'purple' },
    { value: 'legendary', label: 'Legendary', color: 'amber' },
  ];

  const categories = [
    { value: 'daily', label: 'Daily' },
    { value: 'story', label: 'Story' },
    { value: 'personal', label: 'Personal' },
    { value: 'hidden', label: 'Hidden' },
  ];

  const handleFilterChange = (filterType, value) => {
    onFilterChange({
      ...filters,
      [filterType]: filters[filterType] === value ? null : value
    });
  };

  const activeFilterCount = Object.values(filters).filter(v => v !== null).length;

  return (
    <div className="bg-slate-800/50 backdrop-blur-sm rounded-lg p-4 border border-purple-500/20">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Filter className="w-5 h-5 text-purple-400" />
          <h3 className="text-lg font-semibold text-white">Filters</h3>
          {activeFilterCount > 0 && (
            <span className="px-2 py-1 text-xs bg-purple-600 text-white rounded-full">
              {activeFilterCount}
            </span>
          )}
        </div>
        {activeFilterCount > 0 && (
          <button
            onClick={onClearFilters}
            className="flex items-center gap-1 text-sm text-red-400 hover:text-red-300 transition-colors"
          >
            <X className="w-4 h-4" />
            Clear All
          </button>
        )}
      </div>

      {/* Task Type Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-300 mb-2">Task Type</label>
        <div className="flex flex-wrap gap-2">
          {taskTypes.map(type => (
            <button
              key={type.value}
              onClick={() => handleFilterChange('type', type.value)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                filters.type === type.value
                  ? 'bg-purple-600 text-white ring-2 ring-purple-400'
                  : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
              }`}
            >
              <span className="mr-1">{type.icon}</span>
              {type.label}
            </button>
          ))}
        </div>
      </div>

      {/* Difficulty Filter */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-300 mb-2">Difficulty</label>
        <div className="flex flex-wrap gap-2">
          {difficulties.map(diff => (
            <button
              key={diff.value}
              onClick={() => handleFilterChange('difficulty', diff.value)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                filters.difficulty === diff.value
                  ? `bg-${diff.color}-600 text-white ring-2 ring-${diff.color}-400`
                  : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
              }`}
            >
              {diff.label}
            </button>
          ))}
        </div>
      </div>

      {/* Category Filter */}
      <div>
        <label className="block text-sm font-medium text-gray-300 mb-2">Category</label>
        <div className="flex flex-wrap gap-2">
          {categories.map(cat => (
            <button
              key={cat.value}
              onClick={() => handleFilterChange('category', cat.value)}
              className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                filters.category === cat.value
                  ? 'bg-blue-600 text-white ring-2 ring-blue-400'
                  : 'bg-slate-700 text-gray-300 hover:bg-slate-600'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TaskFilters;
