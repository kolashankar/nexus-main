'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { SheetCard } from '@/components/dsa/SheetCard';
import { SearchBar } from '@/components/common/SearchBar';
import { Skeleton } from '@/components/ui/Skeleton';
import { Button } from '@/components/ui/Button';
import { FileText } from 'lucide-react';
import { DSASheet } from '@/types';

const LEVELS = ['All', 'Beginner', 'Intermediate', 'Advanced'];

export default function DSASheetsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLevel, setSelectedLevel] = useState('All');

  const { data, isLoading, error } = useQuery({
    queryKey: ['dsa-sheets', searchQuery, selectedLevel],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
      };
      if (selectedLevel !== 'All') {
        params.level = selectedLevel;
      }
      const response = await apiClient.getDSASheets(params);
      return response;
    },
  });

  const sheets: DSASheet[] = data?.data || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center mb-4">
            <FileText className="w-6 h-6 text-purple-600 mr-2" />
            <h1 className="text-2xl font-bold text-gray-900">DSA Sheets</h1>
          </div>
          <p className="text-gray-600">Curated problem lists for systematic practice</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <div className="flex space-x-3 overflow-x-auto pb-2 mb-4">
            {LEVELS.map((level) => (
              <button
                key={level}
                onClick={() => setSelectedLevel(level)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                  selectedLevel === level
                    ? 'bg-purple-600 text-white'
                    : 'bg-white text-gray-700 hover:bg-purple-50 border border-gray-200'
                }`}
              >
                {level}
              </button>
            ))}
          </div>
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search sheets..."
          />
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-80" />
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600 mb-4">Failed to load sheets</p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </div>
        ) : sheets.length === 0 ? (
          <div className="text-center py-12">
            <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No sheets found</h3>
            <p className="text-gray-600">Try adjusting your search or filters</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sheets.map((sheet) => (
              <SheetCard key={sheet.id} sheet={sheet} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}