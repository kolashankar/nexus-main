import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import SearchBar from '../../../components/common/SearchBar';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import CategoryChips from '../../../components/common/CategoryChips';
import ArticlesFilterModal, { ArticleFilters } from '../../../components/learning/ArticlesFilterModal';
import SortModal, { SortOption } from '../../../components/common/SortModal';
import { toggleBookmark, isBookmarked } from '../../../lib/bookmarks';
import { getInProgressArticles, getArticleProgress } from '../../../lib/readProgress';

interface Article {
  _id: string;
  title: string;
  excerpt: string;
  author: string;
  category: string;
  tags: string[];
  cover_image?: string;
  read_time: number;
  views_count: number;
  created_at: string;
}

const CATEGORIES = [
  'All',
  'Career Growth',
  'Technical Skills',
  'Interview Preparation',
  'Resume Writing',
  'Soft Skills',
  'Industry Insights',
];

const SORT_OPTIONS: SortOption[] = [
  { label: 'Latest', value: 'latest' },
  { label: 'Most Viewed', value: 'views' },
  { label: 'Trending', value: 'trending' },
];

export default function LearningScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [showFilters, setShowFilters] = useState(false);
  const [showSort, setShowSort] = useState(false);
  const [sortBy, setSortBy] = useState('latest');
  const [bookmarkedArticles, setBookmarkedArticles] = useState<Set<string>>(new Set());
  const [inProgressIds, setInProgressIds] = useState<Set<string>>(new Set());
  const [filters, setFilters] = useState<ArticleFilters>({
    categories: [],
    tags: [],
    author: '',
    readTime: '',
  });
  const router = useRouter();

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['articles', searchQuery, selectedCategory, filters, sortBy],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      if (selectedCategory !== 'All') params.category = selectedCategory;
      if (filters.categories.length > 0) params.categories = filters.categories.join(',');
      if (filters.tags.length > 0) params.tags = filters.tags.join(',');
      if (filters.author) params.author = filters.author;
      if (filters.readTime) params.read_time_max = filters.readTime;
      if (sortBy) params.sort = sortBy;

      const response = await api.get('/user/articles', { params });
      return response.data.articles || [];
    },
  });

  useEffect(() => {
    loadBookmarks();
    loadInProgress();
  }, [data]);

  const loadBookmarks = async () => {
    const bookmarkedIds = new Set<string>();
    if (data) {
      for (const article of data) {
        if (await isBookmarked(article._id)) {
          bookmarkedIds.add(article._id);
        }
      }
      setBookmarkedArticles(bookmarkedIds);
    }
  };

  const loadInProgress = async () => {
    const inProgress = await getInProgressArticles();
    setInProgressIds(new Set(inProgress.map((p) => p.articleId)));
  };

  const handleArticlePress = (articleId: string) => {
    router.push(`/(tabs)/learning/${articleId}`);
  };

  const handleBookmark = async (article: Article, e: any) => {
    e.stopPropagation();
    const success = await toggleBookmark(article._id, 'article', article);
    if (success) {
      setBookmarkedArticles((prev) => {
        const newSet = new Set(prev);
        if (newSet.has(article._id)) {
          newSet.delete(article._id);
        } else {
          newSet.add(article._id);
        }
        return newSet;
      });
    }
  };

  const handleTagClick = (tag: string) => {
    setFilters((prev) => ({
      ...prev,
      tags: [tag],
    }));
  };

  const handleApplyFilters = (newFilters: ArticleFilters) => {
    setFilters(newFilters);
  };

  // Get all unique tags from articles
  const allTags = data
    ? Array.from(new Set(data.flatMap((article: Article) => article.tags)))
    : [];

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading articles..." />
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Articles"
          message="Failed to load articles. Please try again."
        />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="px-6 py-4">
        <Text className="text-white text-2xl font-bold">Learning</Text>
        <Text className="text-gray-400 text-sm mt-1">Explore articles and guides</Text>
      </View>

      <View className="px-4">
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Search articles..."
        />
      </View>

      {/* Filter and Sort Buttons */}
      <View className="flex-row px-4 py-2">
        <TouchableOpacity
          className="flex-row items-center bg-dark-200 px-4 py-2 rounded-lg mr-2"
          onPress={() => setShowFilters(true)}
        >
          <Ionicons name="options-outline" size={18} color="#fff" />
          <Text className="text-white ml-2 font-semibold">Filters</Text>
        </TouchableOpacity>
        <TouchableOpacity
          className="flex-row items-center bg-dark-200 px-4 py-2 rounded-lg"
          onPress={() => setShowSort(true)}
        >
          <Ionicons name="swap-vertical-outline" size={18} color="#fff" />
          <Text className="text-white ml-2 font-semibold">Sort</Text>
        </TouchableOpacity>
      </View>

      {/* Category Chips */}
      <CategoryChips
        categories={CATEGORIES}
        selectedCategory={selectedCategory}
        onSelectCategory={setSelectedCategory}
      />

      <ScrollView
        className="flex-1 px-4"
        refreshControl={
          <RefreshControl
            refreshing={isFetching}
            onRefresh={refetch}
            tintColor="#3b82f6"
          />
        }
      >
        {data && data.length === 0 ? (
          <EmptyState
            icon="book-outline"
            title="No Articles Found"
            message="No articles available at the moment. Check back later!"
          />
        ) : (
          data?.map((article: Article) => (
            <TouchableOpacity
              key={article._id}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => handleArticlePress(article._id)}
            >
              <View className="flex-row justify-between items-start mb-2">
                <View className="flex-1">
                  <Text className="text-white text-lg font-bold" numberOfLines={2}>
                    {article.title}
                  </Text>
                  <Text className="text-gray-400 text-sm mt-1">By {article.author}</Text>
                </View>
                <TouchableOpacity onPress={(e) => handleBookmark(article, e)}>
                  <Ionicons
                    name={
                      bookmarkedArticles.has(article._id) ? 'bookmark' : 'bookmark-outline'
                    }
                    size={24}
                    color={bookmarkedArticles.has(article._id) ? '#3b82f6' : '#9ca3af'}
                  />
                </TouchableOpacity>
              </View>

              {inProgressIds.has(article._id) && (
                <View className="bg-yellow-600/20 border border-yellow-600 px-2 py-1 rounded mb-2">
                  <Text className="text-yellow-600 text-xs">Continue Reading</Text>
                </View>
              )}

              <Text className="text-gray-300 text-sm mt-2" numberOfLines={3}>
                {article.excerpt}
              </Text>

              <View className="flex-row flex-wrap mt-3">
                {article.tags.slice(0, 3).map((tag, index) => (
                  <TouchableOpacity
                    key={index}
                    className="bg-dark-300 px-2 py-1 rounded mr-2 mb-2"
                    onPress={() => handleTagClick(tag)}
                  >
                    <Text className="text-gray-400 text-xs">#{tag}</Text>
                  </TouchableOpacity>
                ))}
              </View>

              <View className="flex-row items-center justify-between mt-3">
                <View className="flex-row items-center">
                  <Ionicons name="time-outline" size={14} color="#9ca3af" />
                  <Text className="text-gray-400 text-xs ml-1">
                    {article.read_time} min read
                  </Text>
                  <Ionicons name="eye-outline" size={14} color="#9ca3af" style={{ marginLeft: 12 }} />
                  <Text className="text-gray-400 text-xs ml-1">
                    {article.views_count} views
                  </Text>
                </View>
                <View className="bg-primary-600 px-3 py-1 rounded-full">
                  <Text className="text-white text-xs font-semibold">{article.category}</Text>
                </View>
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>

      <ArticlesFilterModal
        visible={showFilters}
        onClose={() => setShowFilters(false)}
        onApply={handleApplyFilters}
        currentFilters={filters}
        availableTags={allTags}
      />

      <SortModal
        visible={showSort}
        onClose={() => setShowSort(false)}
        onSelect={setSortBy}
        currentSort={sortBy}
        options={SORT_OPTIONS}
      />
    </SafeAreaView>
  );
}