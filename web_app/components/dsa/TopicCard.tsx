'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { DSATopic } from '@/types';
import { BookOpen, ArrowRight } from 'lucide-react';

interface TopicCardProps {
  topic: DSATopic;
}

export function TopicCard({ topic }: TopicCardProps) {
  return (
    <Link href={`/dsa/questions?topic=${topic.id}`}>
      <Card className="h-full hover:shadow-lg transition-all cursor-pointer group">
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div
              className="w-12 h-12 rounded-lg flex items-center justify-center text-2xl"
              style={{ backgroundColor: `${topic.color}20`, color: topic.color }}
            >
              {topic.icon}
            </div>
            <ArrowRight className="w-5 h-5 text-gray-400 group-hover:text-blue-600 transition-colors" />
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
            {topic.name}
          </h3>
          
          <p className="text-sm text-gray-600 mb-4 line-clamp-2">
            {topic.description}
          </p>
          
          <div className="flex items-center text-sm text-gray-500">
            <BookOpen className="w-4 h-4 mr-1" />
            {topic.question_count} problems
          </div>
        </div>
      </Card>
    </Link>
  );
}