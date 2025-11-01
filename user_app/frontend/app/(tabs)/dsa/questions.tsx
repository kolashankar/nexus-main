import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import SearchBar from '../../../components/common/SearchBar';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';

interface DSAQuestion {
  _id: string;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  topics: string[];
  companies: string[];
  description: string;
}

export default function QuestionsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('');
  const router = useRouter();

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['dsa-questions', searchQuery, difficultyFilter],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      if (difficultyFilter) params.difficulty = difficultyFilter;
      
      const response = await api.get('/admin/dsa/questions', { params });
      return response.data.questions || [];
    },
  });

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'bg-green-600';
      case 'Medium': return 'bg-yellow-600';
      case 'Hard': return 'bg-red-600';
      default: return 'bg-gray-600';
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading questions..." />
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Questions"
          message="Failed to load questions. Please try again."
        />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center px-6 py-4">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text className="text-white text-xl font-bold">DSA Questions</Text>
      </View>

      <SearchBar
        value={searchQuery}
        onChangeText={setSearchQuery}
        placeholder="Search questions..."
      />

      {/* Difficulty Filter */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} className="px-4 mb-4">
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            difficultyFilter === '' ? 'bg-primary-600' : 'bg-dark-200'
          }`}
          onPress={() => setDifficultyFilter('')}
        >
          <Text className="text-white font-semibold">All</Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            difficultyFilter === 'Easy' ? 'bg-green-600' : 'bg-dark-200'
          }`}
          onPress={() => setDifficultyFilter('Easy')}
        >
          <Text className="text-white font-semibold">Easy</Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            difficultyFilter === 'Medium' ? 'bg-yellow-600' : 'bg-dark-200'
          }`}
          onPress={() => setDifficultyFilter('Medium')}
        >
          <Text className="text-white font-semibold">Medium</Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full ${
            difficultyFilter === 'Hard' ? 'bg-red-600' : 'bg-dark-200'
          }`}
          onPress={() => setDifficultyFilter('Hard')}
        >
          <Text className="text-white font-semibold">Hard</Text>
        </TouchableOpacity>
      </ScrollView>

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
            icon="code-slash-outline"
            title="No Questions Found"
            message="No questions available. Try adjusting your filters!"
          />
        ) : (
          data?.map((question: DSAQuestion) => (
            <TouchableOpacity
              key={question._id}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => router.push(`/(tabs)/dsa/question-${question._id}`)}
            >
              <View className="flex-row justify-between items-start mb-2">
                <View className="flex-1">
                  <Text className="text-white text-lg font-bold" numberOfLines={2}>
                    {question.title}
                  </Text>
                </View>
                <View className={`${getDifficultyColor(question.difficulty)} px-3 py-1 rounded-full ml-2`}>
                  <Text className="text-white text-xs font-semibold">
                    {question.difficulty}
                  </Text>
                </View>
              </View>

              <Text className="text-gray-300 text-sm mt-2" numberOfLines={2}>
                {question.description}
              </Text>

              <View className="flex-row flex-wrap mt-3">
                {question.topics.slice(0, 3).map((topic, index) => (
                  <View key={index} className="bg-primary-600 px-2 py-1 rounded mr-2 mb-2">
                    <Text className="text-white text-xs">{topic}</Text>
                  </View>
                ))}
              </View>

              {question.companies && question.companies.length > 0 && (
                <View className="flex-row items-center mt-2">
                  <Ionicons name="business-outline" size={14} color="#9ca3af" />
                  <Text className="text-gray-400 text-xs ml-1">
                    {question.companies.slice(0, 3).join(', ')}
                  </Text>
                </View>
              )}
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}