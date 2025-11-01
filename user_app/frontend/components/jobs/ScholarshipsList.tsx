import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../lib/api';
import SearchBar from '../common/SearchBar';
import LoadingSpinner from '../common/LoadingSpinner';
import EmptyState from '../common/EmptyState';
import CategoryChips from '../common/CategoryChips';
import ScholarshipsFilterModal, { ScholarshipFilters } from './ScholarshipsFilterModal';
import SortModal, { SortOption } from '../common/SortModal';
import { toggleBookmark, isBookmarked } from '../../lib/bookmarks';

interface Scholarship {
  _id: string;
  name: string;
  provider: string;
  scholarship_type: string;
  education_level: string;
  country: string;
  amount_min?: number;
  amount_max?: number;
  deadline: string;
  description: string;
  is_active: boolean;
}

const CATEGORIES = [
  'All',
  'Academic Merit',
  'Need-Based',
  'Athletic',
  'Research',
  'Leadership',
  'Community Service',
];

const SORT_OPTIONS: SortOption[] = [
  { label: 'Most Recent', value: 'recent' },
  { label: 'Amount: High to Low', value: 'amount_desc' },
  { label: 'Amount: Low to High', value: 'amount_asc' },
  { label: 'Deadline: Earliest First', value: 'deadline_asc' },
];

export default function ScholarshipsList() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [showFilters, setShowFilters] = useState(false);
  const [showSort, setShowSort] = useState(false);
  const [sortBy, setSortBy] = useState('recent');
  const [bookmarkedScholarships, setBookmarkedScholarships] = useState<Set<string>>(new Set());
  const [filters, setFilters] = useState<ScholarshipFilters>({
    educationLevels: [],
    countries: [],
    amountMin: 0,
    amountMax: 100000,
    deadline: '',
  });

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['scholarships', searchQuery, selectedCategory, filters, sortBy],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      if (selectedCategory !== 'All') params.scholarship_type = selectedCategory;
      if (filters.educationLevels.length > 0)
        params.education_level = filters.educationLevels.join(',');
      if (filters.countries.length > 0) params.country = filters.countries.join(',');
      if (filters.amountMin > 0) params.amount_min = filters.amountMin;
      if (filters.amountMax < 100000) params.amount_max = filters.amountMax;
      if (sortBy) params.sort = sortBy;

      const response = await api.get('/user/scholarships', { params });
      return response.data.scholarships || [];
    },
  });

  useEffect(() => {
    loadBookmarks();
  }, [data]);

  const loadBookmarks = async () => {
    const bookmarkedIds = new Set<string>();
    if (data) {
      for (const scholarship of data) {
        if (await isBookmarked(scholarship._id)) {
          bookmarkedIds.add(scholarship._id);
        }
      }
      setBookmarkedScholarships(bookmarkedIds);
    }
  };

  const handleBookmark = async (scholarship: Scholarship, e: any) => {
    e.stopPropagation();
    const success = await toggleBookmark(scholarship._id, 'scholarship', scholarship);
    if (success) {
      setBookmarkedScholarships((prev) => {
        const newSet = new Set(prev);
        if (newSet.has(scholarship._id)) {
          newSet.delete(scholarship._id);
        } else {
          newSet.add(scholarship._id);
        }
        return newSet;
      });
    }
  };

  const handleApplyFilters = (newFilters: ScholarshipFilters) => {
    setFilters(newFilters);
  };

  if (isLoading) {
    return <LoadingSpinner message="Loading scholarships..." />;
  }

  if (isError) {
    return (
      <EmptyState
        icon="alert-circle-outline"
        title="Error Loading Scholarships"
        message="Failed to load scholarships. Please try again."
      />
    );
  }

  return (
    <View className="flex-1">
      <View className="px-4">
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Search scholarships..."
        />
      </View>

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
            icon="medal-outline"
            title="No Scholarships Found"
            message="No scholarships available at the moment. Check back later!"
          />
        ) : (
          data?.map((scholarship: Scholarship) => (
            <TouchableOpacity
              key={scholarship._id}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => router.push(`/(tabs)/jobs/scholarship-${scholarship._id}`)}
            >
              <View className="flex-row justify-between items-start mb-2">
                <View className="flex-1">
                  <Text className="text-white text-lg font-bold" numberOfLines={1}>
                    {scholarship.name}
                  </Text>
                  <Text className="text-gray-400 text-sm mt-1">{scholarship.provider}</Text>
                </View>
                <View className="flex-row items-center">
                  <View className="bg-purple-600 px-3 py-1 rounded-full mr-2">
                    <Text className="text-white text-xs font-semibold">
                      {scholarship.education_level}
                    </Text>
                  </View>
                  <TouchableOpacity onPress={(e) => handleBookmark(scholarship, e)}>
                    <Ionicons
                      name={
                        bookmarkedScholarships.has(scholarship._id)
                          ? 'bookmark'
                          : 'bookmark-outline'
                      }
                      size={24}
                      color={
                        bookmarkedScholarships.has(scholarship._id) ? '#3b82f6' : '#9ca3af'
                      }
                    />
                  </TouchableOpacity>
                </View>
              </View>

              <View className="flex-row flex-wrap mt-2">
                <View className="flex-row items-center mr-4 mb-2">
                  <Ionicons name="location-outline" size={14} color="#9ca3af" />
                  <Text className="text-gray-400 text-xs ml-1">{scholarship.country}</Text>
                </View>
                <View className="flex-row items-center mr-4 mb-2">
                  <Ionicons name="calendar-outline" size={14} color="#9ca3af" />
                  <Text className="text-gray-400 text-xs ml-1">
                    Deadline: {new Date(scholarship.deadline).toLocaleDateString()}
                  </Text>
                </View>
                {scholarship.amount_min && scholarship.amount_max && (
                  <View className="flex-row items-center mb-2">
                    <Ionicons name="cash-outline" size={14} color="#9ca3af" />
                    <Text className="text-gray-400 text-xs ml-1">
                      ${scholarship.amount_min.toLocaleString()} - $
                      {scholarship.amount_max.toLocaleString()}
                    </Text>
                  </View>
                )}
              </View>

              <Text className="text-gray-300 text-sm mt-2" numberOfLines={2}>
                {scholarship.description}
              </Text>

              <View className="flex-row items-center justify-between mt-3">
                <View className="bg-dark-300 px-3 py-1 rounded-full">
                  <Text className="text-gray-400 text-xs">
                    {scholarship.scholarship_type}
                  </Text>
                </View>
                <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>

      <ScholarshipsFilterModal
        visible={showFilters}
        onClose={() => setShowFilters(false)}
        onApply={handleApplyFilters}
        currentFilters={filters}
      />

      <SortModal
        visible={showSort}
        onClose={() => setShowSort(false)}
        onSelect={setSortBy}
        currentSort={sortBy}
        options={SORT_OPTIONS}
      />
    </View>
  );
}
