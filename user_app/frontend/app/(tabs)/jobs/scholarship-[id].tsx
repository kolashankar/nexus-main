import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Linking, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import { toggleBookmark, isBookmarked } from '../../../lib/bookmarks';

interface Scholarship {
  _id: string;
  title: string;
  organization_name: string;
  country: string;
  scholarship_type: string;
  field_of_study: string;
  education_level: string;
  amount: number;
  currency: string;
  description: string;
  eligibility_criteria: string[];
  benefits: string[];
  application_process: string[];
  required_documents: string[];
  deadline: string;
  application_url?: string;
  is_active: boolean;
}

export default function ScholarshipDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [isBookmarkedState, setIsBookmarkedState] = useState(false);

  const { data: scholarship, isLoading, isError } = useQuery({
    queryKey: ['scholarship', id],
    queryFn: async () => {
      const response = await api.get(`/admin/scholarships/${id}`);
      return response.data.scholarship;
    },
    enabled: !!id,
  });

  useEffect(() => {
    if (scholarship) {
      checkBookmark();
    }
  }, [scholarship]);

  const checkBookmark = async () => {
    if (scholarship) {
      const bookmarked = await isBookmarked(scholarship._id);
      setIsBookmarkedState(bookmarked);
    }
  };

  const handleBookmark = async () => {
    if (scholarship) {
      const success = await toggleBookmark(scholarship._id, 'scholarship', scholarship);
      if (success) {
        setIsBookmarkedState(!isBookmarkedState);
      }
    }
  };

  const handleApply = () => {
    if (scholarship?.application_url) {
      Linking.openURL(scholarship.application_url).catch(() => {
        Alert.alert('Error', 'Unable to open the application link');
      });
    } else {
      Alert.alert('Coming Soon', 'Application feature will be available soon');
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading scholarship details..." />
      </SafeAreaView>
    );
  }

  if (isError || !scholarship) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Scholarship"
          message="Failed to load scholarship details. Please try again."
        />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center justify-between px-6 py-4 border-b border-gray-700">
        <View className="flex-row items-center flex-1">
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
            <Ionicons name="arrow-back" size={24} color="#fff" />
          </TouchableOpacity>
          <Text className="text-white text-xl font-bold" numberOfLines={1}>
            Scholarship Details
          </Text>
        </View>
        <TouchableOpacity onPress={handleBookmark}>
          <Ionicons
            name={isBookmarkedState ? 'bookmark' : 'bookmark-outline'}
            size={26}
            color={isBookmarkedState ? '#3b82f6' : '#fff'}
          />
        </TouchableOpacity>
      </View>

      <ScrollView className="flex-1 px-6 py-4">
        {/* Scholarship Title & Organization */}
        <View className="mb-6">
          <Text className="text-white text-2xl font-bold mb-2">{scholarship.title}</Text>
          <View className="flex-row items-center mb-2">
            <Ionicons name="business" size={16} color="#9ca3af" />
            <Text className="text-gray-300 text-base ml-2">{scholarship.organization_name}</Text>
          </View>
          <View className="flex-row items-center">
            <Ionicons name="location" size={16} color="#9ca3af" />
            <Text className="text-gray-300 text-base ml-2">{scholarship.country}</Text>
          </View>
        </View>

        {/* Scholarship Info Tags */}
        <View className="flex-row flex-wrap mb-6">
          <View className="bg-primary-600 px-3 py-2 rounded-lg mr-2 mb-2">
            <Text className="text-white text-sm font-semibold">{scholarship.scholarship_type}</Text>
          </View>
          <View className="bg-green-600 px-3 py-2 rounded-lg mr-2 mb-2">
            <Text className="text-white text-sm font-semibold">{scholarship.education_level}</Text>
          </View>
          <View className="bg-purple-600 px-3 py-2 rounded-lg mb-2">
            <Text className="text-white text-sm font-semibold">{scholarship.field_of_study}</Text>
          </View>
        </View>

        {/* Amount */}
        <View className="bg-dark-200 rounded-lg p-4 mb-6">
          <Text className="text-gray-400 text-sm mb-1">Scholarship Amount</Text>
          <Text className="text-white text-xl font-bold">
            {scholarship.currency} {scholarship.amount.toLocaleString()}
          </Text>
        </View>

        {/* Description */}
        <View className="mb-6">
          <Text className="text-white text-lg font-bold mb-3">Description</Text>
          <Text className="text-gray-300 text-base leading-6">{scholarship.description}</Text>
        </View>

        {/* Eligibility Criteria */}
        {scholarship.eligibility_criteria && scholarship.eligibility_criteria.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Eligibility Criteria</Text>
            {scholarship.eligibility_criteria.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Ionicons name="checkmark-circle" size={20} color="#10b981" />
                <Text className="text-gray-300 text-base ml-2 flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Benefits */}
        {scholarship.benefits && scholarship.benefits.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Benefits</Text>
            {scholarship.benefits.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Ionicons name="star" size={20} color="#f59e0b" />
                <Text className="text-gray-300 text-base ml-2 flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Application Process */}
        {scholarship.application_process && scholarship.application_process.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Application Process</Text>
            {scholarship.application_process.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <View className="bg-primary-600 w-6 h-6 rounded-full items-center justify-center mr-2">
                  <Text className="text-white text-xs font-bold">{index + 1}</Text>
                </View>
                <Text className="text-gray-300 text-base flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Required Documents */}
        {scholarship.required_documents && scholarship.required_documents.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Required Documents</Text>
            {scholarship.required_documents.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Ionicons name="document-text" size={20} color="#3b82f6" />
                <Text className="text-gray-300 text-base ml-2 flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Deadline */}
        {scholarship.deadline && (
          <View className="bg-red-600/20 border border-red-600 rounded-lg p-4 mb-6">
            <View className="flex-row items-center">
              <Ionicons name="alert-circle" size={24} color="#dc2626" />
              <View className="ml-3">
                <Text className="text-red-600 font-bold text-base">Application Deadline</Text>
                <Text className="text-red-600 text-lg font-bold mt-1">
                  {new Date(scholarship.deadline).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric',
                  })}
                </Text>
              </View>
            </View>
          </View>
        )}
      </ScrollView>

      {/* Apply Button */}
      <View className="px-6 py-4 border-t border-gray-700">
        <TouchableOpacity
          className="bg-primary-600 py-4 rounded-lg flex-row items-center justify-center"
          onPress={handleApply}
        >
          <Ionicons name="send" size={20} color="#fff" />
          <Text className="text-white text-lg font-bold ml-2">Apply Now</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
