'use client';

import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { Header } from '@/components/common/Header';
import { Footer } from '@/components/common/Footer';
import { ArticleCard } from '@/components/learning/ArticleCard';
import { ArticleFilters } from '@/components/learning/ArticleFilters';
import { SearchBar } from '@/components/common/SearchBar';
import { SortDropdown } from '@/components/common/SortDropdown';
import { Button } from '@/components/ui/Button';
import { Skeleton } from '@/components/ui/Skeleton';
import { Filter, BookOpen, TrendingUp } from 'lucide-react';
import { Article } from '@/types';

const CATEGORIES = [
  'All',
  'Career Development',
  'Interview Preparation',
  'Technical Skills',
  'Soft Skills',
  'Industry Trends',
  'Job Search',
  'Productivity',
];

const SORT_OPTIONS = [
  { label: 'Most Recent', value: '-created_at' },
  { label: 'Most Popular', value: '-views_count' },
  { label: 'Quick Read', value: 'read_time' },
  { label: 'Long Read', value: '-read_time' },
];

export default function LearningPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [sortBy, setSortBy] = useState('-created_at');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    category: '',
    tags: [],
    read_time: '',
  });

  // Fetch articles
  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', searchQuery, selectedCategory, sortBy, filters],
    queryFn: async () => {
      const params: any = {
        search: searchQuery || undefined,
        sort: sortBy,
      };

      if (filters.category) {
        params.category = filters.category;
      } else if (selectedCategory !== 'All') {
        params.category = selectedCategory;
      }

      if (filters.read_time) {
        params.max_read_time = filters.read_time;
      }

      const response = await apiClient.getArticles(params);
      return response;
    },
  });

  const articles: Article[] = data?.data || [];

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-purple-600 to-indigo-700 text-white py-16">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl">
              <div className="flex items-center mb-4">
                <BookOpen className="w-8 h-8 mr-3" />
                <h1 className="text-4xl font-bold">Learning Hub</h1>
              </div>
              <p className="text-xl text-purple-100">
                Discover insightful articles to advance your career and skills
              </p>
            </div>
          </div>
        </div>

        <div className="container mx-auto px-4 py-8">
          {/* Category Chips */}
          <div className="mb-6 overflow-x-auto">
            <div className="flex space-x-3 pb-2">
              {CATEGORIES.map((category) => (
                <button
                  key={category}
                  onClick={() => setSelectedCategory(category)}
                  className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors ${
                    selectedCategory === category
                      ? 'bg-purple-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-purple-50 border border-gray-200'
                  }`}
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          {/* Search & Filter Bar */}
          <div className="flex flex-col md:flex-row gap-4 mb-8">
            <div className="flex-1">
              <SearchBar
                value={searchQuery}
                onChange={setSearchQuery}
                placeholder="Search articles by title, tags, or author..."
              />
            </div>
            <div className="flex gap-3">
              <SortDropdown
                options={SORT_OPTIONS}
                value={sortBy}
                onChange={setSortBy}
              />
              <Button
                variant="outline"
                onClick={() => setShowFilters(!showFilters)}
                className="lg:hidden"
              >
                <Filter className="w-4 h-4 mr-2" />
                Filters
              </Button>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex gap-8">
            {/* Articles Grid */}
            <div className="flex-1">
              {isLoading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {[...Array(6)].map((_, i) => (
                    <Skeleton key={i} className="h-96" />
                  ))}
                </div>
              ) : error ? (
                <div className="text-center py-12">
                  <p className="text-red-600 mb-4">Failed to load articles</p>
                  <Button onClick={() => window.location.reload()}>Try Again</Button>
                </div>
              ) : articles.length === 0 ? (
                <div className="text-center py-12">
                  <BookOpen className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">
                    No articles found
                  </h3>
                  <p className="text-gray-600">
                    Try adjusting your search or filters
                  </p>
                </div>
              ) : (
                <>
                  {/* Featured Article (First) */}
                  {articles.length > 0 && (
                    <div className="mb-8">
                      <div className="flex items-center mb-4">
                        <TrendingUp className="w-5 h-5 text-purple-600 mr-2" />
                        <h2 className="text-2xl font-bold text-gray-900">Featured Article</h2>
                      </div>
                      <ArticleCard article={articles[0]} />
                    </div>
                  )}

                  {/* All Articles Grid */}
                  {articles.length > 1 && (
                    <>
                      <h2 className="text-2xl font-bold text-gray-900 mb-6">
                        All Articles
                      </h2>
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {articles.slice(1).map((article) => (
                          <ArticleCard key={article.id} article={article} />
                        ))}
                      </div>
                    </>
                  )}
                </>
              )}
            </div>

            {/* Filter Sidebar (Desktop) */}
            <div className="hidden lg:block w-80">
              <ArticleFilters
                isOpen={true}
                onClose={() => {}}
                filters={filters}
                onFilterChange={setFilters}
              />
            </div>
          </div>

          {/* Filter Modal (Mobile) */}
          {showFilters && (
            <ArticleFilters
              isOpen={showFilters}
              onClose={() => setShowFilters(false)}
              filters={filters}
              onFilterChange={setFilters}
            />
          )}
        </div>
      </div>
      <Footer />
    </>
  );
}
