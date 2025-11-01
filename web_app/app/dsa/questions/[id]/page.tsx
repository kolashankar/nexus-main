'use client';

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { CodeEditor } from '@/components/dsa/CodeEditor';
import { Button } from '@/components/ui/Button';
import { Skeleton } from '@/components/ui/Skeleton';
import { ArrowLeft, Bookmark, Share2, CheckCircle } from 'lucide-react';
import { DSAQuestion } from '@/types';
import { toast } from 'react-hot-toast';

export default function QuestionDetailPage() {
  const params = useParams();
  const router = useRouter();
  const questionId = params?.id as string;
  const [activeTab, setActiveTab] = useState<'description' | 'solution' | 'hints'>('description');
  const [isBookmarked, setIsBookmarked] = useState(false);

  const { data, isLoading, error } = useQuery({
    queryKey: ['dsa-question', questionId],
    queryFn: async () => {
      const response = await apiClient.getDSAQuestionById(questionId);
      return response;
    },
    enabled: !!questionId,
  });

  const question: DSAQuestion | undefined = data?.data;

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

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <Skeleton className="h-10 w-32 mb-8" />
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Skeleton className="h-96" />
            <Skeleton className="h-96" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !question) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Question not found</h2>
          <Button onClick={() => router.push('/dsa/questions')}>Back to Questions</Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Back Button */}
        <Button
          variant="outline"
          onClick={() => router.push('/dsa/questions')}
          className="mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Questions
        </Button>

        {/* Split Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Side - Problem Description */}
          <div className="bg-white rounded-lg shadow-sm p-6 h-fit">
            {/* Header */}
            <div className="mb-6">
              <div className="flex items-center justify-between mb-4">
                <h1 className="text-2xl font-bold text-gray-900">{question.title}</h1>
                <button
                  onClick={() => {
                    setIsBookmarked(!isBookmarked);
                    toast.success(isBookmarked ? 'Removed from bookmarks' : 'Added to bookmarks');
                  }}
                  className="p-2 hover:bg-gray-100 rounded transition-colors"
                >
                  <Bookmark
                    className={`w-5 h-5 ${
                      isBookmarked ? 'fill-blue-600 text-blue-600' : 'text-gray-400'
                    }`}
                  />
                </button>
              </div>
              <div className="flex items-center space-x-3">
                <span className={`px-3 py-1 text-xs font-medium rounded-full ${getDifficultyColor(question.difficulty)}`}>
                  {question.difficulty}
                </span>
                {question.acceptance_rate && (
                  <span className="text-sm text-gray-500">
                    Acceptance: {question.acceptance_rate}%
                  </span>
                )}
              </div>
            </div>

            {/* Tabs */}
            <div className="border-b mb-6">
              <div className="flex space-x-6">
                <button
                  onClick={() => setActiveTab('description')}
                  className={`pb-3 text-sm font-medium transition-colors ${
                    activeTab === 'description'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Description
                </button>
                <button
                  onClick={() => setActiveTab('solution')}
                  className={`pb-3 text-sm font-medium transition-colors ${
                    activeTab === 'solution'
                      ? 'text-blue-600 border-b-2 border-blue-600'
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Solution
                </button>
                {question.hints && question.hints.length > 0 && (
                  <button
                    onClick={() => setActiveTab('hints')}
                    className={`pb-3 text-sm font-medium transition-colors ${
                      activeTab === 'hints'
                        ? 'text-blue-600 border-b-2 border-blue-600'
                        : 'text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    Hints
                  </button>
                )}
              </div>
            </div>

            {/* Tab Content */}
            {activeTab === 'description' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Problem Statement</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{question.description}</p>
                </div>

                {question.examples && question.examples.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Examples</h3>
                    {question.examples.map((example, idx) => (
                      <div key={idx} className="mb-4 bg-gray-50 p-4 rounded-lg">
                        <p className="text-sm font-medium text-gray-700 mb-1">Example {idx + 1}:</p>
                        <p className="text-sm text-gray-600"><strong>Input:</strong> {example.input}</p>
                        <p className="text-sm text-gray-600"><strong>Output:</strong> {example.output}</p>
                        {example.explanation && (
                          <p className="text-sm text-gray-600 mt-1"><strong>Explanation:</strong> {example.explanation}</p>
                        )}
                      </div>
                    ))}
                  </div>
                )}

                {question.constraints && question.constraints.length > 0 && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Constraints</h3>
                    <ul className="list-disc list-inside space-y-1">
                      {question.constraints.map((constraint, idx) => (
                        <li key={idx} className="text-sm text-gray-700">{constraint}</li>
                      ))}
                    </ul>
                  </div>
                )}

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Topics</h3>
                  <div className="flex flex-wrap gap-2">
                    {question.topics.map((topic, idx) => (
                      <span key={idx} className="px-3 py-1 text-sm bg-blue-50 text-blue-700 rounded-full">
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Companies</h3>
                  <div className="flex flex-wrap gap-2">
                    {question.companies.map((company, idx) => (
                      <span key={idx} className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full">
                        {company}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'solution' && (
              <div className="space-y-6">
                {question.solution_approach && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Solution Approach</h3>
                    <p className="text-gray-700 whitespace-pre-wrap">{question.solution_approach}</p>
                  </div>
                )}

                {(question.time_complexity || question.space_complexity) && (
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Complexity Analysis</h3>
                    {question.time_complexity && (
                      <p className="text-sm text-gray-700 mb-1">
                        <strong>Time Complexity:</strong> {question.time_complexity}
                      </p>
                    )}
                    {question.space_complexity && (
                      <p className="text-sm text-gray-700">
                        <strong>Space Complexity:</strong> {question.space_complexity}
                      </p>
                    )}
                  </div>
                )}
              </div>
            )}

            {activeTab === 'hints' && question.hints && (
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Hints</h3>
                <ol className="list-decimal list-inside space-y-2">
                  {question.hints.map((hint, idx) => (
                    <li key={idx} className="text-gray-700">{hint}</li>
                  ))}
                </ol>
              </div>
            )}
          </div>

          {/* Right Side - Code Editor */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Solution Code</h3>
            {question.code_solutions && question.code_solutions.length > 0 ? (
              <CodeEditor solutions={question.code_solutions} />
            ) : (
              <p className="text-gray-500">No solution available yet</p>
            )}
            
            <div className="mt-6">
              <Button className="w-full bg-green-600 hover:bg-green-700">
                <CheckCircle className="w-4 h-4 mr-2" />
                Mark as Solved
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}