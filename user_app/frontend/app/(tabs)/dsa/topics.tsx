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

interface DSATopic {
  _id: string;
  name: string;
  description: string;
  icon: string;
  color: string;
  question_count: number;
}

export default function TopicsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['dsa-topics', searchQuery],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      
      const response = await api.get('/admin/dsa/topics', { params });
      return response.data.topics || [];
    },
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading topics..." />
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Topics"
          message="Failed to load topics. Please try again."
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
        <Text className="text-white text-xl font-bold">DSA Topics</Text>
      </View>

      <SearchBar
        value={searchQuery}
        onChangeText={setSearchQuery}
        placeholder="Search topics..."
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
            icon="list-outline"
            title="No Topics Found"
            message="No topics available. Check back later!"
          />
        ) : (
          <View className="flex-row flex-wrap justify-between">
            {data?.map((topic: DSATopic) => (
              <TouchableOpacity
                key={topic._id}
                className="bg-dark-200 rounded-lg p-4 mb-3"
                style={{ width: '48%' }}
              >
                <View className="items-center">
                  <View className="bg-primary-600 w-12 h-12 rounded-full items-center justify-center mb-3">
                    <Text className="text-2xl">{topic.icon}</Text>
                  </View>
                  <Text className="text-white text-base font-bold text-center" numberOfLines={1}>
                    {topic.name}
                  </Text>
                  <Text className="text-gray-400 text-xs text-center mt-1" numberOfLines={2}>
                    {topic.description}
                  </Text>
                  <View className="bg-dark-300 px-3 py-1 rounded-full mt-3">
                    <Text className="text-gray-300 text-xs">
                      {topic.question_count} problems
                    </Text>
                  </View>
                </View>
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}