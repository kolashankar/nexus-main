"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, BookmarkIcon, Briefcase, GraduationCap, DollarSign, FileText, Code, MapPin, Trash2 } from 'lucide-react';
import { useBookmarkStore } from '@/store/bookmarkStore';
import toast from 'react-hot-toast';

type BookmarkType = 'jobs' | 'internships' | 'scholarships' | 'articles' | 'dsa' | 'roadmaps' | 'all';

const typeConfig = {
  jobs: { label: 'Jobs', icon: Briefcase, color: 'blue' },
  internships: { label: 'Internships', icon: GraduationCap, color: 'green' },
  scholarships: { label: 'Scholarships', icon: DollarSign, color: 'purple' },
  articles: { label: 'Articles', icon: FileText, color: 'indigo' },
  dsa: { label: 'DSA Questions', icon: Code, color: 'green' },
  roadmaps: { label: 'Roadmaps', icon: MapPin, color: 'purple' },
};

export default function BookmarksPage() {
  const router = useRouter();
  const { bookmarks, removeBookmark } = useBookmarkStore();
  const [filterType, setFilterType] = useState<BookmarkType>('all');

  const getFilteredBookmarks = () => {
    if (filterType === 'all') {
      return Object.entries(bookmarks).flatMap(([type, items]) =>
        items.map((id: string) => ({ type, id }))
      );
    }
    return (bookmarks[filterType] || []).map((id: string) => ({ type: filterType, id }));
  };

  const filteredBookmarks = getFilteredBookmarks();

  const handleRemove = (type: string, id: string) => {
    removeBookmark(type, id);
    toast.success('Bookmark removed');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/profile" className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-indigo-100 rounded-lg">
                  <BookmarkIcon className="w-6 h-6 text-indigo-600" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">My Bookmarks</h1>
                  <p className="text-sm text-gray-500">{filteredBookmarks.length} items</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Filter Buttons */}
        <div className="flex flex-wrap gap-2 mb-6">
          <button
            onClick={() => setFilterType('all')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              filterType === 'all'
                ? 'bg-indigo-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
            }`}
          >
            All ({Object.values(bookmarks).flat().length})
          </button>
          {Object.entries(typeConfig).map(([type, config]) => (
            <button
              key={type}
              onClick={() => setFilterType(type as BookmarkType)}
              className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                filterType === type
                  ? `bg-${config.color}-600 text-white`
                  : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-300'
              }`}
            >
              {config.label} ({bookmarks[type]?.length || 0})
            </button>
          ))}
        </div>

        {/* Bookmarks Grid */}
        {filteredBookmarks.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <BookmarkIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-500 mb-2">No Bookmarks Found</h3>
            <p className="text-gray-400 mb-4">
              {filterType === 'all'
                ? 'Start bookmarking content you like'
                : `No ${typeConfig[filterType as keyof typeof typeConfig]?.label} bookmarks found`}
            </p>
            <Link
              href="/"
              className="inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Explore Content
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {filteredBookmarks.map((bookmark, index) => {
              const config = typeConfig[bookmark.type as keyof typeof typeConfig];
              const Icon = config?.icon || BookmarkIcon;

              return (
                <div
                  key={`${bookmark.type}-${bookmark.id}-${index}`}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className={`p-3 bg-${config?.color || 'indigo'}-100 rounded-lg flex-shrink-0`}>
                        <Icon className={`w-6 h-6 text-${config?.color || 'indigo'}-600`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <span className={`px-2 py-1 bg-${config?.color || 'indigo'}-100 text-${config?.color || 'indigo'}-700 text-xs font-medium rounded`}>
                            {config?.label || bookmark.type}
                          </span>
                        </div>
                        <h3 className="font-bold text-gray-900 mb-2">Bookmarked Item #{bookmark.id}</h3>
                        <p className="text-gray-600 text-sm line-clamp-2">
                          This is a bookmarked {bookmark.type} item. Click to view details.
                        </p>
                        <div className="flex space-x-3 mt-3">
                          <Link
                            href={`/${bookmark.type}/${bookmark.id}`}
                            className="text-indigo-600 hover:text-indigo-700 font-medium text-sm"
                          >
                            View Details →
                          </Link>
                        </div>
                      </div>
                    </div>
                    <button
                      onClick={() => handleRemove(bookmark.type, bookmark.id)}
                      className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Remove bookmark"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
