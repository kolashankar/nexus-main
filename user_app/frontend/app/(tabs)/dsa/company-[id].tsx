import React, { useState } from 'react';
import { View, Text, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { useQuery } from '@tanstack/react-query';
import { Ionicons } from '@expo/vector-icons';
import api from '@/lib/api';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import EmptyState from '@/components/common/EmptyState';

interface Company {
  _id: string;
  name: string;
  logo: string;
  industry: string;
  problem_count: number;
  job_count: number;
  description?: string;
}

interface Question {
  _id: string;
  title: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  topics: string[];
}

export default function CompanyDetailScreen() {
  const { id } = useLocalSearchParams();
  const [refreshing, setRefreshing] = useState(false);

  const { data: company, isLoading, refetch } = useQuery({
    queryKey: ['company', id],
    queryFn: async () => {
      const response = await api.get(`/admin/dsa/companies/${id}`);
      return response.data.data;
    }
  });

  const { data: questionsData } = useQuery({
    queryKey: ['company-questions', id],
    queryFn: async () => {
      // Filter questions by this company
      const response = await api.get('/admin/dsa/questions', {
        params: { limit: 100 }
      });
      return response.data.data.filter((q: Question) => 
        q.topics?.some((t: any) => t.toLowerCase().includes(company?.name.toLowerCase() || ''))
      );
    },
    enabled: !!company
  });

  const onRefresh = async () => {
    setRefreshing(true);
    await refetch();
    setRefreshing(false);
  };

  if (isLoading) return <LoadingSpinner />;
  if (!company) return <EmptyState message="Company not found" />;

  const difficultyCount = questionsData?.reduce((acc: any, q: Question) => {
    acc[q.difficulty] = (acc[q.difficulty] || 0) + 1;
    return acc;
  }, {}) || {};

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'bg-green-100 text-green-700';
      case 'Medium': return 'bg-yellow-100 text-yellow-700';
      case 'Hard': return 'bg-red-100 text-red-700';
      default: return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <ScrollView 
      className="flex-1 bg-gray-50"
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Header */}
      <View className="bg-white p-6 border-b border-gray-200">
        <View className="flex-row items-center mb-4">
          <View className="w-16 h-16 bg-blue-100 rounded-full items-center justify-center mr-4">
            <Text className="text-2xl font-bold text-blue-600">
              {company.name.charAt(0)}
            </Text>
          </View>
          <View className="flex-1">
            <Text className="text-2xl font-bold text-gray-900">{company.name}</Text>
            <Text className="text-sm text-gray-500 mt-1">{company.industry}</Text>
          </View>
        </View>

        {company.description && (
          <Text className="text-gray-600 leading-6">{company.description}</Text>
        )}

        {/* Stats */}
        <View className="flex-row mt-4 space-x-4">
          <View className="flex-1 bg-blue-50 p-4 rounded-lg">
            <Text className="text-2xl font-bold text-blue-600">{company.problem_count}</Text>
            <Text className="text-sm text-gray-600 mt-1">Problems</Text>
          </View>
          <View className="flex-1 bg-green-50 p-4 rounded-lg">
            <Text className="text-2xl font-bold text-green-600">{company.job_count}</Text>
            <Text className="text-sm text-gray-600 mt-1">Job Openings</Text>
          </View>
        </View>
      </View>

      {/* Difficulty Breakdown */}
      <View className="bg-white p-6 mt-2 border-b border-gray-200">
        <Text className="text-lg font-semibold text-gray-900 mb-4">Difficulty Breakdown</Text>
        <View className="flex-row space-x-2">
          {['Easy', 'Medium', 'Hard'].map(diff => (
            <View key={diff} className="flex-1 bg-gray-50 p-3 rounded-lg">
              <Text className={`text-xs font-semibold ${diff === 'Easy' ? 'text-green-600' : diff === 'Medium' ? 'text-yellow-600' : 'text-red-600'}`}>
                {diff}
              </Text>
              <Text className="text-2xl font-bold text-gray-900 mt-1">
                {difficultyCount[diff] || 0}
              </Text>
            </View>
          ))}
        </View>
      </View>

      {/* Problems List */}
      <View className="bg-white p-6 mt-2">
        <Text className="text-lg font-semibold text-gray-900 mb-4">
          Problems ({questionsData?.length || 0})
        </Text>

        {questionsData && questionsData.length > 0 ? (
          <View className="space-y-3">
            {questionsData.map((question: Question) => (
              <TouchableOpacity
                key={question._id}
                className="bg-gray-50 p-4 rounded-lg border border-gray-200"
                onPress={() => router.push(`/dsa/question-${question._id}`)}
              >
                <View className="flex-row items-center justify-between mb-2">
                  <Text className="flex-1 text-base font-semibold text-gray-900">
                    {question.title}
                  </Text>
                  <View className={`px-3 py-1 rounded-full ${getDifficultyColor(question.difficulty)}`}>
                    <Text className="text-xs font-semibold">{question.difficulty}</Text>
                  </View>
                </View>
                
                <View className="flex-row flex-wrap gap-2">
                  {question.topics?.slice(0, 3).map((topic, idx) => (
                    <View key={idx} className="bg-white px-2 py-1 rounded border border-gray-200">
                      <Text className="text-xs text-gray-600">{topic}</Text>
                    </View>
                  ))}
                </View>
              </TouchableOpacity>
            ))}
          </View>
        ) : (
          <EmptyState message="No problems found for this company" />
        )}
      </View>

      {/* Interview Tips Section */}
      <View className="bg-white p-6 mt-2 mb-6">
        <Text className="text-lg font-semibold text-gray-900 mb-4">Interview Preparation Tips</Text>
        <View className="space-y-3">
          <View className="flex-row">
            <Ionicons name="checkmark-circle" size={20} color="#10b981" />
            <Text className="flex-1 ml-3 text-gray-700">
              Focus on data structures and algorithms fundamentals
            </Text>
          </View>
          <View className="flex-row">
            <Ionicons name="checkmark-circle" size={20} color="#10b981" />
            <Text className="flex-1 ml-3 text-gray-700">
              Practice coding questions from {company.name}'s frequently asked problems
            </Text>
          </View>
          <View className="flex-row">
            <Ionicons name="checkmark-circle" size={20} color="#10b981" />
            <Text className="flex-1 ml-3 text-gray-700">
              Review system design concepts for senior roles
            </Text>
          </View>
          <View className="flex-row">
            <Ionicons name="checkmark-circle" size={20} color="#10b981" />
            <Text className="flex-1 ml-3 text-gray-700">
              Understand the company's products and technical stack
            </Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );
}
