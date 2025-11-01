'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Article } from '@/types';
import { Clock, Eye, BookOpen, Bookmark, User } from 'lucide-react';
import { formatDate } from '@/lib/utils';
import { toast } from 'react-hot-toast';

interface ArticleCardProps {
  article: Article;
}

export function ArticleCard({ article }: ArticleCardProps) {
  const [isBookmarked, setIsBookmarked] = React.useState(false);

  const handleBookmark = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsBookmarked(!isBookmarked);
    toast.success(isBookmarked ? 'Removed from bookmarks' : 'Added to bookmarks');
  };

  return (
    <Link href={`/learning/articles/${article.id}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer group overflow-hidden">
        {/* Cover Image */}
        {article.cover_image && (
          <div className="w-full h-48 overflow-hidden">
            <img
              src={article.cover_image}
              alt={article.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          </div>
        )}
        
        <div className="p-6">
          {/* Category Badge */}
          <div className="mb-3">
            <span className="inline-block px-3 py-1 text-xs font-medium bg-purple-50 text-purple-700 rounded-full">
              {article.category}
            </span>
          </div>

          {/* Title & Excerpt */}
          <h3 className="text-xl font-semibold text-gray-900 group-hover:text-purple-600 transition-colors line-clamp-2 mb-2">
            {article.title}
          </h3>
          <p className="text-sm text-gray-600 line-clamp-3 mb-4">
            {article.excerpt}
          </p>

          {/* Author & Meta */}
          <div className="flex items-center space-x-4 mb-4">
            <div className="flex items-center space-x-2">
              {article.author_avatar ? (
                <img
                  src={article.author_avatar}
                  alt={article.author}
                  className="w-8 h-8 rounded-full object-cover"
                />
              ) : (
                <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center">
                  <User className="w-4 h-4 text-purple-600" />
                </div>
              )}
              <span className="text-sm text-gray-700 font-medium">{article.author}</span>
            </div>
          </div>

          {/* Stats */}
          <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <Clock className="w-4 h-4 mr-1" />
                {article.read_time} min read
              </div>
              <div className="flex items-center">
                <Eye className="w-4 h-4 mr-1" />
                {article.views_count} views
              </div>
            </div>
            <div className="text-xs text-gray-400">
              {formatDate(article.created_at)}
            </div>
          </div>

          {/* Tags */}
          {article.tags && article.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {article.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                >
                  #{tag}
                </span>
              ))}
              {article.tags.length > 3 && (
                <span className="px-2 py-1 text-xs text-gray-500">
                  +{article.tags.length - 3} more
                </span>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="pt-4 border-t flex items-center justify-between">
            <Button variant="outline" className="flex-1 mr-2 group-hover:bg-purple-50 group-hover:text-purple-600 group-hover:border-purple-600">
              <BookOpen className="w-4 h-4 mr-2" />
              Read Article
            </Button>
            <button
              onClick={handleBookmark}
              className="p-2 hover:bg-gray-100 rounded-full transition-colors"
            >
              <Bookmark
                className={`w-5 h-5 ${
                  isBookmarked ? 'fill-purple-600 text-purple-600' : 'text-gray-400'
                }`}
              />
            </button>
          </div>
        </div>
      </Card>
    </Link>
  );
}
