"use client";

import { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Target, Loader2, Download, RefreshCw } from 'lucide-react';
import FileUpload from '@/components/career-tools/FileUpload';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

export default function ATSHackPage() {
  const [resumeText, setResumeText] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [keywords, setKeywords] = useState('');
  const [useTextInput, setUseTextInput] = useState(false);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [optimization, setOptimization] = useState('');

  const handleAnalyze = async () => {
    if (!resumeText.trim() || !jobDescription.trim()) {
      toast.error('Please provide both resume and job description');
      return;
    }

    setIsAnalyzing(true);
    try {
      const keywordsArray = keywords.split(',').map(k => k.trim()).filter(Boolean);
      const response = await api.post('/api/user/career-tools/ats-hack', {
        resume_text: resumeText,
        job_description: jobDescription,
        keywords: keywordsArray,
      });

      if (response.data.success) {
        setOptimization(response.data.optimization);
        toast.success('ATS analysis complete!');
      } else {
        toast.error('Failed to analyze resume');
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Failed to analyze resume');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setResumeText('');
    setJobDescription('');
    setKeywords('');
    setOptimization('');
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([optimization], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'ats-optimization-report.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    toast.success('Report downloaded!');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center space-x-4">
            <Link href="/career-tools" className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
              <ArrowLeft className="w-5 h-5" />
            </Link>
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-purple-100 rounded-lg">
                <Target className="w-6 h-6 text-purple-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">ATS Hack</h1>
                <p className="text-sm text-gray-500">Optimize your resume for ATS</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            {/* Resume Upload */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Your Resume</h2>
              
              <div className="flex space-x-2 mb-4">
                <button
                  onClick={() => setUseTextInput(false)}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    !useTextInput
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Upload File
                </button>
                <button
                  onClick={() => setUseTextInput(true)}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    useTextInput
                      ? 'bg-purple-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Paste Text
                </button>
              </div>

              {!useTextInput ? (
                <FileUpload onFileUpload={setResumeText} />
              ) : (
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste your resume text here..."
                  className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
                />
              )}
            </div>

            {/* Job Description */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Job Description</h2>
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="w-full h-48 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent resize-none"
              />
            </div>

            {/* Additional Keywords */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Additional Keywords (Optional)</h2>
              <input
                type="text"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
                placeholder="e.g., Python, Machine Learning, AWS (comma separated)"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              />
              <p className="text-sm text-gray-500 mt-2">Separate keywords with commas</p>

              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !resumeText.trim() || !jobDescription.trim()}
                className="w-full mt-4 py-3 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Target className="w-5 h-5 mr-2" />
                    Analyze ATS Compatibility
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {optimization ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-bold text-gray-900">Optimization Report</h2>
                  <div className="flex space-x-2">
                    <button
                      onClick={handleDownload}
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="Download report"
                    >
                      <Download className="w-5 h-5" />
                    </button>
                    <button
                      onClick={handleReset}
                      className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                      title="Analyze another"
                    >
                      <RefreshCw className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                <div className="prose max-w-none">
                  <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                    {optimization}
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <Target className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No Analysis Yet
                </h3>
                <p className="text-gray-400">
                  Provide your resume and job description to get ATS optimization tips
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
