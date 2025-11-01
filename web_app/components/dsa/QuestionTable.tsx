'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { DSAQuestion } from '@/types';
import { CheckCircle, Circle, AlertCircle, Bookmark } from 'lucide-react';
import { toast } from 'react-hot-toast';

interface QuestionTableProps {
  questions: DSAQuestion[];
}

export function QuestionTable({ questions }: QuestionTableProps) {
  const [bookmarked, setBookmarked] = useState<Set<string>>(new Set());

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy':
        return 'text-green-600 bg-green-50';
      case 'medium':
        return 'text-yellow-600 bg-yellow-50';
      case 'hard':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const handleBookmark = (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    const newBookmarked = new Set(bookmarked);
    if (bookmarked.has(id)) {
      newBookmarked.delete(id);
      toast.success('Removed from bookmarks');
    } else {
      newBookmarked.add(id);
      toast.success('Added to bookmarks');
    }
    setBookmarked(newBookmarked);
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-gray-200 bg-gray-50">
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
              Status
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Title
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-24">
              Difficulty
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Topics
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Companies
            </th>
            <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
              
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {questions.map((question) => (
            <tr key={question.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-4 py-4">
                <Circle className="w-5 h-5 text-gray-400" />
              </td>
              <td className="px-4 py-4">
                <Link href={`/dsa/questions/${question.id}`}>
                  <span className="text-blue-600 hover:text-blue-800 font-medium cursor-pointer">
                    {question.title}
                  </span>
                </Link>
              </td>
              <td className="px-4 py-4">
                <span className={`px-2 py-1 text-xs font-medium rounded-full ${getDifficultyColor(question.difficulty)}`}>
                  {question.difficulty}
                </span>
              </td>
              <td className="px-4 py-4">
                <div className="flex flex-wrap gap-1">
                  {question.topics.slice(0, 2).map((topic, idx) => (
                    <span key={idx} className="px-2 py-1 text-xs bg-blue-50 text-blue-700 rounded">
                      {topic}
                    </span>
                  ))}
                  {question.topics.length > 2 && (
                    <span className="px-2 py-1 text-xs text-gray-500">+{question.topics.length - 2}</span>
                  )}
                </div>
              </td>
              <td className="px-4 py-4">
                <div className="flex flex-wrap gap-1">
                  {question.companies.slice(0, 2).map((company, idx) => (
                    <span key={idx} className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded">
                      {company}
                    </span>
                  ))}
                  {question.companies.length > 2 && (
                    <span className="px-2 py-1 text-xs text-gray-500">+{question.companies.length - 2}</span>
                  )}
                </div>
              </td>
              <td className="px-4 py-4">
                <button
                  onClick={(e) => handleBookmark(question.id, e)}
                  className="p-1 hover:bg-gray-200 rounded transition-colors"
                >
                  <Bookmark
                    className={`w-5 h-5 ${
                      bookmarked.has(question.id) ? 'fill-blue-600 text-blue-600' : 'text-gray-400'
                    }`}
                  />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}