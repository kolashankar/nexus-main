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

interface Internship {
  _id: string;
  title: string;
  company_name: string;
  location: string;
  internship_type: string;
  category: string;
  duration: string;
  is_paid: boolean;
  stipend_amount?: number;
  stipend_currency?: string;
  description: string;
  skills_required: string[];
  responsibilities: string[];
  qualifications: string[];
  learning_outcomes: string[];
  start_date?: string;
  application_deadline?: string;
  application_url?: string;
  is_active: boolean;
}

export default function InternshipDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [isBookmarkedState, setIsBookmarkedState] = useState(false);

  const { data: internship, isLoading, isError } = useQuery({
    queryKey: ['internship', id],
    queryFn: async () => {
      const response = await api.get(`/admin/internships/${id}`);
      return response.data.internship;
    },
    enabled: !!id,
  });

  useEffect(() => {
    if (internship) {
      checkBookmark();
    }
  }, [internship]);

  const checkBookmark = async () => {
    if (internship) {
      const bookmarked = await isBookmarked(internship._id);
      setIsBookmarkedState(bookmarked);
    }
  };

  const handleBookmark = async () => {
    if (internship) {
      const success = await toggleBookmark(internship._id, 'internship', internship);
      if (success) {
        setIsBookmarkedState(!isBookmarkedState);
      }
    }
  };

  const handleApply = () => {
    if (internship?.application_url) {
      Linking.openURL(internship.application_url).catch(() => {
        Alert.alert('Error', 'Unable to open the application link');
      });
    } else {
      Alert.alert('Coming Soon', 'Application feature will be available soon');
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading internship details..." />
      </SafeAreaView>
    );
  }

  if (isError || !internship) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Internship"
          message="Failed to load internship details. Please try again."
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
            Internship Details
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
        {/* Internship Title & Company */}
        <View className="mb-6">
          <Text className="text-white text-2xl font-bold mb-2">{internship.title}</Text>
          <View className="flex-row items-center mb-2">
            <Ionicons name="business" size={16} color="#9ca3af" />
            <Text className="text-gray-300 text-base ml-2">{internship.company_name}</Text>
          </View>
          <View className="flex-row items-center">
            <Ionicons name="location" size={16} color="#9ca3af" />
            <Text className="text-gray-300 text-base ml-2">{internship.location}</Text>
          </View>
        </View>

        {/* Internship Info Tags */}
        <View className="flex-row flex-wrap mb-6">
          <View className="bg-primary-600 px-3 py-2 rounded-lg mr-2 mb-2">
            <Text className="text-white text-sm font-semibold">{internship.internship_type}</Text>
          </View>
          <View className="bg-purple-600 px-3 py-2 rounded-lg mr-2 mb-2">
            <Text className="text-white text-sm font-semibold">{internship.category}</Text>
          </View>
          <View className="bg-orange-600 px-3 py-2 rounded-lg mb-2">
            <Text className="text-white text-sm font-semibold">{internship.duration}</Text>
          </View>
        </View>

        {/* Stipend */}
        <View className="bg-dark-200 rounded-lg p-4 mb-6">
          <Text className="text-gray-400 text-sm mb-1">Stipend</Text>
          {internship.is_paid && internship.stipend_amount ? (
            <Text className="text-white text-xl font-bold">
              {internship.stipend_currency || '$'} {internship.stipend_amount.toLocaleString()}/month
            </Text>
          ) : (
            <Text className="text-white text-xl font-bold">Unpaid</Text>
          )}
        </View>

        {/* Description */}
        <View className="mb-6">
          <Text className="text-white text-lg font-bold mb-3">Description</Text>
          <Text className="text-gray-300 text-base leading-6">{internship.description}</Text>
        </View>

        {/* Skills Required */}
        {internship.skills_required && internship.skills_required.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Skills Required</Text>
            <View className="flex-row flex-wrap">
              {internship.skills_required.map((skill, index) => (
                <View key={index} className="bg-blue-600 px-3 py-2 rounded-lg mr-2 mb-2">
                  <Text className="text-white text-sm">{skill}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Responsibilities */}
        {internship.responsibilities && internship.responsibilities.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Responsibilities</Text>
            {internship.responsibilities.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Text className="text-primary-600 mr-2">•</Text>
                <Text className="text-gray-300 text-base flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Qualifications */}
        {internship.qualifications && internship.qualifications.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Qualifications</Text>
            {internship.qualifications.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Text className="text-primary-600 mr-2">•</Text>
                <Text className="text-gray-300 text-base flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Learning Outcomes */}
        {internship.learning_outcomes && internship.learning_outcomes.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Learning Outcomes</Text>
            {internship.learning_outcomes.map((item, index) => (
              <View key={index} className="flex-row mb-2">
                <Ionicons name="school" size={20} color="#10b981" />
                <Text className="text-gray-300 text-base ml-2 flex-1">{item}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Dates */}
        <View className="bg-dark-200 rounded-lg p-4 mb-6">
          {internship.start_date && (
            <View className="flex-row items-center mb-3">
              <Ionicons name="calendar-outline" size={20} color="#3b82f6" />
              <View className="ml-3">
                <Text className="text-gray-400 text-xs">Start Date</Text>
                <Text className="text-white text-base">
                  {new Date(internship.start_date).toLocaleDateString()}
                </Text>
              </View>
            </View>
          )}
          {internship.application_deadline && (
            <View className="flex-row items-center">
              <Ionicons name="time-outline" size={20} color="#ca8a04" />
              <View className="ml-3">
                <Text className="text-gray-400 text-xs">Application Deadline</Text>
                <Text className="text-white text-base">
                  {new Date(internship.application_deadline).toLocaleDateString()}
                </Text>
              </View>
            </View>
          )}
        </View>
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
