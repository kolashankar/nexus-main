import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { 
  getInProgressArticles, 
  getCompletedArticles, 
  clearArticleProgress,
  ArticleProgress 
} from '../../../lib/readProgress';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';

export default function ReadingHistoryScreen() {
  const [inProgress, setInProgress] = useState<ArticleProgress[]>([]);
  const [completed, setCompleted] = useState<ArticleProgress[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'in-progress' | 'completed'>('in-progress');
  const router = useRouter();

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const inProgressData = await getInProgressArticles();
      const completedData = await getCompletedArticles();
      setInProgress(inProgressData);
      setCompleted(completedData);
    } catch (error) {
      console.error('Error loading reading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleClearProgress = async (articleId: string) => {
    Alert.alert('Clear Progress', 'Are you sure you want to remove this article from your history?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Remove',
        style: 'destructive',
        onPress: async () => {
          const success = await clearArticleProgress(articleId);
          if (success) {
            setInProgress((prev) => prev.filter((a) => a.articleId !== articleId));
            setCompleted((prev) => prev.filter((a) => a.articleId !== articleId));
          }
        },
      },
    ]);
  };

  const handleArticlePress = (articleId: string) => {
    router.push(`/(tabs)/learning/${articleId}`);
  };

  const getProgressPercentage = (progress: ArticleProgress) => {
    if (!progress.scrollProgress) return 0;
    return Math.round(progress.scrollProgress * 100);
  };

  const displayList = activeTab === 'in-progress' ? inProgress : completed;

  if (loading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading reading history..." />
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
        <Text className="text-white text-xl font-bold">Reading History</Text>
      </View>

      {/* Tabs */}
      <View className="flex-row px-4 py-3 border-b border-gray-700">
        <TouchableOpacity
          className={`flex-1 py-3 rounded-lg mr-2 ${
            activeTab === 'in-progress' ? 'bg-yellow-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('in-progress')}
        >
          <Text
            className={`text-center font-semibold ${
              activeTab === 'in-progress' ? 'text-white' : 'text-gray-400'
            }`}
          >
            In Progress ({inProgress.length})
          </Text>
        </TouchableOpacity>

        <TouchableOpacity
          className={`flex-1 py-3 rounded-lg ${
            activeTab === 'completed' ? 'bg-green-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('completed')}
        >
          <Text
            className={`text-center font-semibold ${
              activeTab === 'completed' ? 'text-white' : 'text-gray-400'
            }`}
          >
            Completed ({completed.length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Articles List */}
      <ScrollView className="flex-1 px-4 py-4">
        {displayList.length === 0 ? (
          <EmptyState
            icon={activeTab === 'in-progress' ? 'book-outline' : 'checkmark-circle-outline'}
            title={activeTab === 'in-progress' ? 'No Articles in Progress' : 'No Completed Articles'}
            message={
              activeTab === 'in-progress'
                ? 'Start reading an article to track your progress!'
                : 'Complete your first article to see it here!'
            }
          />
        ) : (
          displayList.map((article) => (
            <TouchableOpacity
              key={article.articleId}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => handleArticlePress(article.articleId)}
            >
              <View className="flex-row items-start justify-between mb-2">
                <View className="flex-1 mr-3">
                  <Text className="text-white text-base font-bold" numberOfLines={2}>
                    {article.articleTitle}
                  </Text>
                  {article.articleAuthor && (
                    <Text className="text-gray-400 text-sm mt-1">By {article.articleAuthor}</Text>
                  )}
                </View>
                <TouchableOpacity onPress={() => handleClearProgress(article.articleId)}>
                  <Ionicons name="trash-outline" size={22} color="#ef4444" />
                </TouchableOpacity>
              </View>

              {/* Progress Bar */}
              {activeTab === 'in-progress' && (
                <View className="mt-3">
                  <View className="flex-row justify-between mb-1">
                    <Text className="text-gray-400 text-xs">Progress</Text>
                    <Text className="text-gray-400 text-xs">
                      {getProgressPercentage(article)}%
                    </Text>
                  </View>
                  <View className="bg-dark-300 rounded-full h-2">
                    <View
                      className="bg-yellow-600 rounded-full h-2"
                      style={{ width: `${getProgressPercentage(article)}%` }}
                    />
                  </View>
                </View>
              )}

              {/* Timestamps */}
              <View className="flex-row items-center justify-between mt-3">
                {activeTab === 'in-progress' ? (
                  <View className="flex-row items-center">
                    <Ionicons name="time-outline" size={14} color="#ca8a04" />
                    <Text className="text-yellow-600 text-xs ml-1">
                      Last read {new Date(article.lastReadAt).toLocaleDateString()}
                    </Text>
                  </View>
                ) : (
                  <View className="flex-row items-center">
                    <Ionicons name="checkmark-circle" size={14} color="#10b981" />
                    <Text className="text-green-600 text-xs ml-1">
                      Completed {article.completedAt ? new Date(article.completedAt).toLocaleDateString() : ''}
                    </Text>
                  </View>
                )}
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
