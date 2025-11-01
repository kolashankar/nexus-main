"use client";

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ArrowLeft, FileText, Loader2, Download, Save, RefreshCw } from 'lucide-react';
import FileUpload from '@/components/career-tools/FileUpload';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';

export default function ResumeReviewPage() {
  const router = useRouter();
  const [resumeText, setResumeText] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [industry, setIndustry] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState('');
  const [useTextInput, setUseTextInput] = useState(false);

  const handleAnalyze = async () => {
    if (!resumeText.trim()) {
      toast.error('Please upload a resume or paste your resume text');
      return;
    }

    setIsAnalyzing(true);
    try {
      const response = await api.post('/api/user/career-tools/resume-review', {
        resume_text: resumeText,
        target_role: targetRole,
        industry: industry,
      });

      if (response.data.success) {
        setFeedback(response.data.feedback);
        toast.success('Resume analyzed successfully!');
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
    setTargetRole('');
    setIndustry('');
    setFeedback('');
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([feedback], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'resume-feedback.txt';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    toast.success('Feedback downloaded!');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link
                href="/career-tools"
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <FileText className="w-6 h-6 text-blue-600" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Resume Review</h1>
                  <p className="text-sm text-gray-500">AI-powered resume analysis</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Upload Resume</h2>
              
              {/* Toggle Input Method */}
              <div className="flex space-x-2 mb-4">
                <button
                  onClick={() => setUseTextInput(false)}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    !useTextInput
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Upload File
                </button>
                <button
                  onClick={() => setUseTextInput(true)}
                  className={`flex-1 py-2 px-4 rounded-lg font-medium transition-colors ${
                    useTextInput
                      ? 'bg-indigo-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  Paste Text
                </button>
              </div>

              {/* File Upload or Text Input */}
              {!useTextInput ? (
                <FileUpload onFileUpload={setResumeText} />
              ) : (
                <textarea
                  value={resumeText}
                  onChange={(e) => setResumeText(e.target.value)}
                  placeholder="Paste your resume text here..."
                  className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
                />
              )}
            </div>

            {/* Additional Inputs */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-lg font-bold text-gray-900 mb-4">Additional Information (Optional)</h2>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Role
                  </label>
                  <input
                    type="text"
                    value={targetRole}
                    onChange={(e) => setTargetRole(e.target.value)}
                    placeholder="e.g., Software Engineer, Product Manager"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Industry
                  </label>
                  <input
                    type="text"
                    value={industry}
                    onChange={(e) => setIndustry(e.target.value)}
                    placeholder="e.g., Technology, Finance, Healthcare"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  />
                </div>
              </div>

              <button
                onClick={handleAnalyze}
                disabled={isAnalyzing || !resumeText.trim()}
                className="w-full mt-6 py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center justify-center"
              >
                {isAnalyzing ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    Analyzing...
                  </>
                ) : (
                  <>
                    <FileText className="w-5 h-5 mr-2" />
                    Analyze Resume
                  </>
                )}
              </button>
            </div>
          </div>

          {/* Results Section */}
          <div className="space-y-6">
            {feedback ? (
              <>
                <div className="bg-white rounded-lg shadow-md p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h2 className="text-lg font-bold text-gray-900">Analysis Results</h2>
                    <div className="flex space-x-2">
                      <button
                        onClick={handleDownload}
                        className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                        title="Download feedback"
                      >
                        <Download className="w-5 h-5" />
                      </button>
                      <button
                        onClick={handleReset}
                        className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                        title="Review another resume"
                      >
                        <RefreshCw className="w-5 h-5" />
                      </button>
                    </div>
                  </div>

                  <div className="prose max-w-none">
                    <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                      {feedback}
                    </div>
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-12 text-center">
                <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-500 mb-2">
                  No Analysis Yet
                </h3>
                <p className="text-gray-400">
                  Upload your resume and click &quot;Analyze&quot; to get detailed feedback
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
