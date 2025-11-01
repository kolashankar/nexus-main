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
import Slider from '@react-native-community/slider';

export interface ScholarshipFilters {
  educationLevels: string[];
  countries: string[];
  amountMin: number;
  amountMax: number;
  deadline: string;
}

interface ScholarshipsFilterModalProps {
  visible: boolean;
  onClose: () => void;
  onApply: (filters: ScholarshipFilters) => void;
  currentFilters: ScholarshipFilters;
}

const EDUCATION_LEVELS = ['Undergraduate', 'Graduate', 'PhD', 'Postdoctoral'];
const COUNTRIES = ['USA', 'UK', 'Canada', 'India', 'Germany', 'Australia', 'All'];
const DEADLINE_OPTIONS = [
  { label: 'Any Time', value: '' },
  { label: 'This Month', value: '30d' },
  { label: 'Next 3 Months', value: '90d' },
  { label: 'Next 6 Months', value: '180d' },
];

export default function ScholarshipsFilterModal({
  visible,
  onClose,
  onApply,
  currentFilters,
}: ScholarshipsFilterModalProps) {
  const [filters, setFilters] = useState<ScholarshipFilters>(currentFilters);

  const toggleEducationLevel = (level: string) => {
    setFilters((prev) => ({
      ...prev,
      educationLevels: prev.educationLevels.includes(level)
        ? prev.educationLevels.filter((l) => l !== level)
        : [...prev.educationLevels, level],
    }));
  };

  const toggleCountry = (country: string) => {
    setFilters((prev) => ({
      ...prev,
      countries: prev.countries.includes(country)
        ? prev.countries.filter((c) => c !== country)
        : [...prev.countries, country],
    }));
  };

  const handleApply = () => {
    onApply(filters);
    onClose();
  };

  const handleReset = () => {
    const resetFilters: ScholarshipFilters = {
      educationLevels: [],
      countries: [],
      amountMin: 0,
      amountMax: 100000,
      deadline: '',
    };
    setFilters(resetFilters);
  };

  return (
    <Modal visible={visible} animationType="slide" transparent>
      <View className="flex-1 bg-black/50">
        <View className="flex-1 mt-20 bg-dark-400 rounded-t-3xl">
          {/* Header */}
          <View className="flex-row justify-between items-center px-6 py-4 border-b border-gray-700">
            <Text className="text-white text-xl font-bold">Filters</Text>
            <TouchableOpacity onPress={onClose}>
              <Ionicons name="close" size={24} color="#fff" />
            </TouchableOpacity>
          </View>

          <ScrollView className="flex-1 px-6 py-4">
            {/* Education Level */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">
                Education Level
              </Text>
              <View className="flex-row flex-wrap">
                {EDUCATION_LEVELS.map((level) => (
                  <TouchableOpacity
                    key={level}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.educationLevels.includes(level)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleEducationLevel(level)}
                  >
                    <Text
                      className={`${
                        filters.educationLevels.includes(level)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {level}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Country */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Country</Text>
              <View className="flex-row flex-wrap">
                {COUNTRIES.map((country) => (
                  <TouchableOpacity
                    key={country}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.countries.includes(country)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleCountry(country)}
                  >
                    <Text
                      className={`${
                        filters.countries.includes(country)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {country}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Amount Range */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Amount Range</Text>
              <View className="bg-dark-200 rounded-lg p-4">
                <View className="flex-row justify-between mb-2">
                  <Text className="text-gray-400">
                    ${filters.amountMin.toLocaleString()}
                  </Text>
                  <Text className="text-gray-400">
                    ${filters.amountMax.toLocaleString()}
                  </Text>
                </View>
                <Slider
                  minimumValue={0}
                  maximumValue={100000}
                  step={1000}
                  value={filters.amountMin}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, amountMin: value }))
                  }
                  minimumTrackTintColor="#3b82f6"
                  maximumTrackTintColor="#374151"
                  thumbTintColor="#3b82f6"
                />
                <Text className="text-gray-400 text-sm mt-2">Maximum</Text>
                <Slider
                  minimumValue={0}
                  maximumValue={100000}
                  step={1000}
                  value={filters.amountMax}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, amountMax: value }))
                  }
                  minimumTrackTintColor="#3b82f6"
                  maximumTrackTintColor="#374151"
                  thumbTintColor="#3b82f6"
                />
              </View>
            </View>

            {/* Deadline */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">
                Application Deadline
              </Text>
              <View className="flex-row flex-wrap">
                {DEADLINE_OPTIONS.map((option) => (
                  <TouchableOpacity
                    key={option.value}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.deadline === option.value
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() =>
                      setFilters((prev) => ({ ...prev, deadline: option.value }))
                    }
                  >
                    <Text
                      className={`${
                        filters.deadline === option.value ? 'text-white' : 'text-gray-400'
                      }`}
                    >
                      {option.label}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          </ScrollView>

          {/* Footer Actions */}
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
