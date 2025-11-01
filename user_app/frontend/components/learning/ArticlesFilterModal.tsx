import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  Modal,
  ScrollView,
  TextInput,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';

export interface ArticleFilters {
  categories: string[];
  tags: string[];
  author: string;
  readTime: string;
}

interface ArticlesFilterModalProps {
  visible: boolean;
  onClose: () => void;
  onApply: (filters: ArticleFilters) => void;
  currentFilters: ArticleFilters;
  availableTags: string[];
}

const CATEGORIES = [
  'Career Growth',
  'Technical Skills',
  'Interview Preparation',
  'Resume Writing',
  'Soft Skills',
  'Industry Insights',
];

const READ_TIME_OPTIONS = [
  { label: 'Any Duration', value: '' },
  { label: '< 5 minutes', value: '5' },
  { label: '5-10 minutes', value: '10' },
  { label: '10+ minutes', value: '15' },
];

export default function ArticlesFilterModal({
  visible,
  onClose,
  onApply,
  currentFilters,
  availableTags,
}: ArticlesFilterModalProps) {
  const [filters, setFilters] = useState<ArticleFilters>(currentFilters);

  const toggleCategory = (category: string) => {
    setFilters((prev) => ({
      ...prev,
      categories: prev.categories.includes(category)
        ? prev.categories.filter((c) => c !== category)
        : [...prev.categories, category],
    }));
  };

  const toggleTag = (tag: string) => {
    setFilters((prev) => ({
      ...prev,
      tags: prev.tags.includes(tag)
        ? prev.tags.filter((t) => t !== tag)
        : [...prev.tags, tag],
    }));
  };

  const handleApply = () => {
    onApply(filters);
    onClose();
  };

  const handleReset = () => {
    const resetFilters: ArticleFilters = {
      categories: [],
      tags: [],
      author: '',
      readTime: '',
    };
    setFilters(resetFilters);
  };

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View className="flex-1 bg-black/50">
        <View className="flex-1 mt-20 bg-dark-400 rounded-t-3xl">
          <View className="flex-row justify-between items-center px-6 py-4 border-b border-gray-700">
            <Text className="text-white text-xl font-bold">Filters</Text>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color="#fff" />
            </TouchableOpacity>
          </View>

          <ScrollView className="flex-1 px-6 py-4">
            {/* Category */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Category</Text>
              <View className="flex-row flex-wrap">
                {CATEGORIES.map((category) => (
                  <TouchableOpacity
                    key={category}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.categories.includes(category)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleCategory(category)}
                  >
                    <Text
                      className={`${
                        filters.categories.includes(category)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {category}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Tags */}
            {availableTags.length > 0 && (
              <View className="mb-6">
                <Text className="text-white text-lg font-semibold mb-3">Tags</Text>
                <View className="flex-row flex-wrap">
                  {availableTags.slice(0, 15).map((tag) => (
                    <TouchableOpacity
                      key={tag}
                      className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                        filters.tags.includes(tag)
                          ? 'bg-primary-600'
                          : 'bg-dark-200 border border-gray-700'
                      }`}
                      onPress={() => toggleTag(tag)}
                    >
                      <Text
                        className={`${
                          filters.tags.includes(tag) ? 'text-white' : 'text-gray-400'
                        }`}
                      >
                        {tag}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>
            )}

            {/* Author */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Author</Text>
              <TextInput
                className="bg-dark-200 text-white px-4 py-3 rounded-lg"
                placeholder="Search by author..."
                placeholderTextColor="#9ca3af"
                value={filters.author}
                onChangeText={(text) => setFilters((prev) => ({ ...prev, author: text }))}
              />
            </View>

            {/* Read Time */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Read Time</Text>
              <View className="flex-row flex-wrap">
                {READ_TIME_OPTIONS.map((option) => (
                  <TouchableOpacity
                    key={option.value}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.readTime === option.value
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() =>
                      setFilters((prev) => ({ ...prev, readTime: option.value }))
                    }
                  >
                    <Text
                      className={`${
                        filters.readTime === option.value ? 'text-white' : 'text-gray-400'
                      }`}
                    >
                      {option.label}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </ScrollView>

          <View className="flex-row px-6 py-4 border-t border-gray-700">
            <TouchableOpacity
              className="flex-1 bg-dark-200 py-4 rounded-lg mr-2"
              onPress={handleReset}
            >
              <Text className="text-white text-center font-semibold">Reset</Text>
            </TouchableOpacity>
            <TouchableOpacity
              className="flex-1 bg-primary-600 py-4 rounded-lg ml-2"
              onPress={handleApply}
            >
              <Text className="text-white text-center font-semibold">Apply Filters</Text>
            </TouchableOpacity>
          </View>
        </View>
      </View>
    </Modal>
  );
}
