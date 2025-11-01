'use client';

import React, { useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useQuery } from '@tanstack/react-query';
import { apiClient } from '@/lib/api';
import { Button } from '@/components/ui/Button';
import { Skeleton } from '@/components/ui/Skeleton';
import { Card } from '@/components/ui/Card';
import { 
  ArrowLeft, 
  Clock, 
  BookOpen, 
  CheckCircle, 
  Circle,
  FileText,
  Link as LinkIcon,
  Play
} from 'lucide-react';
import { Roadmap, RoadmapNode } from '@/types';
import { toast } from 'react-hot-toast';

export default function RoadmapDetailPage() {
  const params = useParams();
  const router = useRouter();
  const roadmapId = params?.id as string;
  const [completedNodes, setCompletedNodes] = useState<Set<string>>(new Set());
  const [selectedNode, setSelectedNode] = useState<RoadmapNode | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ['roadmap', roadmapId],
    queryFn: async () => {
      const response = await apiClient.getRoadmapById(roadmapId);
      return response;
    },
    enabled: !!roadmapId,
  });

  const roadmap: Roadmap | undefined = data?.data;

  const toggleNodeCompletion = (nodeId: string) => {
    const newCompleted = new Set(completedNodes);
    if (completedNodes.has(nodeId)) {
      newCompleted.delete(nodeId);
      toast.success('Marked as incomplete');
    } else {
      newCompleted.add(nodeId);
      toast.success('Marked as complete');
    }
    setCompletedNodes(newCompleted);
  };

  const getNodeIcon = (type: string) => {
    switch (type) {
      case 'content':
        return <FileText className="w-5 h-5" />;
      case 'roadmap_link':
        return <LinkIcon className="w-5 h-5" />;
      case 'article_link':
        return <BookOpen className="w-5 h-5" />;
      default:
        return <Circle className="w-5 h-5" />;
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <Skeleton className="h-10 w-32 mb-8" />
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <Skeleton className="h-96 lg:col-span-2" />
            <Skeleton className="h-96" />
          </div>
        </div>
      </div>
    );
  }

  if (error || !roadmap) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Roadmap not found</h2>
          <Button onClick={() => router.push('/roadmaps')}>Back to Roadmaps</Button>
        </div>
      </div>
    );
  }

  const progress = (completedNodes.size / roadmap.nodes.length) * 100;

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Back Button */}
        <Button
          variant="outline"
          onClick={() => router.push('/roadmaps')}
          className="mb-6"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back to Roadmaps
        </Button>

        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <h1 className="text-3xl font-bold text-gray-900 mb-2">{roadmap.title}</h1>
              <p className="text-gray-600 mb-4">{roadmap.description}</p>
              <div className="flex items-center space-x-4 text-sm text-gray-500">
                <div className="flex items-center">
                  <Clock className="w-4 h-4 mr-1" />
                  {roadmap.estimated_time_hours}h
                </div>
                <div className="flex items-center">
                  <BookOpen className="w-4 h-4 mr-1" />
                  {roadmap.nodes.length} steps
                </div>
                <span className="px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
                  {roadmap.level}
                </span>
              </div>
            </div>
          </div>

          {/* Progress Bar */}
          <div>
            <div className="flex items-center justify-between text-sm mb-2">
              <span className="font-medium text-gray-700">Your Progress</span>
              <span className="text-gray-600">
                {completedNodes.size} / {roadmap.nodes.length} completed
              </span>
            </div>
            <div className="h-3 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-green-500 transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Nodes List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-bold text-gray-900 mb-6">Learning Path</h2>
              <div className="space-y-4">
                {roadmap.nodes.map((node, index) => (
                  <Card
                    key={node.id}
                    className={`cursor-pointer transition-all ${
                      selectedNode?.id === node.id
                        ? 'ring-2 ring-blue-500 shadow-md'
                        : 'hover:shadow-md'
                    } ${
                      completedNodes.has(node.id)
                        ? 'bg-green-50 border-green-200'
                        : ''
                    }`}
                    onClick={() => setSelectedNode(node)}
                  >
                    <div className="p-4">
                      <div className="flex items-start">
                        <div className="flex items-center space-x-3 flex-1">
                          <div className="flex-shrink-0">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                toggleNodeCompletion(node.id);
                              }}
                              className="w-8 h-8 rounded-full border-2 flex items-center justify-center transition-colors hover:border-green-500"
                            >
                              {completedNodes.has(node.id) ? (
                                <CheckCircle className="w-6 h-6 text-green-600 fill-green-100" />
                              ) : (
                                <Circle className="w-6 h-6 text-gray-400" />
                              )}
                            </button>
                          </div>
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-1">
                              <div className="text-indigo-600">{getNodeIcon(node.type)}</div>
                              <h3 className="font-semibold text-gray-900">{node.title}</h3>
                            </div>
                            <p className="text-sm text-gray-600 line-clamp-2">{node.description}</p>
                          </div>
                        </div>
                        <span className="text-xs font-medium text-gray-500 ml-3">
                          Step {index + 1}
                        </span>
                      </div>
                    </div>
                  </Card>
                ))}
              </div>
            </div>
          </div>

          {/* Sidebar - Node Detail */}
          <div>
            <div className="bg-white rounded-lg shadow-sm p-6 sticky top-6">
              {selectedNode ? (
                <div>
                  <div className="flex items-center space-x-2 mb-4">
                    <div className="text-indigo-600">{getNodeIcon(selectedNode.type)}</div>
                    <h3 className="text-lg font-bold text-gray-900">{selectedNode.title}</h3>
                  </div>
                  <p className="text-gray-700 mb-4">{selectedNode.description}</p>
                  
                  {selectedNode.content && (
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-gray-900 mb-2">Content</h4>
                      <p className="text-sm text-gray-600 whitespace-pre-wrap">{selectedNode.content}</p>
                    </div>
                  )}

                  {selectedNode.video_url && (
                    <div className="mb-4">
                      <Button className="w-full" variant="outline">
                        <Play className="w-4 h-4 mr-2" />
                        Watch Video
                      </Button>
                    </div>
                  )}

                  {selectedNode.resources && selectedNode.resources.length > 0 && (
                    <div className="mb-4">
                      <h4 className="text-sm font-semibold text-gray-900 mb-2">Resources</h4>
                      <div className="space-y-2">
                        {selectedNode.resources.map((resource, idx) => (
                          <a
                            key={idx}
                            href={resource.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="block text-sm text-blue-600 hover:underline"
                          >
                            {resource.title}
                          </a>
                        ))}
                      </div>
                    </div>
                  )}

                  <Button
                    onClick={() => toggleNodeCompletion(selectedNode.id)}
                    className={`w-full ${
                      completedNodes.has(selectedNode.id)
                        ? 'bg-gray-600 hover:bg-gray-700'
                        : 'bg-green-600 hover:bg-green-700'
                    }`}
                  >
                    <CheckCircle className="w-4 h-4 mr-2" />
                    {completedNodes.has(selectedNode.id) ? 'Mark as Incomplete' : 'Mark as Complete'}
                  </Button>
                </div>
              ) : (
                <div className="text-center text-gray-500 py-8">
                  <BookOpen className="w-12 h-12 mx-auto mb-3 text-gray-400" />
                  <p>Select a step to view details</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}