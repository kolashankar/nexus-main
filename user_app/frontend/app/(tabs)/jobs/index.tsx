import React, { useState } from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import JobsList from '../../../components/jobs/JobsList';
import InternshipsList from '../../../components/jobs/InternshipsList';
import ScholarshipsList from '../../../components/jobs/ScholarshipsList';

type TabType = 'jobs' | 'internships' | 'scholarships';

export default function JobsScreen() {
  const [activeTab, setActiveTab] = useState<TabType>('jobs');
  const router = useRouter();

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      {/* Hero Header */}
      <LinearGradient
        colors={['#2563eb', '#4f46e5', '#6366f1']}
        className="px-6 py-8"
      >
        <Text className="text-white text-3xl font-extrabold mb-2">
          {activeTab === 'jobs' && 'Find Your Dream Job'}
          {activeTab === 'internships' && 'Explore Internships'}
          {activeTab === 'scholarships' && 'Discover Scholarships'}
        </Text>
        <Text className="text-blue-100 text-base">
          {activeTab === 'jobs' && '50,000+ opportunities from top companies'}
          {activeTab === 'internships' && 'Gain valuable industry experience'}
          {activeTab === 'scholarships' && 'Support your educational journey'}
        </Text>
      </LinearGradient>

      {/* Tabs */}
      <View className="flex-row px-4 py-4 bg-white border-b border-gray-200">
        <TouchableOpacity
          className={`flex-1 py-3 rounded-lg mr-2 ${
            activeTab === 'jobs' ? 'bg-blue-600' : 'bg-gray-100'
          }`}
          onPress={() => setActiveTab('jobs')}
        >
          <Text
            className={`text-center font-bold text-sm ${
              activeTab === 'jobs' ? 'text-white' : 'text-gray-700'
            }`}
          >
            Jobs
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          className={`flex-1 py-3 rounded-lg mr-2 ${
            activeTab === 'internships' ? 'bg-blue-600' : 'bg-gray-100'
          }`}
          onPress={() => setActiveTab('internships')}
        >
          <Text
            className={`text-center font-bold text-sm ${
              activeTab === 'internships' ? 'text-white' : 'text-gray-700'
            }`}
          >
            Internships
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          className={`flex-1 py-3 rounded-lg ${
            activeTab === 'scholarships' ? 'bg-blue-600' : 'bg-gray-100'
          }`}
          onPress={() => setActiveTab('scholarships')}
        >
          <Text
            className={`text-center font-bold text-sm ${
              activeTab === 'scholarships' ? 'text-white' : 'text-gray-700'
            }`}
          >
            Scholarships
          </Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      <View className="flex-1 bg-gray-50">
        {activeTab === 'jobs' && <JobsList />}
        {activeTab === 'internships' && <InternshipsList />}
        {activeTab === 'scholarships' && <ScholarshipsList />}
      </View>
    </SafeAreaView>
  );
}