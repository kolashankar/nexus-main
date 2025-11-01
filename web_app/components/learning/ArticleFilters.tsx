'use client';

import React from 'react';
import { X, Filter } from 'lucide-react';
import { Button } from '@/components/ui/Button';

interface ArticleFiltersProps {
  isOpen: boolean;
  onClose: () => void;
  filters: {
    category: string;
    tags: string[];
    read_time: string;
  };
  onFilterChange: (filters: any) => void;
}

const CATEGORIES = [
  'All Categories',
  'Career Development',
  'Interview Preparation',
  'Technical Skills',
  'Soft Skills',
  'Industry Trends',
  'Job Search',
  'Productivity',
  'Personal Finance',
];

const READ_TIME_OPTIONS = [
  { label: 'All', value: '' },
  { label: '< 5 min', value: '5' },
  { label: '5-10 min', value: '10' },
  { label: '10-15 min', value: '15' },
  { label: '> 15 min', value: '15+' },
];

export function ArticleFilters({ isOpen, onClose, filters, onFilterChange }: ArticleFiltersProps) {
  const [localFilters, setLocalFilters] = React.useState(filters);

  const handleCategoryChange = (category: string) => {
    const newFilters = {
      ...localFilters,
      category: category === 'All Categories' ? '' : category,
    };
    setLocalFilters(newFilters);
  };

  const handleReadTimeChange = (readTime: string) => {
    const newFilters = {
      ...localFilters,
      read_time: readTime,
    };
    setLocalFilters(newFilters);
  };

  const handleApply = () => {
    onFilterChange(localFilters);
    onClose();
  };

  const handleReset = () => {
    const resetFilters = {
      category: '',
      tags: [],
      read_time: '',
    };
    setLocalFilters(resetFilters);
    onFilterChange(resetFilters);
  };

  if (!isOpen) return null;

  return (
    <>
      {/* Backdrop (mobile) */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
        onClick={onClose}
      />

      {/* Filter Panel */}
      <div className="fixed lg:sticky top-0 right-0 h-full lg:h-auto w-80 bg-white shadow-xl z-50 lg:z-0 overflow-y-auto">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center">
              <Filter className="w-5 h-5 mr-2 text-purple-600" />
              <h3 className="text-lg font-semibold text-gray-900">Filters</h3>
            </div>
            <button
              onClick={onClose}
              className="lg:hidden p-2 hover:bg-gray-100 rounded-full"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Category Filter */}
          <div className="mb-6">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Category</h4>
            <div className="space-y-2">
              {CATEGORIES.map((category) => (
                <label key={category} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="category"
                    checked={
                      localFilters.category === '' && category === 'All Categories'
                        ? true
                        : localFilters.category === category
                    }
                    onChange={() => handleCategoryChange(category)}
                    className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{category}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Read Time Filter */}
          <div className="mb-6">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Read Time</h4>
            <div className="space-y-2">
              {READ_TIME_OPTIONS.map((option) => (
                <label key={option.value} className="flex items-center cursor-pointer">
                  <input
                    type="radio"
                    name="read_time"
                    checked={localFilters.read_time === option.value}
                    onChange={() => handleReadTimeChange(option.value)}
                    className="w-4 h-4 text-purple-600 border-gray-300 focus:ring-purple-500"
                  />
                  <span className="ml-2 text-sm text-gray-700">{option.label}</span>
                </label>
              ))}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="space-y-3">
            <Button onClick={handleApply} className="w-full bg-purple-600 hover:bg-purple-700">
              Apply Filters
            </Button>
            <Button onClick={handleReset} variant="outline" className="w-full">
              Reset All
            </Button>
          </div>
        </div>
      </div>
    </>
  );
}
