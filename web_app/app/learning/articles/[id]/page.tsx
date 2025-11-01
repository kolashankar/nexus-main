'use client';

import React from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { ReadingProgress } from '@/components/learning/ReadingProgress';
import { TableOfContents } from '@/components/learning/TableOfContents';
import { Button } from '@/components/ui/Button';
import { Skeleton } from '@/components/ui/Skeleton';
import ReactMarkdown from 'react-markdown';
import { 
  ArrowLeft, 
  Clock, 
  Eye, 
  User, 
  Share2, 
  Bookmark, 
  Printer,
  Facebook,
  Twitter,
  Linkedin
} from 'lucide-react';
import { formatDate } from '@/lib/utils';
import { toast } from 'react-hot-toast';
import { Article } from '@/types';

export default function ArticleDetailPage() {
  const params = useParams();
  const router = useRouter();
  const articleId = params?.id as string;
  const [isBookmarked, setIsBookmarked] = React.useState(false);
  const [showShareMenu, setShowShareMenu] = React.useState(false);

  const { data, isLoading, error } = useQuery({
    queryKey: ['article', articleId],
    queryFn: async () => {
      const response = await apiClient.getArticleById(articleId);
      return response;
    },
    enabled: !!articleId,
  });

  const article: Article | undefined = data?.data;

  const handleBookmark = () => {
    setIsBookmarked(!isBookmarked);
    toast.success(isBookmarked ? 'Removed from bookmarks' : 'Added to bookmarks');
  };

  const handleShare = async (platform?: string) => {
    const url = window.location.href;
    const text = article?.title || '';

    if (platform === 'twitter') {
      window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
    } else if (platform === 'facebook') {
      window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
    } else if (platform === 'linkedin') {
      window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`, '_blank');
    } else {
      // Native share or copy to clipboard
      if (navigator.share) {
        try {
          await navigator.share({ title: text, url });
        } catch (err) {
          // User cancelled
        }
      } else {
        await navigator.clipboard.writeText(url);
        toast.success('Link copied to clipboard!');
      }
    }
    setShowShareMenu(false);
  };

  const handlePrint = () => {
    window.print();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <Skeleton className="h-10 w-32 mb-8" />
          <div className="max-w-4xl mx-auto">
            <Skeleton className="h-12 w-full mb-4" />
            <Skeleton className="h-6 w-2/3 mb-8" />
            <Skeleton className="h-96 w-full" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Article not found</h2>
          <Button onClick={() => router.push('/learning')}>Back to Articles</Button>
        </div>
      </div>
    );
  }

  return (
    <>
      <ReadingProgress />
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          {/* Back Button */}
          <Button
            variant="outline"
            onClick={() => router.push('/learning')}
            className="mb-8"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Articles
          </Button>

          <div className="flex gap-8">
            {/* Main Content */}
            <div className="flex-1 max-w-4xl">
              {/* Article Header */}
              <article className="bg-white rounded-lg shadow-sm p-8 mb-6">
                {/* Category Badge */}
                <span className="inline-block px-3 py-1 text-xs font-medium bg-purple-50 text-purple-700 rounded-full mb-4">
                  {article.category}
                </span>

                {/* Title */}
                <h1 className="text-4xl font-bold text-gray-900 mb-4">
                  {article.title}
                </h1>

                {/* Meta Info */}
                <div className="flex flex-wrap items-center gap-6 mb-6 pb-6 border-b">
                  {/* Author */}
                  <div className="flex items-center space-x-3">
                    {article.author_avatar ? (
                      <img
                        src={article.author_avatar}
                        alt={article.author}
                        className="w-12 h-12 rounded-full object-cover"
                      />
                    ) : (
                      <div className="w-12 h-12 rounded-full bg-purple-100 flex items-center justify-center">
                        <User className="w-6 h-6 text-purple-600" />
                      </div>
                    )}
                    <div>
                      <p className="text-sm font-medium text-gray-900">{article.author}</p>
                      <p className="text-xs text-gray-500">{formatDate(article.created_at)}</p>
                    </div>
                  </div>

                  {/* Stats */}
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <div className="flex items-center">
                      <Clock className="w-4 h-4 mr-1" />
                      {article.read_time} min read
                    </div>
                    <div className="flex items-center">
                      <Eye className="w-4 h-4 mr-1" />
                      {article.views_count} views
                    </div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="flex items-center justify-between mb-8">
                  <div className="flex items-center space-x-3">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handleBookmark}
                    >
                      <Bookmark
                        className={`w-4 h-4 mr-2 ${
                          isBookmarked ? 'fill-purple-600 text-purple-600' : ''
                        }`}
                      />
                      {isBookmarked ? 'Saved' : 'Save'}
                    </Button>

                    <div className="relative">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => setShowShareMenu(!showShareMenu)}
                      >
                        <Share2 className="w-4 h-4 mr-2" />
                        Share
                      </Button>

                      {showShareMenu && (
                        <div className="absolute top-full left-0 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-10 min-w-[200px]">
                          <button
                            onClick={() => handleShare('twitter')}
                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                          >
                            <Twitter className="w-4 h-4 mr-2" />
                            Share on Twitter
                          </button>
                          <button
                            onClick={() => handleShare('facebook')}
                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                          >
                            <Facebook className="w-4 h-4 mr-2" />
                            Share on Facebook
                          </button>
                          <button
                            onClick={() => handleShare('linkedin')}
                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50 flex items-center"
                          >
                            <Linkedin className="w-4 h-4 mr-2" />
                            Share on LinkedIn
                          </button>
                          <button
                            onClick={() => handleShare()}
                            className="w-full px-4 py-2 text-left text-sm hover:bg-gray-50"
                          >
                            Copy Link
                          </button>
                        </div>
                      )}
                    </div>

                    <Button
                      variant="outline"
                      size="sm"
                      onClick={handlePrint}
                    >
                      <Printer className="w-4 h-4 mr-2" />
                      Print
                    </Button>
                  </div>
                </div>

                {/* Cover Image */}
                {article.cover_image && (
                  <div className="mb-8 rounded-lg overflow-hidden">
                    <img
                      src={article.cover_image}
                      alt={article.title}
                      className="w-full h-auto"
                    />
                  </div>
                )}

                {/* Article Content */}
                <div className="prose prose-lg max-w-none">
                  <ReactMarkdown
                    components={{
                      h1: ({ node, ...props }) => <h1 id={props.children?.toString().toLowerCase().replace(/[^a-z0-9]+/g, '-')} {...props} />,
                      h2: ({ node, ...props }) => <h2 id={props.children?.toString().toLowerCase().replace(/[^a-z0-9]+/g, '-')} {...props} />,
                      h3: ({ node, ...props }) => <h3 id={props.children?.toString().toLowerCase().replace(/[^a-z0-9]+/g, '-')} {...props} />,
                    }}
                  >
                    {article.content}
                  </ReactMarkdown>
                </div>

                {/* Tags */}
                {article.tags && article.tags.length > 0 && (
                  <div className="mt-8 pt-8 border-t">
                    <h3 className="text-sm font-semibold text-gray-900 mb-3">Tags</h3>
                    <div className="flex flex-wrap gap-2">
                      {article.tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-purple-50 hover:text-purple-700 cursor-pointer transition-colors"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </article>
            </div>

            {/* Sidebar - Table of Contents */}
            <div className="hidden lg:block w-80">
              <TableOfContents content={article.content} />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
