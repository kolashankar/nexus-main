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

interface DSASheet {
  _id: string;
  name: string;
  description: string;
  level: string;
  tags: string[];
  questions: any[];
  difficulty_breakdown: {
    Easy: number;
    Medium: number;
    Hard: number;
  };
  is_published: boolean;
}

export default function SheetsScreen() {
  const [searchQuery, setSearchQuery] = useState('');
  const router = useRouter();

  const { data, isLoading, isError, refetch, isFetching } = useQuery({
    queryKey: ['dsa-sheets', searchQuery],
    queryFn: async () => {
      const params: any = {};
      if (searchQuery) params.search = searchQuery;
      
      const response = await api.get('/admin/dsa/sheets', { params });
      return response.data.sheets || [];
    },
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading sheets..." />
      </SafeAreaView>
    );
  }

  if (isError) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Sheets"
          message="Failed to load sheets. Please try again."
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
        <Text className="text-white text-xl font-bold">DSA Sheets</Text>
      </View>

      <SearchBar
        value={searchQuery}
        onChangeText={setSearchQuery}
        placeholder="Search sheets..."
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
            icon="document-text-outline"
            title="No Sheets Found"
            message="No problem sheets available. Check back later!"
          />
        ) : (
          data?.map((sheet: DSASheet) => (
            <TouchableOpacity
              key={sheet._id}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => router.push(`/(tabs)/dsa/sheet-${sheet._id}`)}
            >
              <View className="flex-row justify-between items-start mb-2">
                <View className="flex-1">
                  <Text className="text-white text-lg font-bold" numberOfLines={1}>
                    {sheet.name}
                  </Text>
                  <Text className="text-gray-400 text-sm mt-1" numberOfLines={2}>
                    {sheet.description}
                  </Text>
                </View>
                <View className="bg-purple-600 px-3 py-1 rounded-full ml-2">
                  <Text className="text-white text-xs font-semibold">{sheet.level}</Text>
                </View>
              </View>

              <View className="flex-row items-center mt-3">
                <View className="flex-row items-center mr-4">
                  <Ionicons name="list-outline" size={16} color="#9ca3af" />
                  <Text className="text-gray-400 text-sm ml-1">
                    {sheet.questions?.length || 0} problems
                  </Text>
                </View>
                {sheet.difficulty_breakdown && (
                  <View className="flex-row items-center">
                    <View className="flex-row items-center mr-2">
                      <View className="bg-green-600 w-2 h-2 rounded-full mr-1" />
                      <Text className="text-gray-400 text-xs">{sheet.difficulty_breakdown.Easy}</Text>
                    </View>
                    <View className="flex-row items-center mr-2">
                      <View className="bg-yellow-600 w-2 h-2 rounded-full mr-1" />
                      <Text className="text-gray-400 text-xs">{sheet.difficulty_breakdown.Medium}</Text>
                    </View>
                    <View className="flex-row items-center">
                      <View className="bg-red-600 w-2 h-2 rounded-full mr-1" />
                      <Text className="text-gray-400 text-xs">{sheet.difficulty_breakdown.Hard}</Text>
                    </View>
                  </View>
                )}
              </View>

              {sheet.tags && sheet.tags.length > 0 && (
                <View className="flex-row flex-wrap mt-3">
                  {sheet.tags.slice(0, 3).map((tag, index) => (
                    <View key={index} className="bg-dark-300 px-2 py-1 rounded mr-2 mb-2">
                      <Text className="text-gray-400 text-xs">#{tag}</Text>
                    </View>
                  ))}
                </View>
              )}
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}