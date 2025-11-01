import React, { useState, useEffect } from 'react';
import { View, Text, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';
import { getAllBookmarks, removeBookmark } from '../../../lib/bookmarks';
import LoadingSpinner from '../../../components/common/LoadingSpinner';
import EmptyState from '../../../components/common/EmptyState';

type BookmarkType = 'job' | 'internship' | 'scholarship' | 'article' | 'question' | 'roadmap';

interface Bookmark {
  id: string;
  type: BookmarkType;
  data: any;
  savedAt: number;
}

export default function BookmarksScreen() {
  const [bookmarks, setBookmarks] = useState<Bookmark[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'all' | BookmarkType>('all');
  const router = useRouter();

  useEffect(() => {
    loadBookmarks();
  }, []);

  const loadBookmarks = async () => {
    try {
      const allBookmarks = await getAllBookmarks();
      setBookmarks(allBookmarks);
    } catch (error) {
      console.error('Error loading bookmarks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRemoveBookmark = async (id: string) => {
    Alert.alert('Remove Bookmark', 'Are you sure you want to remove this bookmark?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Remove',
        style: 'destructive',
        onPress: async () => {
          const success = await removeBookmark(id);
          if (success) {
            setBookmarks((prev) => prev.filter((b) => b.id !== id));
          }
        },
      },
    ]);
  };

  const handleBookmarkPress = (bookmark: Bookmark) => {
    switch (bookmark.type) {
      case 'job':
        router.push(`/(tabs)/jobs/${bookmark.id}`);
        break;
      case 'internship':
        router.push(`/(tabs)/jobs/internship-${bookmark.id}`);
        break;
      case 'scholarship':
        router.push(`/(tabs)/jobs/scholarship-${bookmark.id}`);
        break;
      case 'article':
        router.push(`/(tabs)/learning/${bookmark.id}`);
        break;
      case 'question':
        router.push(`/(tabs)/dsa/question-${bookmark.id}`);
        break;
      case 'roadmap':
        router.push(`/(tabs)/roadmaps/${bookmark.id}`);
        break;
    }
  };

  const getFilteredBookmarks = () => {
    if (activeTab === 'all') return bookmarks;
    return bookmarks.filter((b) => b.type === activeTab);
  };

  const getTypeColor = (type: BookmarkType) => {
    switch (type) {
      case 'job':
        return 'bg-blue-600';
      case 'internship':
        return 'bg-green-600';
      case 'scholarship':
        return 'bg-purple-600';
      case 'article':
        return 'bg-orange-600';
      case 'question':
        return 'bg-pink-600';
      case 'roadmap':
        return 'bg-indigo-600';
      default:
        return 'bg-gray-600';
    }
  };

  const getTypeName = (type: BookmarkType) => {
    return type.charAt(0).toUpperCase() + type.slice(1);
  };

  const filteredBookmarks = getFilteredBookmarks();

  if (loading) {
    return (
      <SafeAreaView className="flex-1 bg-dark-400">
        <LoadingSpinner message="Loading bookmarks..." />
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
        <Text className="text-white text-xl font-bold">Bookmarks</Text>
      </View>

      {/* Tabs */}
      <ScrollView horizontal showsHorizontalScrollIndicator={false} className="px-4 py-3 border-b border-gray-700">
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            activeTab === 'all' ? 'bg-primary-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('all')}
        >
          <Text className="text-white font-semibold">All ({bookmarks.length})</Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            activeTab === 'job' ? 'bg-blue-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('job')}
        >
          <Text className="text-white font-semibold">
            Jobs ({bookmarks.filter((b) => b.type === 'job').length})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            activeTab === 'internship' ? 'bg-green-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('internship')}
        >
          <Text className="text-white font-semibold">
            Internships ({bookmarks.filter((b) => b.type === 'internship').length})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full mr-2 ${
            activeTab === 'scholarship' ? 'bg-purple-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('scholarship')}
        >
          <Text className="text-white font-semibold">
            Scholarships ({bookmarks.filter((b) => b.type === 'scholarship').length})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          className={`px-4 py-2 rounded-full ${
            activeTab === 'article' ? 'bg-orange-600' : 'bg-dark-200'
          }`}
          onPress={() => setActiveTab('article')}
        >
          <Text className="text-white font-semibold">
            Articles ({bookmarks.filter((b) => b.type === 'article').length})
          </Text>
        </TouchableOpacity>
      </ScrollView>

      {/* Bookmarks List */}
      <ScrollView className="flex-1 px-4 py-4">
        {filteredBookmarks.length === 0 ? (
          <EmptyState
            icon="bookmark-outline"
            title="No Bookmarks"
            message={
              activeTab === 'all'
                ? 'You haven\'t saved any bookmarks yet. Start exploring!'
                : `No ${getTypeName(activeTab as BookmarkType)} bookmarks saved.`
            }
          />
        ) : (
          filteredBookmarks.map((bookmark) => (
            <TouchableOpacity
              key={bookmark.id}
              className="bg-dark-200 rounded-lg p-4 mb-3"
              onPress={() => handleBookmarkPress(bookmark)}
            >
              <View className="flex-row items-start justify-between mb-2">
                <View className="flex-1 mr-3">
                  <Text className="text-white text-base font-bold" numberOfLines={2}>
                    {bookmark.data.title || bookmark.data.name}
                  </Text>
                  {bookmark.data.company_name && (
                    <Text className="text-gray-400 text-sm mt-1">
                      {bookmark.data.company_name}
                    </Text>
                  )}
                  {bookmark.data.organization_name && (
                    <Text className="text-gray-400 text-sm mt-1">
                      {bookmark.data.organization_name}
                    </Text>
                  )}
                  {bookmark.data.author && (
                    <Text className="text-gray-400 text-sm mt-1">By {bookmark.data.author}</Text>
                  )}
                </View>
                <TouchableOpacity onPress={() => handleRemoveBookmark(bookmark.id)}>
                  <Ionicons name="trash-outline" size={22} color="#ef4444" />
                </TouchableOpacity>
              </View>

              <View className="flex-row items-center justify-between mt-2">
                <View className={`${getTypeColor(bookmark.type)} px-3 py-1 rounded-full`}>
                  <Text className="text-white text-xs font-semibold">
                    {getTypeName(bookmark.type)}
                  </Text>
                </View>
                <Text className="text-gray-500 text-xs">
                  Saved {new Date(bookmark.savedAt).toLocaleDateString()}
                </Text>
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </SafeAreaView>
  );
}
