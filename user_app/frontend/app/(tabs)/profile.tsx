import React from 'react';
import { View, Text, TouchableOpacity, ScrollView, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { useAuth } from '../../contexts/AuthContext';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';

export default function ProfileScreen() {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Logout',
        style: 'destructive',
        onPress: async () => {
          await logout();
          router.replace('/(auth)/login');
        },
      },
    ]);
  };

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      <ScrollView className="flex-1">
        {/* Header with Gradient */}
        <LinearGradient
          colors={['#2563eb', '#4f46e5']}
          className="px-6 py-8 mb-6"
        >
          <Text className="text-white text-2xl font-bold mb-6">Profile</Text>
          
          {/* User Info */}
          <View className="items-center">
            <View className="bg-white/20 w-24 h-24 rounded-full items-center justify-center mb-4 border-4 border-white/30">
              <Text className="text-white text-4xl font-bold">
                {user?.full_name?.charAt(0).toUpperCase() || 'U'}
              </Text>
            </View>
            <Text className="text-white text-2xl font-bold">{user?.full_name}</Text>
            <Text className="text-blue-100 text-sm mt-1">{user?.email}</Text>
          </View>
        </LinearGradient>

        {/* Menu Items */}
        <View className="px-4">
          <Text className="text-gray-900 text-lg font-bold mb-3 px-2">Quick Access</Text>
          
          <TouchableOpacity 
            className="bg-white px-6 py-4 rounded-xl mb-3 flex-row items-center justify-between shadow-sm border border-gray-100"
            onPress={() => router.push('/(tabs)/profile/bookmarks')}
          >
            <View className="flex-row items-center">
              <View className="bg-blue-100 w-10 h-10 rounded-lg items-center justify-center">
                <Ionicons name="bookmark-outline" size={22} color="#2563eb" />
              </View>
              <Text className="text-gray-900 ml-4 text-base font-semibold">Bookmarks</Text>
            </View>
            <Ionicons name="chevron-forward" size={22} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity 
            className="bg-white px-6 py-4 rounded-xl mb-3 flex-row items-center justify-between shadow-sm border border-gray-100"
            onPress={() => router.push('/(tabs)/profile/reading-history')}
          >
            <View className="flex-row items-center">
              <View className="bg-green-100 w-10 h-10 rounded-lg items-center justify-center">
                <Ionicons name="time-outline" size={22} color="#16a34a" />
              </View>
              <Text className="text-gray-900 ml-4 text-base font-semibold">Reading History</Text>
            </View>
            <Ionicons name="chevron-forward" size={22} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity 
            onPress={() => router.push('/(tabs)/profile/career-tools')}
          >
            <LinearGradient
              colors={['#3b82f6', '#8b5cf6']}
              className="px-6 py-4 rounded-xl mb-3 flex-row items-center justify-between"
            >
              <View className="flex-row items-center">
                <View className="bg-white/20 w-10 h-10 rounded-lg items-center justify-center">
                  <Ionicons name="sparkles" size={22} color="#fff" />
                </View>
                <Text className="text-white ml-4 text-base font-bold">Career Tools (AI)</Text>
              </View>
              <Ionicons name="chevron-forward" size={22} color="#fff" />
            </LinearGradient>
          </TouchableOpacity>

          <TouchableOpacity 
            className="bg-white px-6 py-4 rounded-xl mb-3 flex-row items-center justify-between shadow-sm border border-gray-100"
            onPress={() => router.push('/(tabs)/settings')}
          >
            <View className="flex-row items-center">
              <View className="bg-gray-100 w-10 h-10 rounded-lg items-center justify-center">
                <Ionicons name="settings-outline" size={22} color="#6b7280" />
              </View>
              <Text className="text-gray-900 ml-4 text-base font-semibold">Settings</Text>
            </View>
            <Ionicons name="chevron-forward" size={22} color="#9ca3af" />
          </TouchableOpacity>

          <TouchableOpacity
            className="bg-red-600 px-6 py-4 rounded-xl mt-6 flex-row items-center justify-center shadow-sm"
            onPress={handleLogout}
          >
            <Ionicons name="log-out-outline" size={22} color="#fff" />
            <Text className="text-white ml-3 text-base font-bold">Logout</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
