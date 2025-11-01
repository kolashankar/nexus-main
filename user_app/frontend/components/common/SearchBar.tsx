import React from 'react';
import { View, TextInput, TouchableOpacity } from 'react-native';
import { Ionicons } from '@expo/vector-icons';

interface SearchBarProps {
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  onFilter?: () => void;
}

export default function SearchBar({
  value,
  onChangeText,
  placeholder = 'Search...',
  onFilter,
}: SearchBarProps) {
  return (
    <View className="flex-row items-center px-4 mb-4">
      <View className="flex-1 bg-dark-200 rounded-lg px-4 py-3 flex-row items-center">
        <Ionicons name="search" size={20} color="#9ca3af" />
        <TextInput
          className="flex-1 text-white ml-3"
          placeholder={placeholder}
          placeholderTextColor="#6b7280"
          value={value}
          onChangeText={onChangeText}
        />
      </View>
      {onFilter && (
        <TouchableOpacity
          className="bg-primary-600 rounded-lg p-3 ml-2"
          onPress={onFilter}
        >
          <Ionicons name="filter" size={20} color="#fff" />
        </TouchableOpacity>
      )}
    </View>
  );
}