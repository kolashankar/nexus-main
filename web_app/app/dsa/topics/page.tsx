'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { TopicCard } from '@/components/dsa/TopicCard';
import { SearchBar } from '@/components/common/SearchBar';
import { Skeleton } from '@/components/ui/Skeleton';
import { Button } from '@/components/ui/Button';
import { BookOpen } from 'lucide-react';
import { DSATopic } from '@/types';

export default function DSATopicsPage() {
  const [searchQuery, setSearchQuery] = useState('');

  const { data, isLoading, error } = useQuery({
    queryKey: ['dsa-topics', searchQuery],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
      };
      const response = await apiClient.getDSATopics(params);
      return response;
    },
  });

  const topics: DSATopic[] = data?.data || [];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-white border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center mb-4">
            <BookOpen className="w-6 h-6 text-green-600 mr-2" />
            <h1 className="text-2xl font-bold text-gray-900">DSA Topics</h1>
          </div>
          <p className="text-gray-600">Browse problems organized by data structure and algorithm topics</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-8">
        <div className="mb-6">
          <SearchBar
            value={searchQuery}
            onChange={setSearchQuery}
            placeholder="Search topics..."
          />
        </div>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Skeleton key={i} className="h-48" />
            ))}
          </div>
        ) : error ? (
          <div className="text-center py-12">
            <p className="text-red-600 mb-4">Failed to load topics</p>
            <Button onClick={() => window.location.reload()}>Try Again</Button>
          </div>
        ) : topics.length === 0 ? (
          <div className="text-center py-12">
            <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-gray-900 mb-2">No topics found</h3>
            <p className="text-gray-600">Try adjusting your search</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {topics.map((topic) => (
              <TopicCard key={topic.id} topic={topic} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}