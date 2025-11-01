import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface SearchHistoryProps {
  history: Array<{ query: string; timestamp: number }>;
  onSelectQuery: (query: string) => void;
  onClearHistory: () => void;
  onRemoveItem: (query: string) => void;
}

export default function SearchHistory({
  history,
  onSelectQuery,
  onClearHistory,
  onRemoveItem,
}: SearchHistoryProps) {
  if (history.length === 0) return null;

  return (
    <View className="bg-gray-800 rounded-lg p-4 mb-4">
      <View className="flex-row justify-between items-center mb-3">
        <Text className="text-white font-semibold text-base">
          Recent Searches
        </Text>
        <TouchableOpacity onPress={onClearHistory}>
          <Text className="text-blue-400 text-sm">Clear All</Text>
        </TouchableOpacity>
      </View>
      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
        <View className="flex-row gap-2">
          {history.map((item, index) => (
            <TouchableOpacity
              key={index}
              onPress={() => onSelectQuery(item.query)}
              className="bg-gray-700 rounded-full px-4 py-2 flex-row items-center"
            >
              <Ionicons name="time-outline" size={14} color="#9ca3af" />
              <Text className="text-gray-300 text-sm ml-1">{item.query}</Text>
              <TouchableOpacity
                onPress={(e) => {
                  e.stopPropagation();
                  onRemoveItem(item.query);
                }}
                className="ml-2"
              >
                <Ionicons name="close" size={14} color="#9ca3af" />
              </TouchableOpacity>
            </TouchableOpacity>
          ))}
        </View>
      </ScrollView>
    </View>
  );
}
