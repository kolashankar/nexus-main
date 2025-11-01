import React from 'react';
import { View, Text, ScrollView, TouchableOpacity, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';

export default function JobDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();

  const { data: job, isLoading, isError } = useQuery({
    queryKey: ['job', id],
    queryFn: async () => {
      const response = await api.get(`/user/jobs/${id}`);
      return response.data.job;
    },
    enabled: !!id,
  });

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <View className="flex-1 items-center justify-center">
          <ActivityIndicator size="large" color="#3b82f6" />
        </View>
      </SafeAreaView>
    );
  }

  if (isError || !job) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <View className="flex-1 items-center justify-center px-6">
          <Ionicons name="alert-circle-outline" size={64} color="#4b5563" />
          <Text className="text-white text-xl font-bold mt-4">Job Not Found</Text>
          <TouchableOpacity
            className="bg-primary-600 px-6 py-3 rounded-lg mt-4"
            onPress={() => router.back()}
          >
            <Text className="text-white font-semibold">Go Back</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center px-6 py-4 border-b border-dark-200">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text className="text-white text-lg font-bold flex-1">Job Details</Text>
        <TouchableOpacity>
          <Ionicons name="bookmark-outline" size={24} color="#fff" />
        </TouchableOpacity>
      </View>

      <ScrollView className="flex-1">
        {/* Job Header */}
        <View className="px-6 py-6 border-b border-dark-200">
          <Text className="text-white text-2xl font-bold mb-2">{job.title}</Text>
          <Text className="text-gray-400 text-lg mb-4">{job.company}</Text>
          
          <View className="flex-row flex-wrap">
            <View className="bg-primary-600 px-3 py-1 rounded-full mr-2 mb-2">
              <Text className="text-white text-sm font-semibold">{job.job_type}</Text>
            </View>
            <View className="bg-dark-200 px-3 py-1 rounded-full mr-2 mb-2">
              <Text className="text-gray-300 text-sm">{job.category}</Text>
            </View>
            <View className="bg-dark-200 px-3 py-1 rounded-full mb-2">
              <Text className="text-gray-300 text-sm">{job.experience_level}</Text>
            </View>
          </View>
        </View>

        {/* Job Info */}
        <View className="px-6 py-6 border-b border-dark-200">
          <View className="flex-row items-center mb-3">
            <Ionicons name="location" size={20} color="#9ca3af" />
            <Text className="text-gray-300 ml-3">{job.location}</Text>
          </View>
          {job.salary_min && job.salary_max && (
            <View className="flex-row items-center mb-3">
              <Ionicons name="cash" size={20} color="#9ca3af" />
              <Text className="text-gray-300 ml-3">
                ${job.salary_min.toLocaleString()} - ${job.salary_max.toLocaleString()}
              </Text>
            </View>
          )}
          <View className="flex-row items-center">
            <Ionicons name="calendar" size={20} color="#9ca3af" />
            <Text className="text-gray-300 ml-3">
              Posted {new Date(job.created_at).toLocaleDateString()}
            </Text>
          </View>
        </View>

        {/* Description */}
        <View className="px-6 py-6 border-b border-dark-200">
          <Text className="text-white text-lg font-bold mb-3">Description</Text>
          <Text className="text-gray-300 leading-6">{job.description}</Text>
        </View>

        {/* Skills */}
        {job.skills && job.skills.length > 0 && (
          <View className="px-6 py-6 border-b border-dark-200">
            <Text className="text-white text-lg font-bold mb-3">Required Skills</Text>
            <View className="flex-row flex-wrap">
              {job.skills.map((skill: string, index: number) => (
                <View key={index} className="bg-primary-600 px-3 py-1 rounded-full mr-2 mb-2">
                  <Text className="text-white text-sm">{skill}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Responsibilities */}
        {job.responsibilities && job.responsibilities.length > 0 && (
          <View className="px-6 py-6 border-b border-dark-200">
            <Text className="text-white text-lg font-bold mb-3">Responsibilities</Text>
            {job.responsibilities.map((resp: string, index: number) => (
              <View key={index} className="flex-row mb-2">
                <Text className="text-gray-400 mr-2">•</Text>
                <Text className="text-gray-300 flex-1">{resp}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Qualifications */}
        {job.qualifications && job.qualifications.length > 0 && (
          <View className="px-6 py-6 border-b border-dark-200">
            <Text className="text-white text-lg font-bold mb-3">Qualifications</Text>
            {job.qualifications.map((qual: string, index: number) => (
              <View key={index} className="flex-row mb-2">
                <Text className="text-gray-400 mr-2">•</Text>
                <Text className="text-gray-300 flex-1">{qual}</Text>
              </View>
            ))}
          </View>
        )}

        {/* Benefits */}
        {job.benefits && job.benefits.length > 0 && (
          <View className="px-6 py-6 mb-20">
            <Text className="text-white text-lg font-bold mb-3">Benefits</Text>
            {job.benefits.map((benefit: string, index: number) => (
              <View key={index} className="flex-row mb-2">
                <Ionicons name="checkmark-circle" size={20} color="#10b981" />
                <Text className="text-gray-300 flex-1 ml-2">{benefit}</Text>
              </View>
            ))}
          </View>
        )}
      </ScrollView>

      {/* Apply Button */}
      <View className="absolute bottom-0 left-0 right-0 bg-dark-300 px-6 py-4 border-t border-dark-200">
        <TouchableOpacity className="bg-primary-600 py-4 rounded-lg items-center">
          <Text className="text-white font-bold text-lg">Apply Now</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}
