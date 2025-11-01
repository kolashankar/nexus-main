import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useQuery } from '@tanstack/react-query';
import api from '../../../lib/api';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';
import { toggleBookmark, isBookmarked } from '../../../lib/bookmarks';
import { recordQuestionSubmission, getQuestionStatus } from '../../../lib/dsaProgress';

interface CodeSolution {
  language: string;
  code: string;
}

interface DSAQuestion {
  _id: string;
  title: string;
  description: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  topics: string[];
  companies: string[];
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints: string[];
  solution_approach?: string;
  code_solutions: CodeSolution[];
  hints: string[];
  time_complexity?: string;
  space_complexity?: string;
  similar_questions?: string[];
}

export default function QuestionDetailScreen() {
  const { id } = useLocalSearchParams();
  const router = useRouter();
  const [isBookmarkedState, setIsBookmarkedState] = useState(false);
  const [showSolution, setShowSolution] = useState(false);
  const [showHints, setShowHints] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('Python');
  const [questionStatus, setQuestionStatus] = useState<'unsolved' | 'attempted' | 'solved'>('unsolved');

  const { data: question, isLoading, isError } = useQuery({
    queryKey: ['dsa-question', id],
    queryFn: async () => {
      const response = await api.get(`/admin/dsa/questions/${id}`);
      return response.data.question;
    },
    enabled: !!id,
  });

  useEffect(() => {
    if (question) {
      checkBookmark();
      loadQuestionStatus();
    }
  }, [question]);

  const checkBookmark = async () => {
    if (question) {
      const bookmarked = await isBookmarked(question._id);
      setIsBookmarkedState(bookmarked);
    }
  };

  const loadQuestionStatus = async () => {
    if (question) {
      const status = await getQuestionStatus(question._id);
      setQuestionStatus(status);
    }
  };

  const handleBookmark = async () => {
    if (question) {
      const success = await toggleBookmark(question._id, 'question', question);
      if (success) {
        setIsBookmarkedState(!isBookmarkedState);
      }
    }
  };

  const handleSubmit = async (status: 'attempted' | 'solved') => {
    if (question) {
      const success = await recordQuestionSubmission(question._id, question.title, status);
      if (success) {
        setQuestionStatus(status);
        Alert.alert('Success', `Question marked as ${status}!`);
      }
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'bg-green-600';
      case 'Medium': return 'bg-yellow-600';
      case 'Hard': return 'bg-red-600';
      default: return 'bg-gray-600';
    }
  };

  const getStatusIcon = () => {
    switch (questionStatus) {
      case 'solved': return 'checkmark-circle';
      case 'attempted': return 'time';
      default: return 'code-slash';
    }
  };

  const getStatusColor = () => {
    switch (questionStatus) {
      case 'solved': return '#10b981';
      case 'attempted': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  if (isLoading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading question..." />
      </SafeAreaView>
    );
  }

  if (isError || !question) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <EmptyState
          icon="alert-circle-outline"
          title="Error Loading Question"
          message="Failed to load question details. Please try again."
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
          <Ionicons name={getStatusIcon()} size={24} color={getStatusColor()} />
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
        {/* Question Title */}
        <View className="mb-4">
          <Text className="text-white text-2xl font-bold mb-3">{question.title}</Text>
          <View className="flex-row items-center flex-wrap">
            <View className={`${getDifficultyColor(question.difficulty)} px-3 py-1 rounded-full mr-2 mb-2`}>
              <Text className="text-white text-sm font-semibold">{question.difficulty}</Text>
            </View>
            {question.topics.slice(0, 3).map((topic, index) => (
              <View key={index} className="bg-primary-600 px-3 py-1 rounded-full mr-2 mb-2">
                <Text className="text-white text-sm">{topic}</Text>
              </View>
            ))}
          </View>
        </View>

        {/* Companies */}
        {question.companies && question.companies.length > 0 && (
          <View className="bg-dark-200 rounded-lg p-3 mb-4">
            <Text className="text-gray-400 text-xs mb-1">Asked by companies:</Text>
            <Text className="text-white text-sm">{question.companies.join(', ')}</Text>
          </View>
        )}

        {/* Problem Statement */}
        <View className="mb-6">
          <Text className="text-white text-lg font-bold mb-3">Problem Statement</Text>
          <Text className="text-gray-300 text-base leading-6">{question.description}</Text>
        </View>

        {/* Examples */}
        {question.examples && question.examples.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Examples</Text>
            {question.examples.map((example, index) => (
              <View key={index} className="bg-dark-200 rounded-lg p-4 mb-3">
                <Text className="text-primary-600 font-bold mb-2">Example {index + 1}</Text>
                <View className="mb-2">
                  <Text className="text-gray-400 text-sm">Input:</Text>
                  <Text className="text-white font-mono text-sm mt-1">{example.input}</Text>
                </View>
                <View className="mb-2">
                  <Text className="text-gray-400 text-sm">Output:</Text>
                  <Text className="text-white font-mono text-sm mt-1">{example.output}</Text>
                </View>
                {example.explanation && (
                  <View>
                    <Text className="text-gray-400 text-sm">Explanation:</Text>
                    <Text className="text-gray-300 text-sm mt-1">{example.explanation}</Text>
                  </View>
                )}
              </View>
            ))}
          </View>
        )}

        {/* Constraints */}
        {question.constraints && question.constraints.length > 0 && (
          <View className="mb-6">
            <Text className="text-white text-lg font-bold mb-3">Constraints</Text>
            <View className="bg-dark-200 rounded-lg p-4">
              {question.constraints.map((constraint, index) => (
                <View key={index} className="flex-row mb-2">
                  <Text className="text-primary-600 mr-2">•</Text>
                  <Text className="text-gray-300 text-sm flex-1">{constraint}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Hints */}
        {question.hints && question.hints.length > 0 && (
          <View className="mb-6">
            <TouchableOpacity
              className="flex-row items-center justify-between bg-yellow-600/20 border border-yellow-600 rounded-lg p-4 mb-3"
              onPress={() => setShowHints(!showHints)}
            >
              <Text className="text-yellow-600 font-bold">💡 Hints ({question.hints.length})</Text>
              <Ionicons
                name={showHints ? 'chevron-up' : 'chevron-down'}
                size={20}
                color="#ca8a04"
              />
            </TouchableOpacity>
            {showHints && (
              <View className="bg-dark-200 rounded-lg p-4">
                {question.hints.map((hint, index) => (
                  <View key={index} className="mb-3">
                    <Text className="text-yellow-600 font-semibold mb-1">Hint {index + 1}:</Text>
                    <Text className="text-gray-300 text-sm">{hint}</Text>
                  </View>
                ))}
              </View>
            )}
          </View>
        )}

        {/* Solution */}
        <View className="mb-6">
          <TouchableOpacity
            className="flex-row items-center justify-between bg-green-600/20 border border-green-600 rounded-lg p-4 mb-3"
            onPress={() => setShowSolution(!showSolution)}
          >
            <Text className="text-green-600 font-bold">🎯 Solution Approach</Text>
            <Ionicons
              name={showSolution ? 'chevron-up' : 'chevron-down'}
              size={20}
              color="#10b981"
            />
          </TouchableOpacity>
          {showSolution && (
            <View>
              {question.solution_approach && (
                <View className="bg-dark-200 rounded-lg p-4 mb-4">
                  <Text className="text-white text-base leading-6">{question.solution_approach}</Text>
                </View>
              )}

              {/* Code Solutions */}
              {question.code_solutions && question.code_solutions.length > 0 && (
                <View className="mb-4">
                  <Text className="text-white text-base font-bold mb-3">Code Solutions</Text>
                  
                  {/* Language Selector */}
                  <ScrollView horizontal showsHorizontalScrollIndicator={false} className="mb-3">
                    {question.code_solutions.map((solution, index) => (
                      <TouchableOpacity
                        key={index}
                        className={`px-4 py-2 rounded-lg mr-2 ${
                          selectedLanguage === solution.language ? 'bg-primary-600' : 'bg-dark-200'
                        }`}
                        onPress={() => setSelectedLanguage(solution.language)}
                      >
                        <Text className="text-white font-semibold">{solution.language}</Text>
                      </TouchableOpacity>
                    ))}
                  </ScrollView>

                  {/* Selected Language Code */}
                  {question.code_solutions
                    .filter((s) => s.language === selectedLanguage)
                    .map((solution, index) => (
                      <View key={index} className="bg-dark-300 rounded-lg p-4">
                        <ScrollView horizontal>
                          <Text className="text-gray-300 font-mono text-sm">{solution.code}</Text>
                        </ScrollView>
                      </View>
                    ))}
                </View>
              )}

              {/* Complexity Analysis */}
              {(question.time_complexity || question.space_complexity) && (
                <View className="bg-dark-200 rounded-lg p-4">
                  <Text className="text-white font-bold mb-2">Complexity Analysis</Text>
                  {question.time_complexity && (
                    <View className="mb-2">
                      <Text className="text-gray-400 text-sm">Time Complexity:</Text>
                      <Text className="text-white font-mono">{question.time_complexity}</Text>
                    </View>
                  )}
                  {question.space_complexity && (
                    <View>
                      <Text className="text-gray-400 text-sm">Space Complexity:</Text>
                      <Text className="text-white font-mono">{question.space_complexity}</Text>
                    </View>
                  )}
                </View>
              )}
            </View>
          )}
        </View>
      </ScrollView>

      {/* Action Buttons */}
      <View className="px-6 py-4 border-t border-gray-700">
        <View className="flex-row">
          <TouchableOpacity
            className="flex-1 bg-yellow-600 py-3 rounded-lg mr-2 flex-row items-center justify-center"
            onPress={() => handleSubmit('attempted')}
          >
            <Ionicons name="time" size={20} color="#fff" />
            <Text className="text-white font-bold ml-2">Mark Attempted</Text>
          </TouchableOpacity>
          <TouchableOpacity
            className="flex-1 bg-green-600 py-3 rounded-lg flex-row items-center justify-center"
            onPress={() => handleSubmit('solved')}
          >
            <Ionicons name="checkmark-circle" size={20} color="#fff" />
            <Text className="text-white font-bold ml-2">Mark Solved</Text>
          </TouchableOpacity>
        </View>
      </View>
    </SafeAreaView>
  );
}
