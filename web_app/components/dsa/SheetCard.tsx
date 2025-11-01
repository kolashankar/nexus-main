'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { DSASheet } from '@/types';
import { FileText, User, CheckCircle } from 'lucide-react';

interface SheetCardProps {
  sheet: DSASheet;
}

export function SheetCard({ sheet }: SheetCardProps) {
  const totalQuestions = sheet.questions.length;
  const { easy, medium, hard } = sheet.difficulty_breakdown;

  return (
    <Link href={`/dsa/sheets/${sheet.id}`}>
      <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer group">
        <div className="p-6">
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center space-x-2">
              <div className="w-10 h-10 rounded-lg bg-green-100 flex items-center justify-center">
                <FileText className="w-5 h-5 text-green-600" />
              </div>
              <div>
                <span className="inline-block px-2 py-1 text-xs font-medium bg-blue-50 text-blue-700 rounded">
                  {sheet.level}
                </span>
              </div>
            </div>
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors line-clamp-2">
            {sheet.name}
          </h3>
          
          <p className="text-sm text-gray-600 mb-4 line-clamp-2">
            {sheet.description}
          </p>
          
          <div className="flex items-center text-sm text-gray-600 mb-4">
            <User className="w-4 h-4 mr-1" />
            {sheet.author}
          </div>
          
          <div className="mb-4">
            <div className="flex items-center justify-between text-xs text-gray-600 mb-2">
              <span>{totalQuestions} Problems</span>
            </div>
            <div className="flex space-x-2">
              <div className="flex-1">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-green-500"
                    style={{ width: `${(easy / totalQuestions) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 mt-1 block">Easy: {easy}</span>
              </div>
              <div className="flex-1">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-yellow-500"
                    style={{ width: `${(medium / totalQuestions) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 mt-1 block">Medium: {medium}</span>
              </div>
              <div className="flex-1">
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-red-500"
                    style={{ width: `${(hard / totalQuestions) * 100}%` }}
                  />
                </div>
                <span className="text-xs text-gray-500 mt-1 block">Hard: {hard}</span>
              </div>
            </div>
          </div>
          
          {sheet.tags && sheet.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {sheet.tags.slice(0, 3).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 text-xs bg-gray-100 text-gray-700 rounded"
                >
                  {tag}
                </span>
              ))}
              {sheet.tags.length > 3 && (
                <span className="px-2 py-1 text-xs text-gray-500">+{sheet.tags.length - 3}</span>
              )}
            </div>
          )}
          
          <div className="pt-4 border-t">
            <Button variant="outline" className="w-full group-hover:bg-blue-50 group-hover:text-blue-600 group-hover:border-blue-600">
              <CheckCircle className="w-4 h-4 mr-2" />
              Start Practicing
            </Button>
          </div>
        </div>
      </Card>
    </Link>
  );
}