import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import SearchBar from '@/components/common/SearchBar';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

interface Roadmap {
  _id: string;
  title: string;
  description: string;
  category: string;
  subcategory: string;
  difficulty_level: string;
  estimated_duration: string;
  nodes: any[];
  is_published: boolean;
}

const categories = [
  'All',
  'Web Dev',
  'Mobile Dev',
  'AI/ML',
  'Data Science',
  'DevOps',
  'Backend',
  'Frontend'
];

const difficultyColors = {
  'Beginner': 'bg-green-100 text-green-700',
  'Intermediate': 'bg-yellow-100 text-yellow-700',
  'Advanced': 'bg-red-100 text-red-700'
};

export default function RoadmapsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState({
    difficulty: 'all',
    duration: 'all',
    status: 'all'
  });

  const { data, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['roadmaps', searchQuery, selectedCategory, filters],
    queryFn: async () => {
      const params: any = {
        is_published: true,
        limit: 100
      };
      
      if (searchQuery) params.search = searchQuery;
      if (selectedCategory !== 'All') params.category = selectedCategory;
      if (filters.difficulty !== 'all') params.difficulty_level = filters.difficulty;
      
      const response = await api.get('/admin/roadmaps', { params });
      return response.data.roadmaps || [];
    }
  });

  // Calculate user progress for each roadmap (placeholder - would come from backend)
  const getRoadmapProgress = (roadmap: Roadmap) => {
    // In real app, this would fetch from user progress data
    return Math.floor(Math.random() * 100);
  };

  const getDurationCategory = (duration: string) => {
    const hours = parseInt(duration);
    if (hours < 90) return '<3 months';
    if (hours < 180) return '3-6 months';
    return '6+ months';
  };

  const filteredData = data?.filter((roadmap: Roadmap) => {
    if (filters.duration !== 'all') {
      const durationCat = getDurationCategory(roadmap.estimated_duration);
      if (filters.duration !== durationCat) return false;
    }
    
    if (filters.status !== 'all') {
      const progress = getRoadmapProgress(roadmap);
      if (filters.status === 'not_started' && progress > 0) return false;
      if (filters.status === 'in_progress' && (progress === 0 || progress === 100)) return false;
      if (filters.status === 'completed' && progress !== 100) return false;
    }
    
    return true;
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-gray-50">
        <LoadingSpinner message="Loading roadmaps..." />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      {/* Header */}
      <View className="bg-white px-6 py-4 border-b border-gray-200">
        <Text className="text-2xl font-bold text-gray-900">Learning Roadmaps</Text>
        <Text className="text-sm text-gray-500 mt-1">
          Structured learning paths to master new skills
        </Text>
      </View>

      <SearchBar
        value={searchQuery}
        onChangeText={setSearchQuery}
        placeholder="Search roadmaps..."
      />

      {/* Category Chips */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        className="bg-white px-4 py-3 border-b border-gray-200"
      >
        {categories.map((category) => (
          <TouchableOpacity
            key={category}
            onPress={() => setSelectedCategory(category)}
            className={`px-4 py-2 rounded-full mr-2 ${
              selectedCategory === category
                ? 'bg-blue-500'
                : 'bg-gray-100'
            }`}
          >
            <Text
              className={`text-sm font-semibold ${
                selectedCategory === category ? 'text-white' : 'text-gray-700'
              }`}
            >
              {category}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {/* Filter Bar */}
      <View className="bg-white px-6 py-3 border-b border-gray-200 flex-row items-center justify-between">
        <Text className="text-sm text-gray-600">
          {filteredData?.length || 0} roadmaps
        </Text>
        <TouchableOpacity
          onPress={() => setShowFilters(!showFilters)}
          className="flex-row items-center"
        >
          <Ionicons name="filter-outline" size={20} color="#3b82f6" />
          <Text className="text-blue-500 font-semibold ml-2">Filters</Text>
        </TouchableOpacity>
      </View>

      {/* Filters Panel */}
      {showFilters && (
        <View className="bg-white px-6 py-4 border-b border-gray-200">
          <View className="mb-4">
            <Text className="text-sm font-semibold text-gray-700 mb-2">Difficulty</Text>
            <View className="flex-row space-x-2">
              {['all', 'Beginner', 'Intermediate', 'Advanced'].map((diff) => (
                <TouchableOpacity
                  key={diff}
                  onPress={() => setFilters({...filters, difficulty: diff})}
                  className={`px-3 py-2 rounded-lg ${
                    filters.difficulty === diff ? 'bg-blue-500' : 'bg-gray-100'
                  }`}
                >
                  <Text className={`text-xs font-semibold ${
                    filters.difficulty === diff ? 'text-white' : 'text-gray-700'
                  }`}>
                    {diff === 'all' ? 'All' : diff}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          <View className="mb-4">
            <Text className="text-sm font-semibold text-gray-700 mb-2">Duration</Text>
            <View className="flex-row space-x-2">
              {['all', '<3 months', '3-6 months', '6+ months'].map((dur) => (
                <TouchableOpacity
                  key={dur}
                  onPress={() => setFilters({...filters, duration: dur})}
                  className={`px-3 py-2 rounded-lg ${
                    filters.duration === dur ? 'bg-blue-500' : 'bg-gray-100'
                  }`}
                >
                  <Text className={`text-xs font-semibold ${
                    filters.duration === dur ? 'text-white' : 'text-gray-700'
                  }`}>
                    {dur === 'all' ? 'All' : dur}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          <View>
            <Text className="text-sm font-semibold text-gray-700 mb-2">Status</Text>
            <View className="flex-row space-x-2">
              {[
                {key: 'all', label: 'All'},
                {key: 'not_started', label: 'Not Started'},
                {key: 'in_progress', label: 'In Progress'},
                {key: 'completed', label: 'Completed'}
              ].map((status) => (
                <TouchableOpacity
                  key={status.key}
                  onPress={() => setFilters({...filters, status: status.key})}
                  className={`px-3 py-2 rounded-lg ${
                    filters.status === status.key ? 'bg-blue-500' : 'bg-gray-100'
                  }`}
                >
                  <Text className={`text-xs font-semibold ${
                    filters.status === status.key ? 'text-white' : 'text-gray-700'
                  }`}>
                    {status.label}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </View>

          <TouchableOpacity
            onPress={() => setFilters({ difficulty: 'all', duration: 'all', status: 'all' })}
            className="mt-4 bg-gray-100 py-2 rounded-lg items-center"
          >
            <Text className="text-gray-700 font-semibold">Reset Filters</Text>
          </TouchableOpacity>
        </View>
      )}

      <ScrollView
        className="flex-1"
        refreshControl={
          <RefreshControl refreshing={isFetching} onRefresh={refetch} />
        }
      >
        {filteredData && filteredData.length === 0 ? (
          <EmptyState
            icon="map-outline"
            title="No Roadmaps Found"
            message="No roadmaps match your criteria. Try adjusting filters!"
          />
        ) : (
          <View className="px-4 py-4 space-y-4">
            {filteredData?.map((roadmap: Roadmap) => {
              const progress = getRoadmapProgress(roadmap);
              return (
                <TouchableOpacity
                  key={roadmap._id}
                  className="bg-white rounded-xl p-5 shadow-sm border border-gray-200"
                  onPress={() => router.push(`/roadmaps/${roadmap._id}`)}
                >
                  {/* Header */}
                  <View className="flex-row items-start justify-between mb-3">
                    <View className="flex-1 mr-3">
                      <Text className="text-lg font-bold text-gray-900" numberOfLines={2}>
                        {roadmap.title}
                      </Text>
                      <Text className="text-sm text-gray-500 mt-1">
                        {roadmap.subcategory || roadmap.category}
                      </Text>
                    </View>
                    <View className={`px-3 py-1 rounded-full ${difficultyColors[roadmap.difficulty_level as keyof typeof difficultyColors] || 'bg-gray-100 text-gray-700'}`}>
                      <Text className="text-xs font-semibold">{roadmap.difficulty_level}</Text>
                    </View>
                  </View>

                  {/* Description */}
                  <Text className="text-gray-600 text-sm mb-4" numberOfLines={2}>
                    {roadmap.description}
                  </Text>

                  {/* Progress Bar */}
                  <View className="mb-3">
                    <View className="flex-row justify-between mb-1">
                      <Text className="text-xs text-gray-500">Progress</Text>
                      <Text className="text-xs font-semibold text-blue-600">{progress}%</Text>
                    </View>
                    <View className="h-2 bg-gray-200 rounded-full overflow-hidden">
                      <View 
                        className="h-full bg-blue-500 rounded-full" 
                        style={{ width: `${progress}%` }}
                      />
                    </View>
                  </View>

                  {/* Footer Stats */}
                  <View className="flex-row items-center justify-between pt-3 border-t border-gray-100">
                    <View className="flex-row items-center">
                      <Ionicons name="time-outline" size={16} color="#6b7280" />
                      <Text className="text-xs text-gray-500 ml-1">
                        {roadmap.estimated_duration} hours
                      </Text>
                    </View>
                    <View className="flex-row items-center">
                      <Ionicons name="git-network-outline" size={16} color="#6b7280" />
                      <Text className="text-xs text-gray-500 ml-1">
                        {roadmap.nodes?.length || 0} topics
                      </Text>
                    </View>
                    <View className="flex-row items-center">
                      <Ionicons name="arrow-forward-circle" size={20} color="#3b82f6" />
                      <Text className="text-xs font-semibold text-blue-600 ml-1">Start</Text>
                    </View>
                  </View>
                </TouchableOpacity>
              );
            })}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
