import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '@/lib/api';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

interface UsageItem {
  _id: string;
  tool_type: string;
  created_at: string;
  input_data: any;
  output_data: any;
}

const TOOL_COLORS = {
  'resume_review': 'bg-blue-500',
  'cover_letter': 'bg-green-500',
  'ats_hack': 'bg-purple-500',
  'cold_email': 'bg-orange-500'
};

const TOOL_ICONS = {
  'resume_review': 'document-text',
  'cover_letter': 'mail',
  'ats_hack': 'shield-checkmark',
  'cold_email': 'send'
};

export default function UsageHistoryScreen() {
  const [selectedTool, setSelectedTool] = useState('all');

  const { data: usageData, isLoading, refetch, isFetching } = useQuery({
    queryKey: ['career-tools-usage'],
    queryFn: async () => {
      const response = await api.get('/career-tools/my-usage');
      return response.data.usage_history || [];
    }
  });

  const filteredData = selectedTool === 'all'
    ? usageData
    : usageData?.filter((item: UsageItem) => item.tool_type === selectedTool);

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-gray-50">
        <LoadingSpinner message="Loading usage history..." />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      {/* Header */}
      <View className="bg-white px-6 py-4 border-b border-gray-200 flex-row items-center">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#000" />
        </TouchableOpacity>
        <View className="flex-1">
          <Text className="text-xl font-bold text-gray-900">Usage History</Text>
          <Text className="text-sm text-gray-500">
            {filteredData?.length || 0} items
          </Text>
        </View>
      </View>

      {/* Filter Chips */}
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        className="bg-white px-4 py-3 border-b border-gray-200"
      >
        {['all', 'resume_review', 'cover_letter', 'ats_hack', 'cold_email'].map((tool) => (
          <TouchableOpacity
            key={tool}
            onPress={() => setSelectedTool(tool)}
            className={`px-4 py-2 rounded-full mr-2 ${
              selectedTool === tool ? 'bg-blue-500' : 'bg-gray-100'
            }`}
          >
            <Text
              className={`text-sm font-semibold ${
                selectedTool === tool ? 'text-white' : 'text-gray-700'
              }`}
            >
              {tool === 'all'
                ? 'All'
                : tool.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <ScrollView
        className="flex-1"
        refreshControl={
          <RefreshControl refreshing={isFetching} onRefresh={refetch} />
        }
      >
        {filteredData && filteredData.length === 0 ? (
          <EmptyState
            icon="time-outline"
            title="No Usage History"
            message="Your AI-generated content will appear here"
          />
        ) : (
          <View className="px-4 py-4">
            {filteredData?.map((item: UsageItem) => {
              const toolColor = TOOL_COLORS[item.tool_type as keyof typeof TOOL_COLORS] || 'bg-gray-500';
              const toolIcon = TOOL_ICONS[item.tool_type as keyof typeof TOOL_ICONS] || 'sparkles';
              const date = new Date(item.created_at);
              
              return (
                <View
                  key={item._id}
                  className="bg-white rounded-xl p-5 mb-4 border border-gray-200"
                >
                  {/* Header */}
                  <View className="flex-row items-start mb-3">
                    <View className={`${toolColor} w-12 h-12 rounded-lg items-center justify-center mr-3`}>
                      <Ionicons name={toolIcon as any} size={24} color="#fff" />
                    </View>
                    <View className="flex-1">
                      <Text className="text-base font-bold text-gray-900 mb-1">
                        {item.tool_type.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                      </Text>
                      <Text className="text-xs text-gray-500">
                        {date.toLocaleDateString()} at {date.toLocaleTimeString()}
                      </Text>
                    </View>
                  </View>

                  {/* Preview */}
                  <Text className="text-gray-700 text-sm leading-5 mb-3" numberOfLines={3}>
                    {JSON.stringify(item.output_data).substring(0, 150)}...
                  </Text>

                  {/* Actions */}
                  <View className="flex-row space-x-2">
                    <TouchableOpacity className="flex-1 bg-gray-100 py-2 rounded-lg items-center">
                      <Text className="text-gray-700 font-semibold text-sm">View</Text>
                    </TouchableOpacity>
                    <TouchableOpacity className="flex-1 bg-gray-100 py-2 rounded-lg items-center">
                      <Text className="text-gray-700 font-semibold text-sm">Re-use</Text>
                    </TouchableOpacity>
                    <TouchableOpacity className="bg-red-100 px-4 py-2 rounded-lg items-center">
                      <Ionicons name="trash-outline" size={18} color="#ef4444" />
                    </TouchableOpacity>
                  </View>
                </View>
              );
            })}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
