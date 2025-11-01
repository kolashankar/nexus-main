import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';

export default function ArticleDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();

  const { data: article, isLoading, isError } = useQuery({
    queryKey: ['article', id],
    queryFn: async () => {
      const response = await api.get(`/user/articles/${id}`);
      return response.data.article;
    },
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <View className="flex-1 items-center justify-center">
          <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      </SafeAreaView>
    );
  }

  if (isError || !article) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <View className="flex-1 items-center justify-center px-6">
          <Ionicons name="alert-circle-outline" size={64} color="#4b5563" />
          <Text className="text-white text-xl font-bold mt-4">Article Not Found</Text>
          <TouchableOpacity
            className="bg-primary-600 px-6 py-3 rounded-lg mt-4"
            onPress={() => router.back()}
          >
            <Text className="text-white font-semibold">Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center px-6 py-4 border-b border-dark-200">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text className="text-white text-lg font-bold flex-1" numberOfLines={1}>
          Article
        </Text>
        <TouchableOpacity>
          <Ionicons name="bookmark-outline" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <ScrollView className="flex-1">
        {/* Article Header */}
        <View className="px-6 py-6 border-b border-dark-200">
          <Text className="text-white text-2xl font-bold mb-3">{article.title}</Text>
          
          <View className="flex-row items-center justify-between mb-4">
            <View>
              <Text className="text-gray-400 text-sm">By {article.author}</Text>
              <Text className="text-gray-500 text-xs mt-1">
                {new Date(article.created_at).toLocaleDateString()}
              </Text>
            </View>
            <View className="flex-row items-center">
              <Ionicons name="time-outline" size={16} color="#9ca3af" />
              <Text className="text-gray-400 text-sm ml-1">{article.read_time} min</Text>
            </View>
          </View>

          <View className="flex-row flex-wrap">
            <View className="bg-primary-600 px-3 py-1 rounded-full mr-2 mb-2">
              <Text className="text-white text-sm font-semibold">{article.category}</Text>
            </View>
            {article.tags.slice(0, 3).map((tag: string, index: number) => (
              <View key={index} className="bg-dark-300 px-3 py-1 rounded-full mr-2 mb-2">
                <Text className="text-gray-300 text-sm">#{tag}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Article Content */}
        <View className="px-6 py-6">
          <Text className="text-gray-300 text-base leading-7">
            {article.content}
          </Text>
        </View>

        {/* Stats */}
        <View className="px-6 py-6 border-t border-dark-200 mb-6">
          <View className="flex-row items-center justify-between">
            <View className="flex-row items-center">
              <Ionicons name="eye-outline" size={20} color="#9ca3af" />
              <Text className="text-gray-400 ml-2">{article.views_count} views</Text>
            </View>
            <TouchableOpacity className="bg-primary-600 px-4 py-2 rounded-lg">
              <Text className="text-white font-semibold">Share</Text>
            </TouchableOpacity>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}