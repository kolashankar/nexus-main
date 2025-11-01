'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { QuestionTable } from '@/components/dsa/QuestionTable';
import { SearchBar } from '@/components/common/SearchBar';
import { SortDropdown } from '@/components/common/SortDropdown';
import { Button } from '@/components/ui/Button';
import { Skeleton } from '@/components/ui/Skeleton';
import { Filter, Code } from 'lucide-react';
import { DSAQuestion } from '@/types';

const DIFFICULTIES = ['All', 'Easy', 'Medium', 'Hard'];

const SORT_OPTIONS = [
  { label: 'Most Recent', value: '-created_at' },
  { label: 'Title A-Z', value: 'title' },
  { label: 'Difficulty', value: 'difficulty' },
];

export default function DSAQuestionsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('All');
  const [sortBy, setSortBy] = useState('-created_at');

  const { data, isLoading, error } = useQuery({
    queryKey: ['dsa-questions', searchQuery, selectedDifficulty, sortBy],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
        sort: sortBy,
      };

      if (selectedDifficulty !== 'All') {
        params.difficulty = selectedDifficulty;
      }

      const response = await apiClient.getDSAQuestions(params);
      return response;
    },
  });

  const questions: DSAQuestion[] = data?.data || [];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center mb-4">
            <Code className="w-6 h-6 text-blue-600 mr-2" />
            <h1 className="text-2xl font-bold text-gray-900">DSA Questions</h1>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        {/* Difficulty Filter */}
        <div className="mb-6">
          <div className="flex space-x-3 overflow-x-auto pb-2">
            {DIFFICULTIES.map((diff) => (
              <button
                key={diff}
                onClick={() => setSelectedDifficulty(diff)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  selectedDifficulty === diff
                    ? 'bg-blue-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-blue-50 border border-gray-200'
                }`}
              >
                {diff}
              </button>
            ))}
          </div>
        </div>

        {/* Search & Sort Bar */}
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1">
            <SearchBar
              value={searchQuery}
              onChange={setSearchQuery}
              placeholder="Search questions by title or topic..."
            />
          </div>
          <SortDropdown
            options={SORT_OPTIONS}
            value={sortBy}
            onChange={setSortBy}
          />
        </div>

        {/* Questions Table */}
        <div className="bg-white rounded-lg shadow-sm overflow-hidden">
          {isLoading ? (
            <div className="p-8">
              <Skeleton className="h-12 mb-4" />
              <Skeleton className="h-12 mb-4" />
              <Skeleton className="h-12 mb-4" />
            </div>
          ) : error ? (
            <div className="text-center py-12">
              <p className="text-red-600 mb-4">Failed to load questions</p>
              <Button onClick={() => window.location.reload()}>Try Again</Button>
            </div>
          ) : questions.length === 0 ? (
            <div className="text-center py-12">
              <Code className="w-16 h-16 text-gray-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                No questions found
              </h3>
              <p className="text-gray-600">Try adjusting your search or filters</p>
            </div>
          ) : (
            <QuestionTable questions={questions} />
          )}
        </div>
      </div>
    </div>
  );
}