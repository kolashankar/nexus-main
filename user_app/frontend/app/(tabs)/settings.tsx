import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Switch, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuth } from '../../contexts/AuthContext';
import {
  getNotificationPreferences,
  updateNotificationPreferences,
  registerForPushNotifications,
  scheduleDailyDSAChallenge,
  NotificationPreferences,
} from '../../lib/notificationService';
import {
  clearAllCache,
  getCacheSize,
} from '../../lib/cacheManager';
import { clearAllSearchHistory } from '../../lib/searchHistory';

export default function SettingsScreen() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [notificationPrefs, setNotificationPrefs] = useState<NotificationPreferences>({
    enabled: true,
    jobAlerts: true,
    articleUpdates: true,
    dsaChallenge: true,
    roadmapReminders: true,
    careerToolUpdates: true,
  });
  const [cacheSize, setCacheSize] = useState<number>(0);
  const [pushToken, setPushToken] = useState<string | null>(null);

  useEffect(() => {
    loadPreferences();
    loadCacheSize();
  }, []);

  const loadPreferences = async () => {
    const prefs = await getNotificationPreferences();
    setNotificationPrefs(prefs);
  };

  const loadCacheSize = async () => {
    const size = await getCacheSize();
    setCacheSize(size);
  };

  const handleNotificationToggle = async (key: keyof NotificationPreferences) => {
    const newPrefs = { ...notificationPrefs, [key]: !notificationPrefs[key] };
    setNotificationPrefs(newPrefs);
    await updateNotificationPreferences(newPrefs);

    if (key === 'enabled' && newPrefs.enabled) {
      const token = await registerForPushNotifications();
      setPushToken(token);
      await scheduleDailyDSAChallenge();
    }
  };

  const handleClearCache = () => {
    Alert.alert(
      'Clear Cache',
      'This will clear all cached data. You\'ll need to reload content when online.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            await clearAllCache();
            await loadCacheSize();
            Alert.alert('Success', 'Cache cleared successfully');
          },
        },
      ]
    );
  };

  const handleClearSearchHistory = () => {
    Alert.alert(
      'Clear Search History',
      'This will clear all your recent searches.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Clear',
          style: 'destructive',
          onPress: async () => {
            await clearAllSearchHistory();
            Alert.alert('Success', 'Search history cleared');
          },
        },
      ]
    );
  };

  const handleLogout = () => {
    Alert.alert(
      'Logout',
      'Are you sure you want to logout?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Logout',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/');
          },
        },
      ]
    );
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-900">
      <View className="flex-row items-center justify-between px-6 py-4 border-b border-gray-800">
        <Text className="text-white text-2xl font-bold">Settings</Text>
      </View>

      <ScrollView className="flex-1">
        {/* Account Section */}
        <View className="px-6 py-4">
          <Text className="text-gray-400 text-sm font-semibold mb-3">ACCOUNT</Text>
          <View className="bg-gray-800 rounded-lg">
            <View className="flex-row items-center p-4 border-b border-gray-700">
              <Ionicons name="person-circle" size={40} color="#3b82f6" />
              <View className="ml-3 flex-1">
                <Text className="text-white text-base font-semibold">{user?.name}</Text>
                <Text className="text-gray-400 text-sm">{user?.email}</Text>
              </View>
            </View>
            <TouchableOpacity
              onPress={() => router.push('/(tabs)/profile')}
              className="flex-row items-center justify-between p-4"
            >
              <View className="flex-row items-center">
                <Ionicons name="person" size={20} color="#9ca3af" />
                <Text className="text-white text-base ml-3">Edit Profile</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Notifications Section */}
        <View className="px-6 py-4">
          <Text className="text-gray-400 text-sm font-semibold mb-3">NOTIFICATIONS</Text>
          <View className="bg-gray-800 rounded-lg">
            <View className="flex-row items-center justify-between p-4 border-b border-gray-700">
              <View className="flex-row items-center flex-1">
                <Ionicons name="notifications" size={20} color="#9ca3af" />
                <Text className="text-white text-base ml-3">Push Notifications</Text>
              </View>
              <Switch
                value={notificationPrefs.enabled}
                onValueChange={() => handleNotificationToggle('enabled')}
                trackColor={{ false: '#374151', true: '#3b82f6' }}
                thumbColor={notificationPrefs.enabled ? '#60a5fa' : '#9ca3af'}
              />
            </View>
            {notificationPrefs.enabled && (
              <>
                <View className="flex-row items-center justify-between p-4 border-b border-gray-700">
                  <Text className="text-gray-300 text-sm ml-8">Job Alerts</Text>
                  <Switch
                    value={notificationPrefs.jobAlerts}
                    onValueChange={() => handleNotificationToggle('jobAlerts')}
                    trackColor={{ false: '#374151', true: '#3b82f6' }}
                    thumbColor={notificationPrefs.jobAlerts ? '#60a5fa' : '#9ca3af'}
                  />
                </View>
                <View className="flex-row items-center justify-between p-4 border-b border-gray-700">
                  <Text className="text-gray-300 text-sm ml-8">Article Updates</Text>
                  <Switch
                    value={notificationPrefs.articleUpdates}
                    onValueChange={() => handleNotificationToggle('articleUpdates')}
                    trackColor={{ false: '#374151', true: '#3b82f6' }}
                    thumbColor={notificationPrefs.articleUpdates ? '#60a5fa' : '#9ca3af'}
                  />
                </View>
                <View className="flex-row items-center justify-between p-4 border-b border-gray-700">
                  <Text className="text-gray-300 text-sm ml-8">Daily DSA Challenge</Text>
                  <Switch
                    value={notificationPrefs.dsaChallenge}
                    onValueChange={() => handleNotificationToggle('dsaChallenge')}
                    trackColor={{ false: '#374151', true: '#3b82f6' }}
                    thumbColor={notificationPrefs.dsaChallenge ? '#60a5fa' : '#9ca3af'}
                  />
                </View>
                <View className="flex-row items-center justify-between p-4 border-b border-gray-700">
                  <Text className="text-gray-300 text-sm ml-8">Roadmap Reminders</Text>
                  <Switch
                    value={notificationPrefs.roadmapReminders}
                    onValueChange={() => handleNotificationToggle('roadmapReminders')}
                    trackColor={{ false: '#374151', true: '#3b82f6' }}
                    thumbColor={notificationPrefs.roadmapReminders ? '#60a5fa' : '#9ca3af'}
                  />
                </View>
                <View className="flex-row items-center justify-between p-4">
                  <Text className="text-gray-300 text-sm ml-8">Career Tool Updates</Text>
                  <Switch
                    value={notificationPrefs.careerToolUpdates}
                    onValueChange={() => handleNotificationToggle('careerToolUpdates')}
                    trackColor={{ false: '#374151', true: '#3b82f6' }}
                    thumbColor={notificationPrefs.careerToolUpdates ? '#60a5fa' : '#9ca3af'}
                  />
                </View>
              </>
            )}
          </View>
        </View>

        {/* Data & Storage Section */}
        <View className="px-6 py-4">
          <Text className="text-gray-400 text-sm font-semibold mb-3">DATA & STORAGE</Text>
          <View className="bg-gray-800 rounded-lg">
            <View className="p-4 border-b border-gray-700">
              <View className="flex-row items-center justify-between">
                <View className="flex-row items-center flex-1">
                  <Ionicons name="archive" size={20} color="#9ca3af" />
                  <Text className="text-white text-base ml-3">Cache Size</Text>
                </View>
                <Text className="text-gray-400 text-sm">{formatBytes(cacheSize)}</Text>
              </View>
            </View>
            <TouchableOpacity
              onPress={handleClearCache}
              className="flex-row items-center justify-between p-4 border-b border-gray-700"
            >
              <View className="flex-row items-center">
                <Ionicons name="trash-bin" size={20} color="#ef4444" />
                <Text className="text-red-400 text-base ml-3">Clear Cache</Text>
              </View>
            </TouchableOpacity>
            <TouchableOpacity
              onPress={handleClearSearchHistory}
              className="flex-row items-center justify-between p-4"
            >
              <View className="flex-row items-center">
                <Ionicons name="search" size={20} color="#ef4444" />
                <Text className="text-red-400 text-base ml-3">Clear Search History</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>

        {/* About Section */}
        <View className="px-6 py-4">
          <Text className="text-gray-400 text-sm font-semibold mb-3">ABOUT</Text>
          <View className="bg-gray-800 rounded-lg">
            <TouchableOpacity className="flex-row items-center justify-between p-4 border-b border-gray-700">
              <View className="flex-row items-center">
                <Ionicons name="information-circle" size={20} color="#9ca3af" />
                <Text className="text-white text-base ml-3">About CareerGuide</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
            </TouchableOpacity>
            <TouchableOpacity className="flex-row items-center justify-between p-4 border-b border-gray-700">
              <View className="flex-row items-center">
                <Ionicons name="shield-checkmark" size={20} color="#9ca3af" />
                <Text className="text-white text-base ml-3">Privacy Policy</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
            </TouchableOpacity>
            <TouchableOpacity className="flex-row items-center justify-between p-4">
              <View className="flex-row items-center">
                <Ionicons name="document-text" size={20} color="#9ca3af" />
                <Text className="text-white text-base ml-3">Terms of Service</Text>
              </View>
              <Ionicons name="chevron-forward" size={20} color="#9ca3af" />
            </TouchableOpacity>
          </View>
        </View>

        {/* Logout */}
        <View className="px-6 py-4 pb-8">
          <TouchableOpacity
            onPress={handleLogout}
            className="bg-red-600 rounded-lg p-4 flex-row items-center justify-center"
          >
            <Ionicons name="log-out" size={20} color="white" />
            <Text className="text-white text-base font-semibold ml-2">Logout</Text>
          </TouchableOpacity>
        </View>

        <View className="items-center pb-8">
          <Text className="text-gray-500 text-sm">CareerGuide v1.0.0</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
