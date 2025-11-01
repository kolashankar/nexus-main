import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';

interface CategoryChipsProps {
  categories: string[];
  selectedCategory: string;
  onSelectCategory: (category: string) => void;
}

export default function CategoryChips({
  categories,
  selectedCategory,
  onSelectCategory,
}: CategoryChipsProps) {
  return (
    <ScrollView
      horizontal
      showsHorizontalScrollIndicator={false}
      className="px-4 py-2"
      contentContainerStyle={{ paddingRight: 16 }}
    >
      {categories.map((category) => (
        <TouchableOpacity
          key={category}
          className={`px-4 py-2 rounded-full mr-2 ${
            selectedCategory === category
              ? 'bg-primary-600'
              : 'bg-dark-200 border border-gray-700'
          }`}
          onPress={() => onSelectCategory(category)}
        >
          <Text
            className={`font-semibold ${
              selectedCategory === category ? 'text-white' : 'text-gray-400'
            }`}
          >
            {category}
          </Text>
        </TouchableOpacity>
      ))}
    </ScrollView>
  );
}
