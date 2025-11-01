import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { LinearGradient } from 'expo-linear-gradient';
import { getDSAStats, DSAStats } from '../../../lib/dsaProgress';

export default function DSAScreen() {
  const router = useRouter();
  const [stats, setStats] = useState<DSAStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const dsaStats = await getDSAStats();
      setStats(dsaStats);
    } catch (error) {
      console.error('Error loading DSA stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const sections = [
    {
      title: 'DSA Questions',
      description: 'Practice 3000+ coding problems',
      icon: 'code-slash' as keyof typeof Ionicons.glyphMap,
      route: '/(tabs)/dsa/questions',
      color: 'bg-blue-600',
      gradient: ['#2563eb', '#3b82f6'],
    },
    {
      title: 'Topics',
      description: 'Learn by category',
      icon: 'list' as keyof typeof Ionicons.glyphMap,
      route: '/(tabs)/dsa/topics',
      color: 'bg-green-600',
      gradient: ['#16a34a', '#22c55e'],
    },
    {
      title: 'DSA Sheets',
      description: 'Curated problem collections',
      icon: 'document-text' as keyof typeof Ionicons.glyphMap,
      route: '/(tabs)/dsa/sheets',
      color: 'bg-purple-600',
      gradient: ['#9333ea', '#a855f7'],
    },
    {
      title: 'Company Questions',
      description: 'Interview prep by company',
      icon: 'business' as keyof typeof Ionicons.glyphMap,
      route: '/(tabs)/dsa/companies',
      color: 'bg-orange-600',
      gradient: ['#ea580c', '#f97316'],
    },
  ];

  return (
    <SafeAreaView className="flex-1 bg-gray-50">
      {/* Hero Header */}
      <LinearGradient
        colors={['#2563eb', '#4f46e5', '#6366f1']}
        className="px-6 py-8"
      >
        <Text className="text-white text-3xl font-extrabold mb-2">DSA Corner</Text>
        <Text className="text-blue-100 text-base">Master Technical Interviews</Text>
        
        {/* Stats */}
        <View className="flex-row justify-between mt-6">
          <View className="bg-white/20 rounded-lg p-4 flex-1 mr-2">
            <Text className="text-white text-2xl font-bold">{stats?.totalSolved || 0}</Text>
            <Text className="text-blue-100 text-xs mt-1">Solved</Text>
          </View>
          <View className="bg-white/20 rounded-lg p-4 flex-1 mr-2">
            <Text className="text-white text-2xl font-bold">
              {stats?.totalSolved ? Math.round((stats.totalSolved / (stats.totalSolved + 100)) * 100) : 0}%
            </Text>
            <Text className="text-blue-100 text-xs mt-1">Progress</Text>
          </View>
          <View className="bg-white/20 rounded-lg p-4 flex-1">
            <Text className="text-white text-2xl font-bold">{stats?.streak || 0}</Text>
            <Text className="text-blue-100 text-xs mt-1">Streak</Text>
          </View>
        </View>
      </LinearGradient>

      <ScrollView className="flex-1 px-4 py-6">
        {/* Quick Access */}
        <Text className="text-gray-900 text-xl font-bold mb-4">Quick Access</Text>
        {sections.map((section, index) => (
          <TouchableOpacity
            key={index}
            className="bg-white rounded-2xl p-5 mb-4 flex-row items-center shadow-sm border border-gray-100"
            onPress={() => router.push(section.route as any)}
          >
            <LinearGradient
              colors={section.gradient}
              className="w-14 h-14 rounded-xl items-center justify-center mr-4"
            >
              <Ionicons name={section.icon} size={26} color="#fff" />
            </LinearGradient>
            <View className="flex-1">
              <Text className="text-gray-900 text-lg font-bold">{section.title}</Text>
              <Text className="text-gray-600 text-sm mt-1">{section.description}</Text>
            </View>
            <Ionicons name="chevron-forward" size={24} color="#9ca3af" />
          </TouchableOpacity>
        ))}

        {/* CTA Card */}
        <LinearGradient
          colors={['#1e293b', '#334155']}
          className="rounded-2xl p-6 mt-4"
        >
          <Text className="text-white text-xl font-bold mb-2">Ready to Start?</Text>
          <Text className="text-gray-300 text-sm mb-4">
            Begin your journey to master DSA and ace technical interviews
          </Text>
          <TouchableOpacity 
            className="bg-blue-600 rounded-lg py-3 items-center"
            onPress={() => router.push('/(tabs)/dsa/questions')}
          >
            <Text className="text-white font-bold">Start Practicing</Text>
          </TouchableOpacity>
        </LinearGradient>
      </ScrollView>
    </SafeAreaView>
  );
}