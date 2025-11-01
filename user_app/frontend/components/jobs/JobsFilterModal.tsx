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

export interface JobFilters {
  jobTypes: string[];
  experienceLevels: string[];
  salaryMin: number;
  salaryMax: number;
  location: string;
  postedDate: string;
}

interface JobsFilterModalProps {
  visible: boolean;
  onClose: () => void;
  onApply: (filters: JobFilters) => void;
  currentFilters: JobFilters;
}

const JOB_TYPES = ['Full-time', 'Part-time', 'Contract', 'Remote', 'Hybrid'];
const EXPERIENCE_LEVELS = ['Entry', 'Mid', 'Senior', 'Lead', 'Executive'];
const POSTED_OPTIONS = [
  { label: 'Any Time', value: '' },
  { label: 'Last 24 Hours', value: '1d' },
  { label: 'Last Week', value: '7d' },
  { label: 'Last Month', value: '30d' },
];

export default function JobsFilterModal({
  visible,
  onClose,
  onApply,
  currentFilters,
}: JobsFilterModalProps) {
  const [filters, setFilters] = useState<JobFilters>(currentFilters);

  const toggleJobType = (type: string) => {
    setFilters((prev) => ({
      ...prev,
      jobTypes: prev.jobTypes.includes(type)
        ? prev.jobTypes.filter((t) => t !== type)
        : [...prev.jobTypes, type],
    }));
  };

  const toggleExperienceLevel = (level: string) => {
    setFilters((prev) => ({
      ...prev,
      experienceLevels: prev.experienceLevels.includes(level)
        ? prev.experienceLevels.filter((l) => l !== level)
        : [...prev.experienceLevels, level],
    }));
  };

  const handleApply = () => {
    onApply(filters);
    onClose();
  };

  const handleReset = () => {
    const resetFilters: JobFilters = {
      jobTypes: [],
      experienceLevels: [],
      salaryMin: 0,
      salaryMax: 200000,
      location: '',
      postedDate: '',
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
            {/* Job Type */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Job Type</Text>
              <View className="flex-row flex-wrap">
                {JOB_TYPES.map((type) => (
                  <TouchableOpacity
                    key={type}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.jobTypes.includes(type)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleJobType(type)}
                  >
                    <Text
                      className={`${
                        filters.jobTypes.includes(type) ? 'text-white' : 'text-gray-400'
                      }`}
                    >
                      {type}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Experience Level */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">
                Experience Level
              </Text>
              <View className="flex-row flex-wrap">
                {EXPERIENCE_LEVELS.map((level) => (
                  <TouchableOpacity
                    key={level}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.experienceLevels.includes(level)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleExperienceLevel(level)}
                  >
                    <Text
                      className={`${
                        filters.experienceLevels.includes(level)
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

            {/* Salary Range */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Salary Range</Text>
              <View className="bg-dark-200 rounded-lg p-4">
                <View className="flex-row justify-between mb-2">
                  <Text className="text-gray-400">
                    ${filters.salaryMin.toLocaleString()}
                  </Text>
                  <Text className="text-gray-400">
                    ${filters.salaryMax.toLocaleString()}
                  </Text>
                </View>
                <Slider
                  minimumValue={0}
                  maximumValue={200000}
                  step={5000}
                  value={filters.salaryMin}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, salaryMin: value }))
                  }
                  minimumTrackTintColor="#3b82f6"
                  maximumTrackTintColor="#374151"
                  thumbTintColor="#3b82f6"
                />
                <Text className="text-gray-400 text-sm mt-2">Maximum</Text>
                <Slider
                  minimumValue={0}
                  maximumValue={200000}
                  step={5000}
                  value={filters.salaryMax}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, salaryMax: value }))
                  }
                  minimumTrackTintColor="#3b82f6"
                  maximumTrackTintColor="#374151"
                  thumbTintColor="#3b82f6"
                />
              </View>
            </View>

            {/* Location */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Location</Text>
              <TextInput
                className="bg-dark-200 text-white px-4 py-3 rounded-lg"
                placeholder="Enter location..."
                placeholderTextColor="#9ca3af"
                value={filters.location}
                onChangeText={(text) =>
                  setFilters((prev) => ({ ...prev, location: text }))
                }
              />
            </View>

            {/* Posted Date */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Posted Date</Text>
              <View className="flex-row flex-wrap">
                {POSTED_OPTIONS.map((option) => (
                  <TouchableOpacity
                    key={option.value}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.postedDate === option.value
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() =>
                      setFilters((prev) => ({ ...prev, postedDate: option.value }))
                    }
                  >
                    <Text
                      className={`${
                        filters.postedDate === option.value ? 'text-white' : 'text-gray-400'
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
