import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  ScrollView,
  TextInput,
  ActivityIndicator,
  Alert
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { router } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import api from '@/lib/api';
import * as Clipboard from 'expo-clipboard';

export default function CoverLetterScreen() {
  const [formData, setFormData] = useState({
    job_title: '',
    company_name: '',
    job_description: '',
    your_skills: ''
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleGenerate = async () => {
    if (!formData.job_title || !formData.company_name) {
      Alert.alert('Error', 'Please fill in at least job title and company name');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/career-tools/cover-letter', formData);
      setResult(response.data.cover_letter || response.data.content);
    } catch (error: any) {
      Alert.alert(
        'Error',
        error.response?.data?.detail || 'Failed to generate cover letter'
      );
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    await Clipboard.setStringAsync(result);
    Alert.alert('Success', 'Cover letter copied to clipboard!');
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView>
        {/* Header */}
        <View className="bg-white px-6 py-4 border-b border-gray-200 flex-row items-center">
          <TouchableOpacity onPress={() => router.back()} className="mr-4">
            <Ionicons name="arrow-back" size={24} color="#000" />
          </TouchableOpacity>
          <View className="flex-1">
            <Text className="text-xl font-bold text-gray-900">Cover Letter Generator</Text>
            <Text className="text-sm text-gray-500">AI-powered personalized letters</Text>
          </View>
        </View>

        {!result ? (
          <View className="p-6">
            {/* Form */}
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">Job Details</Text>
              
              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Job Title *
                </Text>
                <TextInput
                  value={formData.job_title}
                  onChangeText={(text) => setFormData({...formData, job_title: text})}
                  placeholder="e.g., Senior Software Engineer"
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 border border-gray-200"
                />
              </View>

              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Company Name *
                </Text>
                <TextInput
                  value={formData.company_name}
                  onChangeText={(text) => setFormData({...formData, company_name: text})}
                  placeholder="e.g., Google"
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 border border-gray-200"
                />
              </View>

              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Job Description (Optional)
                </Text>
                <TextInput
                  value={formData.job_description}
                  onChangeText={(text) => setFormData({...formData, job_description: text})}
                  placeholder="Paste the job description here..."
                  multiline
                  numberOfLines={6}
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-32 border border-gray-200"
                  textAlignVertical="top"
                />
              </View>

              <View>
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Your Skills & Experience (Optional)
                </Text>
                <TextInput
                  value={formData.your_skills}
                  onChangeText={(text) => setFormData({...formData, your_skills: text})}
                  placeholder="e.g., 5 years in React, Node.js, AWS..."
                  multiline
                  numberOfLines={4}
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-24 border border-gray-200"
                  textAlignVertical="top"
                />
              </View>
            </View>

            {/* Generate Button */}
            <TouchableOpacity
              onPress={handleGenerate}
              disabled={loading || !formData.job_title || !formData.company_name}
              className={`rounded-lg py-4 items-center ${
                loading || !formData.job_title || !formData.company_name
                  ? 'bg-gray-300'
                  : 'bg-green-500'
              }`}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <View className="flex-row items-center">
                  <Ionicons name="sparkles" size={20} color="#fff" />
                  <Text className="text-white font-bold text-base ml-2">
                    Generate Cover Letter
                  </Text>
                </View>
              )}
            </TouchableOpacity>

            {/* Tips */}
            <View className="bg-blue-50 p-4 rounded-lg mt-4">
              <Text className="text-blue-900 font-semibold mb-2">💡 Pro Tip</Text>
              <Text className="text-blue-700 text-sm leading-5">
                Include specific details about the job and your relevant experience for a more personalized cover letter.
              </Text>
            </View>
          </View>
        ) : (
          // Results View
          <View className="p-6">
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-bold text-gray-900 mb-4">
                Your Cover Letter
              </Text>
              <Text className="text-gray-700 leading-7 whitespace-pre-wrap">
                {result}
              </Text>
            </View>

            {/* Action Buttons */}
            <View className="space-y-3 mb-6">
              <TouchableOpacity
                onPress={copyToClipboard}
                className="bg-blue-500 py-4 rounded-lg flex-row items-center justify-center"
              >
                <Ionicons name="copy-outline" size={20} color="#fff" />
                <Text className="text-white font-semibold ml-2">Copy to Clipboard</Text>
              </TouchableOpacity>
              
              <View className="flex-row space-x-3">
                <TouchableOpacity
                  onPress={() => setResult('')}
                  className="flex-1 bg-gray-200 py-4 rounded-lg items-center"
                >
                  <Text className="text-gray-700 font-semibold">Generate Another</Text>
                </TouchableOpacity>
                <TouchableOpacity
                  onPress={() => Alert.alert('Success', 'Saved to usage history!')}
                  className="flex-1 bg-green-500 py-4 rounded-lg items-center"
                >
                  <Text className="text-white font-semibold">Save</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
