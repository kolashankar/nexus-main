'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import { ChevronDown } from 'lucide-react';

interface CodeEditorProps {
  solutions: Array<{
    language: string;
    code: string;
  }>;
  readOnly?: boolean;
}

export function CodeEditor({ solutions, readOnly = true }: CodeEditorProps) {
  const [selectedLanguage, setSelectedLanguage] = useState(solutions[0]?.language || 'python');
  const selectedSolution = solutions.find(s => s.language === selectedLanguage);

  return (
    <div className="bg-gray-900 rounded-lg overflow-hidden">
      {/* Language Selector */}
      <div className="bg-gray-800 px-4 py-3 flex items-center justify-between border-b border-gray-700">
        <div className="flex items-center space-x-2">
          <span className="text-sm text-gray-400">Language:</span>
          <div className="relative">
            <select
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
              className="appearance-none bg-gray-700 text-white text-sm px-3 py-1 pr-8 rounded border border-gray-600 focus:outline-none focus:border-blue-500"
            >
              {solutions.map((solution) => (
                <option key={solution.language} value={solution.language}>
                  {solution.language.charAt(0).toUpperCase() + solution.language.slice(1)}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-2 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400 pointer-events-none" />
          </div>
        </div>
      </div>

      {/* Code Display */}
      <div className="p-4">
        <pre className="text-sm text-gray-100 overflow-x-auto">
          <code>{selectedSolution?.code || '// No solution available'}</code>
        </pre>
      </div>
    </div>
  );
}