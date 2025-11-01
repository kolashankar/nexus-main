"use client";

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { FileText, Mail, Target, Sparkles, History, ChevronRight } from 'lucide-react';
import { Header } from '@/components/common/Header';
import { Footer } from '@/components/common/Footer';
import { useAuthStore } from '@/store/authStore';
import toast from 'react-hot-toast';

const tools = [
  {
    id: 'resume-review',
    title: 'Resume Review',
    description: 'Get AI-powered feedback on your resume with ATS optimization tips',
    icon: FileText,
    color: 'from-blue-500 to-blue-600',
    href: '/career-tools/resume-review',
  },
  {
    id: 'cover-letter',
    title: 'Cover Letter Generator',
    description: 'Create professional, personalized cover letters in seconds',
    icon: Mail,
    color: 'from-green-500 to-green-600',
    href: '/career-tools/cover-letter',
  },
  {
    id: 'ats-hack',
    title: 'ATS Hack',
    description: 'Optimize your resume to pass Applicant Tracking Systems',
    icon: Target,
    color: 'from-purple-500 to-purple-600',
    href: '/career-tools/ats-hack',
  },
  {
    id: 'cold-email',
    title: 'Cold Email Generator',
    description: 'Craft compelling outreach emails for networking and opportunities',
    icon: Sparkles,
    color: 'from-orange-500 to-orange-600',
    href: '/career-tools/cold-email',
  },
];

const tips = [
  'All tools are powered by advanced AI for professional results',
  'Your data is secure and never shared with third parties',
  'Save your generated content to history for easy access',
  'Customize tone and style to match your personality',
];

export default function CareerToolsPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      toast.error('Please sign in to use Career Tools');
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null;
  }

  return (
    <>
      <Header />
      <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-white to-purple-50">
        {/* Hero Section */}
        <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-16 px-4">
          <div className="max-w-7xl mx-auto">
            <div className="flex items-center justify-center mb-4">
              <Sparkles className="w-12 h-12" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-center mb-4">
              AI-Powered Career Tools
            </h1>
            <p className="text-xl text-center text-indigo-100 max-w-2xl mx-auto">
              Accelerate your job search with our suite of AI-powered tools designed to help you stand out
            </p>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-4 py-12">
          {/* Tools Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            {tools.map((tool) => {
              const Icon = tool.icon;
              return (
                <Link
                  key={tool.id}
                  href={tool.href}
                  className="group relative bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden"
                >
                  <div className={`absolute inset-0 bg-gradient-to-br ${tool.color} opacity-0 group-hover:opacity-5 transition-opacity`} />
                  <div className="p-6">
                    <div className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${tool.color} text-white mb-4`}>
                      <Icon className="w-6 h-6" />
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors">
                      {tool.title}
                    </h3>
                    <p className="text-gray-600 mb-4">{tool.description}</p>
                    <div className="flex items-center text-indigo-600 font-medium group-hover:translate-x-2 transition-transform">
                      Get Started
                      <ChevronRight className="w-4 h-4 ml-1" />
                    </div>
                  </div>
                </Link>
              );
            })}
          </div>

          {/* Usage History Link */}
          <div className="bg-gradient-to-r from-gray-50 to-gray-100 rounded-xl p-6 mb-12">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4">
                <div className="p-3 bg-white rounded-lg shadow-sm">
                  <History className="w-6 h-6 text-gray-700" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Usage History</h3>
                  <p className="text-gray-600">View all your generated content in one place</p>
                </div>
              </div>
              <Link
                href="/career-tools/history"
                className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
              >
                View History
              </Link>
            </div>
          </div>

          {/* Pro Tips Section */}
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center">
              <Sparkles className="w-6 h-6 text-yellow-500 mr-2" />
              Pro Tips
            </h2>
            <ul className="space-y-3">
              {tips.map((tip, index) => (
                <li key={index} className="flex items-start">
                  <div className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-sm font-bold mr-3 mt-0.5">
                    {index + 1}
                  </div>
                  <p className="text-gray-700">{tip}</p>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
      <Footer />
    </>
  );
}
