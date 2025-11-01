import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, RefreshControl } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import {
  getSheetProgress,
  toggleSheetQuestion,
  isQuestionCompletedInSheet,
} from '../../../lib/dsaProgress';

interface DSASheet {
  _id: string;
  name: string;
  description: string;
  level: string;
  tags: string[];
  questions: Array<{
    _id: string;
    title: string;
    difficulty: string;
    topics: string[];
  }>;
  difficulty_breakdown: {
    Easy: number;
    Medium: number;
    Hard: number;
  };
}

export default function SheetDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [completedQuestions, setCompletedQuestions] = useState<Set<string>>(new Set());

  const { data: sheet, isLoading, isError, refetch } = useQuery({
    queryKey: ['dsa-sheet', id],
    queryFn: async () => {
      const response = await api.get(`/admin/dsa/sheets/${id}`);
      return response.data.sheet;
    },
    enabled: !!id,
  });

  useEffect(() => {
    if (sheet) {
      loadProgress();
    }
  }, [sheet]);

  const loadProgress = async () => {
    if (sheet) {
      const progress = await getSheetProgress(sheet._id);
      if (progress) {
        setCompletedQuestions(new Set(progress.completedQuestions));
      }
    }
  };

  const handleToggleQuestion = async (questionId: string) => {
    if (sheet) {
      const success = await toggleSheetQuestion(sheet._id, questionId, sheet.questions.length);
      if (success) {
        setCompletedQuestions((prev) => {
          const newSet = new Set(prev);
          if (newSet.has(questionId)) {
            newSet.delete(questionId);
          } else {
            newSet.add(questionId);
          }
          return newSet;
        });
      }
    }
  };

  const handleQuestionPress = (questionId: string) => {
    router.push(`/(tabs)/dsa/question-${questionId}`);
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy':
        return 'text-green-600';
      case 'Medium':
        return 'text-yellow-600';
      case 'Hard':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  const progressPercentage = sheet
    ? Math.round((completedQuestions.size / sheet.questions.length) * 100)
    : 0;

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading sheet..." />
      </SafeAreaView>
    );
  }

  if (isError || !sheet) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Sheet"
          message="Failed to load sheet details. Please try again."
        />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-dark-400">
      {/* Header */}
      <View className="flex-row items-center px-6 py-4 border-b border-gray-700">
        <TouchableOpacity onPress={() => router.back()} className="mr-4">
          <Ionicons name="arrow-back" size={24} color="#fff" />
        </TouchableOpacity>
        <Text className="text-white text-xl font-bold flex-1" numberOfLines={1}>
          {sheet.name}
        </Text>
      </View>

      <ScrollView
        className="flex-1"
        refreshControl={<RefreshControl refreshing={false} onRefresh={refetch} tintColor="#3b82f6" />}
      >
        {/* Sheet Info */}
        <View className="px-6 py-4 border-b border-gray-700">
          <Text className="text-gray-300 text-sm mb-3">{sheet.description}</Text>
          <View className="flex-row items-center flex-wrap">
            <View className="bg-purple-600 px-3 py-1 rounded-full mr-2 mb-2">
              <Text className="text-white text-sm font-semibold">{sheet.level}</Text>
            </View>
            {sheet.tags.slice(0, 3).map((tag, index) => (
              <View key={index} className="bg-dark-300 px-3 py-1 rounded-full mr-2 mb-2">
                <Text className="text-gray-400 text-sm">#{tag}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Progress Bar */}
        <View className="px-6 py-4 border-b border-gray-700">
          <View className="flex-row justify-between items-center mb-2">
            <Text className="text-white font-bold">
              Progress: {completedQuestions.size}/{sheet.questions.length}
            </Text>
            <Text className="text-primary-600 font-bold">{progressPercentage}%</Text>
          </View>
          <View className="bg-dark-300 rounded-full h-3">
            <View
              className="bg-primary-600 rounded-full h-3"
              style={{ width: `${progressPercentage}%` }}
            />
          </View>

          {/* Difficulty Breakdown */}
          {sheet.difficulty_breakdown && (
            <View className="flex-row items-center mt-3">
              <View className="flex-row items-center mr-4">
                <View className="bg-green-600 w-3 h-3 rounded-full mr-1" />
                <Text className="text-gray-400 text-sm">{sheet.difficulty_breakdown.Easy} Easy</Text>
              </View>
              <View className="flex-row items-center mr-4">
                <View className="bg-yellow-600 w-3 h-3 rounded-full mr-1" />
                <Text className="text-gray-400 text-sm">{sheet.difficulty_breakdown.Medium} Medium</Text>
              </View>
              <View className="flex-row items-center">
                <View className="bg-red-600 w-3 h-3 rounded-full mr-1" />
                <Text className="text-gray-400 text-sm">{sheet.difficulty_breakdown.Hard} Hard</Text>
              </View>
            </View>
          )}
        </View>

        {/* Questions List */}
        <View className="px-6 py-4">
          <Text className="text-white text-lg font-bold mb-4">Questions</Text>
          {sheet.questions.map((question, index) => (
            <View key={question._id} className="bg-dark-200 rounded-lg p-4 mb-3">
              <View className="flex-row items-start">
                {/* Checkbox */}
                <TouchableOpacity
                  className="mr-3 mt-1"
                  onPress={() => handleToggleQuestion(question._id)}
                >
                  <View
                    className={`w-6 h-6 rounded border-2 items-center justify-center ${
                      completedQuestions.has(question._id)
                        ? 'bg-green-600 border-green-600'
                        : 'border-gray-500'
                    }`}
                  >
                    {completedQuestions.has(question._id) && (
                      <Ionicons name="checkmark" size={16} color="#fff" />
                    )}
                  </View>
                </TouchableOpacity>

                {/* Question Info */}
                <TouchableOpacity
                  className="flex-1"
                  onPress={() => handleQuestionPress(question._id)}
                >
                  <View className="flex-row items-start justify-between mb-2">
                    <Text
                      className={`text-base font-bold flex-1 mr-2 ${
                        completedQuestions.has(question._id)
                          ? 'text-gray-500 line-through'
                          : 'text-white'
                      }`}
                      numberOfLines={2}
                    >
                      {index + 1}. {question.title}
                    </Text>
                    <Text className={`text-sm font-semibold ${getDifficultyColor(question.difficulty)}`}>
                      {question.difficulty}
                    </Text>
                  </View>

                  {/* Topics */}
                  <View className="flex-row flex-wrap">
                    {question.topics.slice(0, 3).map((topic, topicIndex) => (
                      <View key={topicIndex} className="bg-primary-600 px-2 py-1 rounded mr-2 mb-1">
                        <Text className="text-white text-xs">{topic}</Text>
                      </View>
                    ))}
                  </View>
                </TouchableOpacity>
              </View>
            </View>
          ))}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
