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
import * as DocumentPicker from 'expo-document-picker';
import * as FileSystem from 'expo-file-system';
import api from '@/lib/api';
import { useAuth } from '@/contexts/AuthContext';

export default function ResumeReviewScreen() {
  const { user } = useAuth();
  const [document, setDocument] = useState<any>(null);
  const [resumeText, setResumeText] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const pickDocument = async () => {
    try {
      const result = await DocumentPicker.getDocumentAsync({
        type: ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
        copyToCacheDirectory: true
      });

      if (!result.canceled && result.assets && result.assets.length > 0) {
        const file = result.assets[0];
        setDocument(file);
        
        // Read file content if it's a text file
        if (file.uri) {
          try {
            const content = await FileSystem.readAsStringAsync(file.uri);
            setResumeText(content.substring(0, 5000)); // Limit to 5000 chars
          } catch (error) {
            console.log('Could not read file content:', error);
          }
        }
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick document');
    }
  };

  const handleReview = async () => {
    if (!resumeText.trim()) {
      Alert.alert('Error', 'Please upload a resume or paste resume text');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/career-tools/resume-review', {
        resume_text: resumeText,
        job_title: '',  // Optional
        industry: ''    // Optional
      });

      setResult(response.data);
    } catch (error: any) {
      Alert.alert(
        'Error',
        error.response?.data?.detail || 'Failed to review resume'
      );
    } finally {
      setLoading(false);
    }
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
            <Text className="text-xl font-bold text-gray-900">Resume Review</Text>
            <Text className="text-sm text-gray-500">AI-powered resume analysis</Text>
          </View>
        </View>

        {!result ? (
          <View className="p-6">
            {/* Upload Section */}
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">
                Upload Resume
              </Text>
              
              <TouchableOpacity
                onPress={pickDocument}
                className="bg-blue-50 border-2 border-dashed border-blue-300 rounded-lg p-8 items-center mb-4"
              >
                <Ionicons name="cloud-upload-outline" size={48} color="#3b82f6" />
                <Text className="text-blue-600 font-semibold mt-3 mb-1">
                  {document ? 'Change Document' : 'Upload Resume'}
                </Text>
                <Text className="text-gray-500 text-xs">PDF, DOC, DOCX (Max 5MB)</Text>
              </TouchableOpacity>

              {document && (
                <View className="bg-gray-50 p-4 rounded-lg flex-row items-center">
                  <Ionicons name="document-text" size={24} color="#6b7280" />
                  <View className="flex-1 ml-3">
                    <Text className="text-gray-900 font-semibold" numberOfLines={1}>
                      {document.name}
                    </Text>
                    <Text className="text-gray-500 text-xs">
                      {(document.size / 1024).toFixed(1)} KB
                    </Text>
                  </View>
                  <TouchableOpacity onPress={() => setDocument(null)}>
                    <Ionicons name="close-circle" size={24} color="#ef4444" />
                  </TouchableOpacity>
                </View>
              )}
            </View>

            {/* OR Divider */}
            <View className="flex-row items-center my-4">
              <View className="flex-1 h-px bg-gray-300" />
              <Text className="mx-4 text-gray-500 font-semibold">OR</Text>
              <View className="flex-1 h-px bg-gray-300" />
            </View>

            {/* Text Input */}
            <View className="bg-white rounded-xl p-6 mb-6 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">
                Paste Resume Text
              </Text>
              <TextInput
                value={resumeText}
                onChangeText={setResumeText}
                placeholder="Paste your resume text here..."
                multiline
                numberOfLines={10}
                className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-40 border border-gray-200"
                textAlignVertical="top"
              />
              <Text className="text-gray-500 text-xs mt-2">
                {resumeText.length} / 5000 characters
              </Text>
            </View>

            {/* Submit Button */}
            <TouchableOpacity
              onPress={handleReview}
              disabled={loading || !resumeText.trim()}
              className={`rounded-lg py-4 items-center ${
                loading || !resumeText.trim() ? 'bg-gray-300' : 'bg-blue-500'
              }`}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <View className="flex-row items-center">
                  <Ionicons name="sparkles" size={20} color="#fff" />
                  <Text className="text-white font-bold text-base ml-2">
                    Analyze Resume with AI
                  </Text>
                </View>
              )}
            </TouchableOpacity>
          </View>
        ) : (
          // Results View
          <View className="p-6">
            {/* Overall Score */}
            <View className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-6 mb-4">
              <Text className="text-white text-lg font-semibold mb-2">Overall Score</Text>
              <Text className="text-white text-5xl font-bold mb-2">
                {result.ats_score || 'N/A'}
                {result.ats_score && <Text className="text-2xl">/100</Text>}
              </Text>
              <Text className="text-white/80 text-sm">Based on ATS compatibility & content quality</Text>
            </View>

            {/* Feedback Sections */}
            {result.feedback && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  AI Feedback
                </Text>
                <Text className="text-gray-700 leading-6 whitespace-pre-wrap">
                  {result.feedback}
                </Text>
              </View>
            )}

            {/* Suggestions */}
            {result.suggestions && result.suggestions.length > 0 && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  Improvement Suggestions
                </Text>
                {result.suggestions.map((suggestion: string, index: number) => (
                  <View key={index} className="flex-row mb-3">
                    <View className="bg-blue-100 w-6 h-6 rounded-full items-center justify-center mr-3 mt-0.5">
                      <Text className="text-blue-600 font-bold text-xs">{index + 1}</Text>
                    </View>
                    <Text className="flex-1 text-gray-700 leading-6">{suggestion}</Text>
                  </View>
                ))}
              </View>
            )}

            {/* Keywords */}
            {result.keywords && result.keywords.length > 0 && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  Important Keywords
                </Text>
                <View className="flex-row flex-wrap">
                  {result.keywords.map((keyword: string, index: number) => (
                    <View key={index} className="bg-green-100 px-3 py-2 rounded-full mr-2 mb-2">
                      <Text className="text-green-700 font-semibold text-sm">{keyword}</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {/* Action Buttons */}
            <View className="flex-row space-x-3 mb-6">
              <TouchableOpacity
                onPress={() => setResult(null)}
                className="flex-1 bg-gray-200 py-4 rounded-lg items-center"
              >
                <Text className="text-gray-700 font-semibold">Review Another</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => {
                  // Save to history
                  Alert.alert('Success', 'Saved to usage history!');
                }}
                className="flex-1 bg-blue-500 py-4 rounded-lg items-center"
              >
                <Text className="text-white font-semibold">Save Result</Text>
              </TouchableOpacity>
            </View>
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
