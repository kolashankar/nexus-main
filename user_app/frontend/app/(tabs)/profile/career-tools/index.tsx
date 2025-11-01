import React from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { useAuth } from '@/contexts/AuthContext';

interface Tool {
  id: string;
  title: string;
  description: string;
  icon: keyof typeof Ionicons.glyphMap;
  route: string;
  color: string;
}

const tools: Tool[] = [
  {
    id: 'resume-review',
    title: 'Resume Review',
    description: 'Get AI-powered feedback on your resume format, content, and ATS compatibility',
    icon: 'document-text',
    route: '/profile/career-tools/resume-review',
    color: 'bg-blue-500'
  },
  {
    id: 'cover-letter',
    title: 'Cover Letter Generator',
    description: 'Create personalized cover letters tailored to specific job applications',
    icon: 'mail',
    route: '/profile/career-tools/cover-letter',
    color: 'bg-green-500'
  },
  {
    id: 'ats-hack',
    title: 'ATS Optimizer',
    description: 'Optimize your resume to pass Applicant Tracking Systems with keyword analysis',
    icon: 'shield-checkmark',
    route: '/profile/career-tools/ats-hack',
    color: 'bg-purple-500'
  },
  {
    id: 'cold-email',
    title: 'Cold Email Generator',
    description: 'Generate professional networking emails for recruiters and hiring managers',
    icon: 'send',
    route: '/profile/career-tools/cold-email',
    color: 'bg-orange-500'
  }
];

export default function CareerToolsScreen() {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <SafeAreaView className="flex-1 bg-gray-50">
        <View className="flex-1 items-center justify-center px-6">
          <Ionicons name="lock-closed-outline" size={80} color="#9ca3af" />
          <Text className="text-2xl font-bold text-gray-900 mt-6 mb-3 text-center">
            Sign In Required
          </Text>
          <Text className="text-gray-600 text-center mb-8">
            Please sign in to access AI-powered career tools
          </Text>
          <TouchableOpacity
            onPress={() => router.push('/login')}
            className="bg-blue-500 px-8 py-3 rounded-lg"
          >
            <Text className="text-white font-semibold text-base">Sign In</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView>
        {/* Header */}
        <View className="bg-white px-6 py-6 border-b border-gray-200">
          <Text className="text-2xl font-bold text-gray-900 mb-2">Career Tools</Text>
          <Text className="text-sm text-gray-500">
            AI-powered tools to boost your job search
          </Text>
        </View>

        {/* Welcome Message */}
        <View className="bg-gradient-to-r from-blue-500 to-purple-600 mx-4 mt-4 p-6 rounded-xl">
          <View className="flex-row items-center mb-3">
            <View className="bg-white/20 p-2 rounded-full mr-3">
              <Ionicons name="sparkles" size={24} color="#fff" />
            </View>
            <Text className="text-white text-lg font-bold">Powered by Gemini AI</Text>
          </View>
          <Text className="text-white/90 text-sm leading-6">
            Get personalized, AI-generated content to help you stand out in your job search. 
            All tools use advanced AI to provide professional, tailored results.
          </Text>
        </View>

        {/* Tools Grid */}
        <View className="px-4 py-6">
          {tools.map((tool, index) => (
            <TouchableOpacity
              key={tool.id}
              onPress={() => router.push(tool.route as any)}
              className="bg-white rounded-xl p-5 mb-4 shadow-sm border border-gray-200"
            >
              <View className="flex-row items-start">
                <View className={`${tool.color} w-14 h-14 rounded-xl items-center justify-center mr-4`}>
                  <Ionicons name={tool.icon} size={28} color="#fff" />
                </View>
                <View className="flex-1">
                  <View className="flex-row items-center justify-between mb-2">
                    <Text className="text-lg font-bold text-gray-900 flex-1">
                      {tool.title}
                    </Text>
                    <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
                  </View>
                  <Text className="text-gray-600 text-sm leading-5">
                    {tool.description}
                  </Text>
                </View>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {/* Usage History */}
        <TouchableOpacity
          onPress={() => router.push('/profile/career-tools/history')}
          className="bg-white mx-4 mb-6 p-4 rounded-xl flex-row items-center justify-between border border-gray-200"
        >
          <View className="flex-row items-center">
            <View className="bg-gray-100 w-12 h-12 rounded-full items-center justify-center mr-3">
              <Ionicons name="time-outline" size={24} color="#6b7280" />
            </View>
            <View>
              <Text className="text-base font-semibold text-gray-900">Usage History</Text>
              <Text className="text-sm text-gray-500">View all your AI-generated content</Text>
            </View>
          </View>
          <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
        </TouchableOpacity>

        {/* Tips Section */}
        <View className="bg-white mx-4 mb-6 p-6 rounded-xl border border-gray-200">
          <Text className="text-lg font-bold text-gray-900 mb-4">Pro Tips</Text>
          <View className="space-y-3">
            <View className="flex-row">
              <Ionicons name="bulb-outline" size={20} color="#f59e0b" />
              <Text className="flex-1 ml-3 text-gray-700 text-sm">
                Be specific with your inputs for better AI-generated results
              </Text>
            </View>
            <View className="flex-row">
              <Ionicons name="create-outline" size={20} color="#f59e0b" />
              <Text className="flex-1 ml-3 text-gray-700 text-sm">
                Always review and customize AI content before using it
              </Text>
            </View>
            <View className="flex-row">
              <Ionicons name="save-outline" size={20} color="#f59e0b" />
              <Text className="flex-1 ml-3 text-gray-700 text-sm">
                Save your favorites in Usage History for quick access
              </Text>
            </View>
          </View>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
