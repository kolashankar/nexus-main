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

export interface InternshipFilters {
  internshipTypes: string[];
  durations: string[];
  isPaid: string; // 'all', 'paid', 'unpaid'
  locationTypes: string[];
  stipendMin: number;
  stipendMax: number;
  location: string;
}

interface InternshipsFilterModalProps {
  visible: boolean;
  onClose: () => void;
  onApply: (filters: InternshipFilters) => void;
  currentFilters: InternshipFilters;
}

const INTERNSHIP_TYPES = ['Full-time', 'Part-time', 'Summer', 'Virtual'];
const DURATIONS = ['1-2 months', '3-4 months', '5-6 months', '6+ months'];
const PAID_OPTIONS = [
  { label: 'All', value: 'all' },
  { label: 'Paid Only', value: 'paid' },
  { label: 'Unpaid', value: 'unpaid' },
];
const LOCATION_TYPES = ['On-site', 'Remote', 'Hybrid'];

export default function InternshipsFilterModal({
  visible,
  onClose,
  onApply,
  currentFilters,
}: InternshipsFilterModalProps) {
  const [filters, setFilters] = useState<InternshipFilters>(currentFilters);

  const toggleInternshipType = (type: string) => {
    setFilters((prev) => ({
      ...prev,
      internshipTypes: prev.internshipTypes.includes(type)
        ? prev.internshipTypes.filter((t) => t !== type)
        : [...prev.internshipTypes, type],
    }));
  };

  const toggleDuration = (duration: string) => {
    setFilters((prev) => ({
      ...prev,
      durations: prev.durations.includes(duration)
        ? prev.durations.filter((d) => d !== duration)
        : [...prev.durations, duration],
    }));
  };

  const toggleLocationType = (type: string) => {
    setFilters((prev) => ({
      ...prev,
      locationTypes: prev.locationTypes.includes(type)
        ? prev.locationTypes.filter((t) => t !== type)
        : [...prev.locationTypes, type],
    }));
  };

  const handleApply = () => {
    onApply(filters);
    onClose();
  };

  const handleReset = () => {
    const resetFilters: InternshipFilters = {
      internshipTypes: [],
      durations: [],
      isPaid: 'all',
      locationTypes: [],
      stipendMin: 0,
      stipendMax: 5000,
      location: '',
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
            {/* Internship Type */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">
                Internship Type
              </Text>
              <View className="flex-row flex-wrap">
                {INTERNSHIP_TYPES.map((type) => (
                  <TouchableOpacity
                    key={type}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.internshipTypes.includes(type)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleInternshipType(type)}
                  >
                    <Text
                      className={`${
                        filters.internshipTypes.includes(type)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {type}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Duration */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Duration</Text>
              <View className="flex-row flex-wrap">
                {DURATIONS.map((duration) => (
                  <TouchableOpacity
                    key={duration}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.durations.includes(duration)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleDuration(duration)}
                  >
                    <Text
                      className={`${
                        filters.durations.includes(duration)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {duration}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Paid/Unpaid */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Compensation</Text>
              <View className="flex-row flex-wrap">
                {PAID_OPTIONS.map((option) => (
                  <TouchableOpacity
                    key={option.value}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.isPaid === option.value
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() =>
                      setFilters((prev) => ({ ...prev, isPaid: option.value }))
                    }
                  >
                    <Text
                      className={`${
                        filters.isPaid === option.value ? 'text-white' : 'text-gray-400'
                      }`}
                    >
                      {option.label}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Location Type */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">
                Location Type
              </Text>
              <View className="flex-row flex-wrap">
                {LOCATION_TYPES.map((type) => (
                  <TouchableOpacity
                    key={type}
                    className={`px-4 py-2 rounded-full mr-2 mb-2 ${
                      filters.locationTypes.includes(type)
                        ? 'bg-primary-600'
                        : 'bg-dark-200 border border-gray-700'
                    }`}
                    onPress={() => toggleLocationType(type)}
                  >
                    <Text
                      className={`${
                        filters.locationTypes.includes(type)
                          ? 'text-white'
                          : 'text-gray-400'
                      }`}
                    >
                      {type}
                    </Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>

            {/* Stipend Range */}
            <View className="mb-6">
              <Text className="text-white text-lg font-semibold mb-3">Stipend Range</Text>
              <View className="bg-dark-200 rounded-lg p-4">
                <View className="flex-row justify-between mb-2">
                  <Text className="text-gray-400">
                    ${filters.stipendMin.toLocaleString()}
                  </Text>
                  <Text className="text-gray-400">
                    ${filters.stipendMax.toLocaleString()}
                  </Text>
                </View>
                <Slider
                  minimumValue={0}
                  maximumValue={5000}
                  step={100}
                  value={filters.stipendMin}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, stipendMin: value }))
                  }
                  minimumTrackTintColor="#3b82f6"
                  maximumTrackTintColor="#374151"
                  thumbTintColor="#3b82f6"
                />
                <Text className="text-gray-400 text-sm mt-2">Maximum</Text>
                <Slider
                  minimumValue={0}
                  maximumValue={5000}
                  step={100}
                  value={filters.stipendMax}
                  onValueChange={(value) =>
                    setFilters((prev) => ({ ...prev, stipendMax: value }))
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
