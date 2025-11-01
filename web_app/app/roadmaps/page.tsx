'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { Header } from '@/components/common/Header';
import { Footer } from '@/components/common/Footer';
import { RoadmapCard } from '@/components/roadmaps/RoadmapCard';
import { SearchBar } from '@/components/common/SearchBar';
import { SortDropdown } from '@/components/common/SortDropdown';
import { Skeleton } from '@/components/ui/Skeleton';
import { Button } from '@/components/ui/Button';
import { Map, TrendingUp } from 'lucide-react';
import { Roadmap } from '@/types';

const CATEGORIES = [
  'All',
  'Web Development',
  'Mobile Development',
  'AI/ML',
  'Data Science',
  'DevOps',
  'Cloud Computing',
  'Cybersecurity',
];

const LEVELS = ['All', 'Beginner', 'Intermediate', 'Advanced'];

const SORT_OPTIONS = [
  { label: 'Most Recent', value: '-created_at' },
  { label: 'Title A-Z', value: 'title' },
  { label: 'Shortest First', value: 'estimated_time_hours' },
];

export default function RoadmapsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedLevel, setSelectedLevel] = useState('All');
  const [sortBy, setSortBy] = useState('-created_at');

  const { data, isLoading, error } = useQuery({
    queryKey: ['roadmaps', searchQuery, selectedCategory, selectedLevel, sortBy],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
        sort: sortBy,
      };

      if (selectedCategory !== 'All') {
        params.category = selectedCategory;
      }

      if (selectedLevel !== 'All') {
        params.level = selectedLevel;
      }

      const response = await apiClient.getRoadmaps(params);
      return response;
    },
  });

  const roadmaps: Roadmap[] = data?.data || [];

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-700 text-white py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl">
              <div className="flex items-center mb-4">
                <Map className="w-8 h-8 mr-3" />
                <h1 className="text-4xl font-bold">Learning Roadmaps</h1>
              </div>
              <p className="text-xl text-indigo-100">
                Structured learning paths to master any technology
              </p>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-4 py-8">
          {/* Category Tabs */}
          <div className="mb-6 overflow-x-auto">
            <div className="flex space-x-3 pb-2">
              {CATEGORIES.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                    selectedCategory === category
                      ? 'bg-indigo-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-indigo-50 border border-gray-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Level Filter */}
          <div className="mb-6">
            <div className="flex space-x-3">
              {LEVELS.map((level) => (
                <button
                  key={level}
                  onClick={() => setSelectedLevel(level)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedLevel === level
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'text-gray-600 hover:bg-gray-100'
                  }`}
                >
                  {level}
                </button>
              ))}
            </div>
          </div>

          {/* Search & Sort Bar */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="flex-1">
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder="Search roadmaps by title or topic..."
              />
            </div>
            <SortDropdown
              options={SORT_OPTIONS}
              value={sortBy}
              onChange={setSortBy}
            />
          </div>

          {/* Roadmaps Grid */}
          {isLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <Skeleton key={i} className="h-96" />
              ))}
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-600 mb-4">Failed to load roadmaps</p>
              <Button onClick={() => window.location.reload()}>Try Again</Button>
            </div>
          ) : roadmaps.length === 0 ? (
            <div className="text-center py-12">
              <Map className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No roadmaps found
              </h3>
              <p className="text-gray-600">
                Try adjusting your search or filters
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {roadmaps.map((roadmap) => (
                <RoadmapCard key={roadmap.id} roadmap={roadmap} />
              ))}
            </div>
          )}
        </div>
      </div>
      <Footer />
    </>
  );
}
