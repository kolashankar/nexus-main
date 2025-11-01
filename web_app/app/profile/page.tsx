"use client";

import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/authStore';
import { useBookmarkStore } from '@/store/bookmarkStore';
import { User, BookmarkIcon, FileText, Code, MapPin, Settings, LogOut, TrendingUp } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import toast from 'react-hot-toast';

export default function ProfilePage() {
  const router = useRouter();
  const { user, logout, isAuthenticated } = useAuthStore();
  const { bookmarks } = useBookmarkStore();
  const [stats, setStats] = useState({
    bookmarksCount: 0,
    dsaSolved: 0,
    articlesRead: 0,
    roadmapsInProgress: 0,
  });

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    // Calculate stats
    setStats({
      bookmarksCount: Object.keys(bookmarks).reduce((acc, key) => acc + bookmarks[key].length, 0),
      dsaSolved: 0, // Would come from API
      articlesRead: 0, // Would come from API
      roadmapsInProgress: 0, // Would come from API
    });
  }, [isAuthenticated, bookmarks, router]);

  const handleLogout = () => {
    logout();
    toast.success('Logged out successfully');
    router.push('/login');
  };

  if (!isAuthenticated || !user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Header */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-16 px-4">
        <div className="max-w-7xl mx-auto">
          <div className="flex items-center space-x-6">
            <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-indigo-600 text-3xl font-bold">
              {user.name.charAt(0).toUpperCase()}
            </div>
            <div className="flex-1">
              <h1 className="text-3xl font-bold mb-2">{user.name}</h1>
              <p className="text-indigo-100 flex items-center">
                <User className="w-4 h-4 mr-2" />
                {user.email}
              </p>
            </div>
            <div className="flex space-x-3">
              <Link
                href="/settings"
                className="px-6 py-3 bg-white text-indigo-600 rounded-lg font-medium hover:bg-indigo-50 transition-colors flex items-center"
              >
                <Settings className="w-5 h-5 mr-2" />
                Settings
              </Link>
              <button
                onClick={handleLogout}
                className="px-6 py-3 bg-indigo-700 text-white rounded-lg font-medium hover:bg-indigo-800 transition-colors flex items-center"
              >
                <LogOut className="w-5 h-5 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Statistics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Bookmarks</h3>
              <BookmarkIcon className="w-5 h-5 text-indigo-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats.bookmarksCount}</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">DSA Solved</h3>
              <Code className="w-5 h-5 text-green-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats.dsaSolved}</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Articles Read</h3>
              <FileText className="w-5 h-5 text-blue-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats.articlesRead}</p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-600">Roadmaps</h3>
              <MapPin className="w-5 h-5 text-purple-600" />
            </div>
            <p className="text-3xl font-bold text-gray-900">{stats.roadmapsInProgress}</p>
          </div>
        </div>

        {/* Content Sections */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Bookmarks Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <BookmarkIcon className="w-6 h-6 mr-2 text-indigo-600" />
                Bookmarks
              </h2>
              <Link
                href="/profile/bookmarks"
                className="text-indigo-600 hover:text-indigo-700 font-medium text-sm"
              >
                View All →
              </Link>
            </div>
            
            {stats.bookmarksCount === 0 ? (
              <div className="text-center py-8">
                <BookmarkIcon className="w-12 h-12 text-gray-300 mx-auto mb-3" />
                <p className="text-gray-500">No bookmarks yet</p>
                <p className="text-sm text-gray-400 mt-1">Start bookmarking content you like</p>
              </div>
            ) : (
              <div className="space-y-3">
                {Object.entries(bookmarks).map(([type, items]) => {
                  if (items.length === 0) return null;
                  return (
                    <div key={type} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                      <span className="font-medium text-gray-700 capitalize">{type}</span>
                      <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                        {items.length}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* Reading History Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <FileText className="w-6 h-6 mr-2 text-blue-600" />
                Reading History
              </h2>
              <Link
                href="/profile/reading-history"
                className="text-blue-600 hover:text-blue-700 font-medium text-sm"
              >
                View All →
              </Link>
            </div>
            
            <div className="text-center py-8">
              <FileText className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No reading history yet</p>
              <p className="text-sm text-gray-400 mt-1">Start reading articles to track your progress</p>
            </div>
          </div>

          {/* DSA Progress Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <Code className="w-6 h-6 mr-2 text-green-600" />
                DSA Progress
              </h2>
              <Link
                href="/dsa"
                className="text-green-600 hover:text-green-700 font-medium text-sm"
              >
                View Dashboard →
              </Link>
            </div>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Easy Problems</span>
                  <span className="font-medium text-gray-900">0 / 100</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-green-500 h-2 rounded-full" style={{ width: '0%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Medium Problems</span>
                  <span className="font-medium text-gray-900">0 / 200</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-yellow-500 h-2 rounded-full" style={{ width: '0%' }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-600">Hard Problems</span>
                  <span className="font-medium text-gray-900">0 / 150</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div className="bg-red-500 h-2 rounded-full" style={{ width: '0%' }} />
                </div>
              </div>
            </div>
          </div>

          {/* Career Tools Usage Section */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-900 flex items-center">
                <TrendingUp className="w-6 h-6 mr-2 text-purple-600" />
                Career Tools Usage
              </h2>
              <Link
                href="/career-tools/history"
                className="text-purple-600 hover:text-purple-700 font-medium text-sm"
              >
                View History →
              </Link>
            </div>
            
            <div className="text-center py-8">
              <TrendingUp className="w-12 h-12 text-gray-300 mx-auto mb-3" />
              <p className="text-gray-500">No usage history yet</p>
              <p className="text-sm text-gray-400 mt-1">Start using AI career tools</p>
              <Link
                href="/career-tools"
                className="inline-block mt-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium"
              >
                Explore Career Tools
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
