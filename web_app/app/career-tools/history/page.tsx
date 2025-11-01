"use client";

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { ArrowLeft, History, Search, Filter, FileText, Mail, Target, Sparkles, Trash2, Eye } from 'lucide-react';
import { api } from '@/lib/api';
import toast from 'react-hot-toast';
import { format } from 'date-fns';

type ToolType = 'resume_review' | 'cover_letter' | 'ats_hack' | 'cold_email' | 'all';

interface UsageItem {
  id: string;
  tool_type: string;
  input_data: any;
  output_data: string;
  created_at: string;
}

const toolConfig = {
  resume_review: {
    label: 'Resume Review',
    icon: FileText,
    color: 'blue',
  },
  cover_letter: {
    label: 'Cover Letter',
    icon: Mail,
    color: 'green',
  },
  ats_hack: {
    label: 'ATS Hack',
    icon: Target,
    color: 'purple',
  },
  cold_email: {
    label: 'Cold Email',
    icon: Sparkles,
    color: 'orange',
  },
};

export default function UsageHistoryPage() {
  const [usage, setUsage] = useState<UsageItem[]>([]);
  const [filteredUsage, setFilteredUsage] = useState<UsageItem[]>([]);
  const [filterType, setFilterType] = useState<ToolType>('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState<UsageItem | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    fetchUsage();
  }, []);

  useEffect(() => {
    filterAndSearchUsage();
  }, [usage, filterType, searchQuery]);

  const fetchUsage = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('/api/user/career-tools/history');
      if (response.data.success) {
        setUsage(response.data.usage || []);
      }
    } catch (error: any) {
      toast.error('Failed to fetch usage history');
    } finally {
      setIsLoading(false);
    }
  };

  const filterAndSearchUsage = () => {
    let filtered = usage;

    // Filter by type
    if (filterType !== 'all') {
      filtered = filtered.filter((item) => item.tool_type === filterType);
    }

    // Search
    if (searchQuery) {
      filtered = filtered.filter(
        (item) =>
          item.output_data.toLowerCase().includes(searchQuery.toLowerCase()) ||
          JSON.stringify(item.input_data).toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    setFilteredUsage(filtered);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this entry?')) return;

    try {
      await api.delete(`/api/user/career-tools/history/${id}`);
      setUsage(usage.filter((item) => item.id !== id));
      toast.success('Entry deleted successfully');
    } catch (error: any) {
      toast.error('Failed to delete entry');
    }
  };

  const getToolConfig = (toolType: string) => {
    return toolConfig[toolType as keyof typeof toolConfig] || toolConfig.resume_review;
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link href="/career-tools" className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <ArrowLeft className="w-5 h-5" />
              </Link>
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gray-100 rounded-lg">
                  <History className="w-6 h-6 text-gray-700" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">Usage History</h1>
                  <p className="text-sm text-gray-500">{filteredUsage.length} items</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Search and Filter */}
        <div className="bg-white rounded-lg shadow-md p-4 mb-6">
          <div className="flex flex-col md:flex-row gap-4">
            {/* Search */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search history..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>

            {/* Filter */}
            <div className="flex space-x-2">
              <button
                onClick={() => setFilterType('all')}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  filterType === 'all'
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                All
              </button>
              {Object.entries(toolConfig).map(([type, config]) => (
                <button
                  key={type}
                  onClick={() => setFilterType(type as ToolType)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    filterType === type
                      ? `bg-${config.color}-600 text-white`
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {config.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Usage List */}
        {isLoading ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4" />
            <p className="text-gray-500">Loading history...</p>
          </div>
        ) : filteredUsage.length === 0 ? (
          <div className="bg-white rounded-lg shadow-md p-12 text-center">
            <History className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-500 mb-2">No History Found</h3>
            <p className="text-gray-400 mb-4">
              {filterType === 'all'
                ? 'Start using Career Tools to see your history here'
                : `No ${getToolConfig(filterType).label} history found`}
            </p>
            <Link
              href="/career-tools"
              className="inline-block px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
            >
              Explore Career Tools
            </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-4">
            {filteredUsage.map((item) => {
              const config = getToolConfig(item.tool_type);
              const Icon = config.icon;

              return (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex items-start space-x-4 flex-1">
                      <div className={`p-3 bg-${config.color}-100 rounded-lg flex-shrink-0`}>
                        <Icon className={`w-6 h-6 text-${config.color}-600`} />
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center space-x-2 mb-2">
                          <h3 className="font-bold text-gray-900">{config.label}</h3>
                          <span className="text-sm text-gray-500">
                            {format(new Date(item.created_at), 'MMM d, yyyy h:mm a')}
                          </span>
                        </div>
                        <p className="text-gray-600 line-clamp-2 mb-3">
                          {item.output_data.substring(0, 200)}...
                        </p>
                        <button
                          onClick={() => setSelectedItem(item)}
                          className="text-indigo-600 hover:text-indigo-700 font-medium text-sm flex items-center"
                        >
                          <Eye className="w-4 h-4 mr-1" />
                          View Full Content
                        </button>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDelete(item.id)}
                      className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete"
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

      {/* View Modal */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div className="p-6 border-b flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">
                {getToolConfig(selectedItem.tool_type).label} - Full Content
              </h2>
              <button
                onClick={() => setSelectedItem(null)}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                ✕
              </button>
            </div>
            <div className="p-6 overflow-y-auto flex-1">
              <div className="prose max-w-none">
                <div className="whitespace-pre-wrap text-gray-700 leading-relaxed">
                  {selectedItem.output_data}
                </div>
              </div>
            </div>
            <div className="p-6 border-t bg-gray-50 flex justify-end space-x-3">
              <button
                onClick={() => {
                  navigator.clipboard.writeText(selectedItem.output_data);
                  toast.success('Copied to clipboard!');
                }}
                className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
              >
                Copy to Clipboard
              </button>
              <button
                onClick={() => setSelectedItem(null)}
                className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
