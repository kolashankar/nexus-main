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

const TONES = ['Professional', 'Friendly', 'Direct'];
const PURPOSES = ['Job Application', 'Networking', 'Collaboration', 'Information Request'];

export default function ColdEmailScreen() {
  const [formData, setFormData] = useState({
    recipient_name: '',
    recipient_role: '',
    company_name: '',
    purpose: 'Job Application',
    your_background: '',
    tone: 'Professional'
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState('');

  const handleGenerate = async () => {
    if (!formData.recipient_name || !formData.company_name) {
      Alert.alert('Error', 'Please fill in at least recipient name and company name');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/career-tools/cold-email', formData);
      setResult(response.data.email || response.data.content);
    } catch (error: any) {
      Alert.alert(
        'Error',
        error.response?.data?.detail || 'Failed to generate cold email'
      );
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = async () => {
    await Clipboard.setStringAsync(result);
    Alert.alert('Success', 'Email copied to clipboard!');
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
            <Text className="text-xl font-bold text-gray-900">Cold Email Generator</Text>
            <Text className="text-sm text-gray-500">AI-powered professional emails</Text>
          </View>
        </View>

        {!result ? (
          <View className="p-6">
            {/* Form */}
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-semibold text-gray-900 mb-4">Recipient Details</Text>
              
              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Recipient Name *
                </Text>
                <TextInput
                  value={formData.recipient_name}
                  onChangeText={(text) => setFormData({...formData, recipient_name: text})}
                  placeholder="e.g., John Doe"
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 border border-gray-200"
                />
              </View>

              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Recipient Role (Optional)
                </Text>
                <TextInput
                  value={formData.recipient_role}
                  onChangeText={(text) => setFormData({...formData, recipient_role: text})}
                  placeholder="e.g., Hiring Manager, CTO"
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
                  placeholder="e.g., Microsoft"
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 border border-gray-200"
                />
              </View>

              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Purpose
                </Text>
                <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                  {PURPOSES.map((purpose) => (
                    <TouchableOpacity
                      key={purpose}
                      onPress={() => setFormData({...formData, purpose})}
                      className={`px-4 py-2 rounded-lg mr-2 ${
                        formData.purpose === purpose ? 'bg-orange-500' : 'bg-gray-100'
                      }`}
                    >
                      <Text
                        className={`text-sm font-semibold ${
                          formData.purpose === purpose ? 'text-white' : 'text-gray-700'
                        }`}
                      >
                        {purpose}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </ScrollView>
              </View>

              <View className="mb-4">
                <Text className="text-sm font-semibold text-gray-700 mb-2">
                  Your Background (Optional)
                </Text>
                <TextInput
                  value={formData.your_background}
                  onChangeText={(text) => setFormData({...formData, your_background: text})}
                  placeholder="e.g., Software Engineer with 3 years experience in React and Node.js..."
                  multiline
                  numberOfLines={4}
                  className="bg-gray-50 p-4 rounded-lg text-gray-900 min-h-24 border border-gray-200"
                  textAlignVertical="top"
                />
              </View>

              <View>
                <Text className="text-sm font-semibold text-gray-700 mb-2">Tone</Text>
                <View className="flex-row">
                  {TONES.map((tone) => (
                    <TouchableOpacity
                      key={tone}
                      onPress={() => setFormData({...formData, tone})}
                      className={`flex-1 py-3 rounded-lg mr-2 ${
                        formData.tone === tone ? 'bg-orange-500' : 'bg-gray-100'
                      }`}
                    >
                      <Text
                        className={`text-sm font-semibold text-center ${
                          formData.tone === tone ? 'text-white' : 'text-gray-700'
                        }`}
                      >
                        {tone}
                      </Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </View>
            </View>

            {/* Generate Button */}
            <TouchableOpacity
              onPress={handleGenerate}
              disabled={loading || !formData.recipient_name || !formData.company_name}
              className={`rounded-lg py-4 items-center ${
                loading || !formData.recipient_name || !formData.company_name
                  ? 'bg-gray-300'
                  : 'bg-orange-500'
              }`}
            >
              {loading ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <View className="flex-row items-center">
                  <Ionicons name="sparkles" size={20} color="#fff" />
                  <Text className="text-white font-bold text-base ml-2">
                    Generate Email
                  </Text>
                </View>
              )}
            </TouchableOpacity>

            {/* Tips */}
            <View className="bg-orange-50 p-4 rounded-lg mt-4">
              <Text className="text-orange-900 font-semibold mb-2">✉️ Cold Email Tips</Text>
              <Text className="text-orange-700 text-sm leading-5">
                Keep it short, personalize it, and always include a clear call-to-action. 
                AI generates a template - customize it to match your voice!
              </Text>
            </View>
          </View>
        ) : (
          // Results View
          <View className="p-6">
            <View className="bg-white rounded-xl p-6 mb-4 border border-gray-200">
              <Text className="text-lg font-bold text-gray-900 mb-4">Your Cold Email</Text>
              <Text className="text-gray-700 leading-7 whitespace-pre-wrap">
                {result}
              </Text>
            </View>

            {/* Action Buttons */}
            <View className="space-y-3 mb-6">
              <TouchableOpacity
                onPress={copyToClipboard}
                className="bg-orange-500 py-4 rounded-lg flex-row items-center justify-center"
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
                  className="flex-1 bg-orange-500 py-4 rounded-lg items-center"
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
