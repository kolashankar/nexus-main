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

export default function ATSHackScreen() {
  const [jobDescription, setJobDescription] = useState('');
  const [resumeText, setResumeText] = useState('');
  const [document, setDocument] = useState<any>(null);
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
        
        try {
          const content = await FileSystem.readAsStringAsync(file.uri);
          setResumeText(content.substring(0, 5000));
        } catch (error) {
          console.log('Could not read file:', error);
        }
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to pick document');
    }
  };

  const handleAnalyze = async () => {
    if (!jobDescription.trim() || !resumeText.trim()) {
      Alert.alert('Error', 'Please provide both job description and resume');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/career-tools/ats-hack', {
        job_description: jobDescription,
        resume_text: resumeText
      });
      setResult(response.data);
    } catch (error: any) {
      Alert.alert(
        'Error',
        error.response?.data?.detail || 'Failed to analyze ATS compatibility'
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
            <Text className="text-xl font-bold text-gray-900">ATS Optimizer</Text>
            <Text className="text-sm text-gray-500">Beat applicant tracking systems</Text>
          </View>
        </View>

        {!result ? (
          <View className="p-6">
            {/* Job Description */}
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">
                Job Description *
              </Text>
              <TextInput
                value={jobDescription}
                onChangeText={setJobDescription}
                placeholder="Paste the full job description here..."
                multiline
                numberOfLines={8}
                className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-48 border border-gray-200"
                textAlignVertical="top"
              />
            </View>

            {/* Resume Section */}
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">
                Your Resume *
              </Text>
              
              <TouchableOpacity
                onPress={pickDocument}
                className="bg-purple-50 border-2 border-dashed border-purple-300 rounded-lg p-8 items-center mb-4"
              >
                <Ionicons name="cloud-upload-outline" size={48} color="#8b5cf6" />
                <Text className="text-purple-600 font-semibold mt-3 mb-1">
                  {document ? 'Change Document' : 'Upload Resume'}
                </Text>
                <Text className="text-gray-500 text-xs">PDF, DOC, DOCX (Max 5MB)</Text>
              </TouchableOpacity>

              {document && (
                <View className="bg-gray-50 p-4 rounded-lg flex-row items-center mb-4">
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

              <View className="flex-row items-center my-2">
                <View className="flex-1 h-px bg-gray-300" />
                <Text className="mx-4 text-gray-500 font-semibold text-xs">OR PASTE TEXT</Text>
                <View className="flex-1 h-px bg-gray-300" />
              </View>

              <TextInput
                value={resumeText}
                onChangeText={setResumeText}
                placeholder="Paste your resume text here..."
                multiline
                numberOfLines={6}
                className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-32 border border-gray-200"
                textAlignVertical="top"
              />
            </View>

            {/* Analyze Button */}
            <TouchableOpacity
              onPress={handleAnalyze}
              disabled={loading || !jobDescription.trim() || !resumeText.trim()}
              className={`rounded-lg py-4 items-center ${
                loading || !jobDescription.trim() || !resumeText.trim()
                  ? 'bg-gray-300'
                  : 'bg-purple-500'
              }`}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <View className="flex-row items-center">
                  <Ionicons name="shield-checkmark" size={20} color="#fff" />
                  <Text className="text-white font-bold text-base ml-2">
                    Analyze ATS Compatibility
                  </Text>
                </View>
              )}
            </TouchableOpacity>

            {/* Info Box */}
            <View className="bg-purple-50 p-4 rounded-lg mt-4">
              <Text className="text-purple-900 font-semibold mb-2">🔒 What is ATS?</Text>
              <Text className="text-purple-700 text-sm leading-5">
                Applicant Tracking Systems (ATS) scan resumes for keywords and formatting. 
                This tool helps ensure your resume passes these automated screenings.
              </Text>
            </View>
          </View>
        ) : (
          // Results View
          <View className="p-6">
            {/* Match Score */}
            <View className="bg-gradient-to-r from-purple-500 to-pink-600 rounded-xl p-6 mb-4">
              <Text className="text-white text-lg font-semibold mb-2">Match Score</Text>
              <Text className="text-white text-5xl font-bold mb-2">
                {result.match_percentage || 'N/A'}
                {result.match_percentage && <Text className="text-2xl">%</Text>}
              </Text>
              <Text className="text-white/80 text-sm">Keyword match with job description</Text>
            </View>

            {/* Analysis */}
            {result.analysis && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">Analysis</Text>
                <Text className="text-gray-700 leading-6 whitespace-pre-wrap">
                  {result.analysis}
                </Text>
              </View>
            )}

            {/* Missing Keywords */}
            {result.missing_keywords && result.missing_keywords.length > 0 && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  Missing Keywords
                </Text>
                <View className="flex-row flex-wrap">
                  {result.missing_keywords.map((keyword: string, index: number) => (
                    <View key={index} className="bg-red-100 px-3 py-2 rounded-full mr-2 mb-2">
                      <Text className="text-red-700 font-semibold text-sm">{keyword}</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {/* Matched Keywords */}
            {result.matched_keywords && result.matched_keywords.length > 0 && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  Matched Keywords
                </Text>
                <View className="flex-row flex-wrap">
                  {result.matched_keywords.map((keyword: string, index: number) => (
                    <View key={index} className="bg-green-100 px-3 py-2 rounded-full mr-2 mb-2">
                      <Text className="text-green-700 font-semibold text-sm">{keyword}</Text>
                    </View>
                  ))}
                </View>
              </View>
            )}

            {/* Optimization Tips */}
            {result.optimization_tips && result.optimization_tips.length > 0 && (
              <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
                <Text className="text-lg font-bold text-gray-900 mb-4">
                  Optimization Tips
                </Text>
                {result.optimization_tips.map((tip: string, index: number) => (
                  <View key={index} className="flex-row mb-3">
                    <Ionicons name="bulb" size={20} color="#f59e0b" />
                    <Text className="flex-1 ml-3 text-gray-700 leading-6">{tip}</Text>
                  </View>
                ))}
              </View>
            )}

            {/* Action Buttons */}
            <View className="flex-row space-x-3 mb-6">
              <TouchableOpacity
                onPress={() => setResult(null)}
                className="flex-1 bg-gray-200 py-4 rounded-lg items-center"
              >
                <Text className="text-gray-700 font-semibold">Analyze Another</Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={() => Alert.alert('Success', 'Saved to usage history!')}
                className="flex-1 bg-purple-500 py-4 rounded-lg items-center"
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
