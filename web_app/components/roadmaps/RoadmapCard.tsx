'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Roadmap } from '@/types';
import { Clock, BookOpen, TrendingUp, ArrowRight } from 'lucide-react';

interface RoadmapCardProps {
  roadmap: Roadmap;
}

export function RoadmapCard({ roadmap }: RoadmapCardProps) {
  const getLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'beginner':
        return 'text-green-600 bg-green-50';
      case 'intermediate':
        return 'text-yellow-600 bg-yellow-50';
      case 'advanced':
        return 'text-red-600 bg-red-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  return (
    <Link href={`/roadmaps/${roadmap.id}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer group">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-2">
                <span className={`px-3 py-1 text-xs font-medium rounded-full ${getLevelColor(roadmap.level)}`}>
                  {roadmap.level}
                </span>
                <span className="px-3 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded-full">
                  {roadmap.category}
                </span>
              </div>
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors" />
          </div>

          {/* Title & Description */}
          <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">
            {roadmap.title}
          </h3>
          <p className="text-sm text-gray-600 mb-4 line-clamp-3">
            {roadmap.description}
          </p>

          {/* Meta Info */}
          <div className="flex items-center space-x-4 mb-4 text-sm text-gray-500">
            <div className="flex items-center">
              <Clock className="w-4 h-4 mr-1" />
              {roadmap.estimated_time_hours}h
            </div>
            <div className="flex items-center">
              <BookOpen className="w-4 h-4 mr-1" />
              {roadmap.nodes.length} steps
            </div>
          </div>

          {/* Topics */}
          {roadmap.topics_covered && roadmap.topics_covered.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {roadmap.topics_covered.slice(0, 3).map((topic, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                >
                  {topic}
                </span>
              ))}
              {roadmap.topics_covered.length > 3 && (
                <span className="px-2 py-1 text-xs text-gray-500">
                  +{roadmap.topics_covered.length - 3} more
                </span>
              )}
            </div>
          )}

          {/* Footer */}
          <div className="pt-4 border-t">
            <Button variant="outline" className="w-full group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-600">
              <TrendingUp className="w-4 h-4 mr-2" />
              Start Learning
            </Button>
          </div>
        </div>
      </Card>
    </Link>
  );
}