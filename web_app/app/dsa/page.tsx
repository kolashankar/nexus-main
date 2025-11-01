'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { Skeleton } from '@/components/ui/Skeleton';
import { Header } from '@/components/common/Header';
import { Footer } from '@/components/common/Footer';
import Link from 'next/link';
import { Code, BookOpen, FileText, Building, ArrowRight, TrendingUp } from 'lucide-react';

export default function DSAPage() {
  const { data, isLoading } = useQuery({
    queryKey: ['dsa-dashboard'],
    queryFn: async () => {
      const response = await apiClient.getDSADashboard();
      return response;
    },
  });

  const dashboardData = data?.data || {};
  const stats = dashboardData.stats || {};
  const topTopics = dashboardData.top_topics || [];
  const topCompanies = dashboardData.top_companies || [];

  const totalProblems = stats.total_questions || 0;
  const totalTopics = stats.total_topics || 0;
  const totalCompanies = stats.total_companies || 0;
  const totalSheets = stats.total_sheets || 0;

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white py-20">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-5xl font-bold mb-4">DSA Corner</h1>
            <p className="text-2xl text-blue-100 mb-8">
              Master Data Structures & Algorithms with {totalProblems}+ coding problems
            </p>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-12">
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="text-3xl font-bold">{totalProblems.toLocaleString()}</div>
                <div className="text-blue-100 text-sm mt-1">Total Problems</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="text-3xl font-bold">{totalTopics}</div>
                <div className="text-blue-100 text-sm mt-1">Topics</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="text-3xl font-bold">{totalCompanies}</div>
                <div className="text-blue-100 text-sm mt-1">Companies</div>
              </div>
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4">
                <div className="text-3xl font-bold">{totalSheets}</div>
                <div className="text-blue-100 text-sm mt-1">Study Sheets</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12">
        {/* Quick Access Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Link href="/dsa/questions">
            <div className="bg-white rounded-xl shadow-sm p-8 hover:shadow-lg transition-all cursor-pointer group border-2 border-transparent hover:border-blue-500">
              <div className="w-14 h-14 rounded-xl bg-blue-100 flex items-center justify-center mb-4 group-hover:bg-blue-600 transition-colors">
                <Code className="w-7 h-7 text-blue-600 group-hover:text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600">
                Problems
              </h3>
              <p className="text-gray-600 mb-4">
                Practice coding
              </p>
              <div className="flex items-center text-blue-600 text-sm font-semibold">
                Browse all problems
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>

          <Link href="/dsa/topics">
            <div className="bg-white rounded-xl shadow-sm p-8 hover:shadow-lg transition-all cursor-pointer group border-2 border-transparent hover:border-green-500">
              <div className="w-14 h-14 rounded-xl bg-green-100 flex items-center justify-center mb-4 group-hover:bg-green-600 transition-colors">
                <BookOpen className="w-7 h-7 text-green-600 group-hover:text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-green-600">
                Topics
              </h3>
              <p className="text-gray-600 mb-4">
                By category
              </p>
              <div className="flex items-center text-green-600 text-sm font-semibold">
                Explore topics
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>

          <Link href="/dsa/companies">
            <div className="bg-white rounded-xl shadow-sm p-8 hover:shadow-lg transition-all cursor-pointer group border-2 border-transparent hover:border-orange-500">
              <div className="w-14 h-14 rounded-xl bg-orange-100 flex items-center justify-center mb-4 group-hover:bg-orange-600 transition-colors">
                <Building className="w-7 h-7 text-orange-600 group-hover:text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-orange-600">
                Companies
              </h3>
              <p className="text-gray-600 mb-4">
                Interview prep
              </p>
              <div className="flex items-center text-orange-600 text-sm font-semibold">
                Company questions
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>

          <Link href="/dsa/sheets">
            <div className="bg-white rounded-xl shadow-sm p-8 hover:shadow-lg transition-all cursor-pointer group border-2 border-transparent hover:border-purple-500">
              <div className="w-14 h-14 rounded-xl bg-purple-100 flex items-center justify-center mb-4 group-hover:bg-purple-600 transition-colors">
                <FileText className="w-7 h-7 text-purple-600 group-hover:text-white" />
              </div>
              <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-purple-600">
                Sheets
              </h3>
              <p className="text-gray-600 mb-4">
                Study guides
              </p>
              <div className="flex items-center text-purple-600 text-sm font-semibold">
                Practice sheets
                <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          </Link>
        </div>

        {/* Popular Topics Section */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Popular Topics</h2>
            <Link href="/dsa/topics" className="text-blue-600 hover:text-blue-700 font-semibold flex items-center">
              View All
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[...Array(8)].map((_, i) => (
                <Skeleton key={i} className="h-20" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {topTopics.length > 0 ? (
                topTopics.map((topic: any) => (
                  <Link
                    key={topic._id}
                    href={`/dsa/topics`}
                    className="bg-white rounded-lg shadow-sm p-4 hover:shadow-md transition-shadow border border-gray-100 hover:border-blue-500"
                  >
                    <div className="font-semibold text-gray-900 mb-1">{topic.name}</div>
                    <div className="text-sm text-gray-600">({topic.question_count || 0} problems)</div>
                  </Link>
                ))
              ) : (
                <div className="col-span-4 text-center py-8 text-gray-500">
                  No topics available yet. Admin needs to create DSA topics.
                </div>
              )}
            </div>
          )}
        </div>

        {/* Top Companies Section */}
        <div className="mb-12">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900">Top Companies</h2>
            <Link href="/dsa/companies" className="text-blue-600 hover:text-blue-700 font-semibold flex items-center">
              View All
              <ArrowRight className="w-4 h-4 ml-1" />
            </Link>
          </div>
          
          {isLoading ? (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {[...Array(6)].map((_, i) => (
                <Skeleton key={i} className="h-32" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
              {topCompanies.length > 0 ? (
                topCompanies.map((company: any) => (
                  <Link
                    key={company._id}
                    href={`/dsa/companies`}
                    className="bg-white rounded-lg shadow-sm p-6 hover:shadow-md transition-all border border-gray-100 hover:border-blue-500 group"
                  >
                    <div className="text-4xl mb-3 text-center">{company.logo || '🏢'}</div>
                    <div className="text-center">
                      <div className="font-bold text-gray-900 mb-1 group-hover:text-blue-600">{company.name}</div>
                      <div className="text-sm text-gray-600">{company.problem_count || 0} problems</div>
                    </div>
                  </Link>
                ))
              ) : (
                <div className="col-span-6 text-center py-8 text-gray-500">
                  No companies available yet. Admin needs to create DSA companies.
                </div>
              )}
            </div>
          )}
        </div>

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-12 text-center text-white">
          <h2 className="text-3xl font-bold mb-4">Ready to Start?</h2>
          <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
            Choose your path to mastering DSA. Start with easy problems or explore specific topics and companies.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/dsa/questions?difficulty=Easy">
              <button className="px-8 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-blue-50 transition-colors">
                Start with Easy
              </button>
            </Link>
            <Link href="/dsa/questions">
              <button className="px-8 py-3 bg-blue-500 text-white rounded-lg font-semibold hover:bg-blue-400 transition-colors border-2 border-white/20">
                Browse All
              </button>
            </Link>
          </div>
        </div>
      </div>
      </div>
      <Footer />
    </>
  );
}