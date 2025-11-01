import React from 'react';
import { View, Text } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface EmptyStateProps {
  icon: keyof typeof Ionicons.glyphMap;
  title: string;
  message: string;
}

export default function EmptyState({ icon, title, message }: EmptyStateProps) {
  return (
    <View className="flex-1 items-center justify-center px-6">
      <Ionicons name={icon} size={64} color="#4b5563" />
      <Text className="text-white text-xl font-bold mt-4">{title}</Text>
      <Text className="text-gray-400 text-center mt-2">{message}</Text>
    </View>
  );
}