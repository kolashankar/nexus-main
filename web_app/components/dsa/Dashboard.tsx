'use client';

import React from 'react';
import { Card } from '@/components/ui/Card';
import { TrendingUp, Target, Flame, Trophy } from 'lucide-react';

interface DashboardProps {
  stats: {
    problems_solved: number;
    current_streak: number;
    difficulty_breakdown: {
      easy: number;
      medium: number;
      hard: number;
    };
  };
}

export function Dashboard({ stats }: DashboardProps) {
  const totalSolved = stats.problems_solved;
  const { easy, medium, hard } = stats.difficulty_breakdown;

  return (
    <div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {/* Total Solved */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-blue-100 flex items-center justify-center">
                <Target className="w-6 h-6 text-blue-600" />
              </div>
              <TrendingUp className="w-5 h-5 text-green-500" />
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Problems Solved</h3>
            <p className="text-3xl font-bold text-gray-900">{totalSolved}</p>
          </div>
        </Card>

        {/* Current Streak */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-orange-100 flex items-center justify-center">
                <Flame className="w-6 h-6 text-orange-600" />
              </div>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Current Streak</h3>
            <p className="text-3xl font-bold text-gray-900">{stats.current_streak} days</p>
          </div>
        </Card>

        {/* Easy */}
        <Card>
          <div className="p-6">
            <div className="flex items-center justify-between mb-4">
              <div className="w-12 h-12 rounded-lg bg-green-100 flex items-center justify-center">
                <Trophy className="w-6 h-6 text-green-600" />
              </div>
            </div>
            <h3 className="text-sm font-medium text-gray-600 mb-1">Easy Solved</h3>
            <p className="text-3xl font-bold text-gray-900">{easy}</p>
          </div>
        </Card>

        {/* Medium & Hard */}
        <Card>
          <div className="p-6">
            <h3 className="text-sm font-medium text-gray-600 mb-4">Difficulty Split</h3>
            <div className="space-y-3">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-yellow-600">Medium</span>
                  <span className="font-semibold">{medium}</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-yellow-500" style={{ width: `${totalSolved ? (medium / totalSolved) * 100 : 0}%` }} />
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-red-600">Hard</span>
                  <span className="font-semibold">{hard}</span>
                </div>
                <div className="h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div className="h-full bg-red-500" style={{ width: `${totalSolved ? (hard / totalSolved) * 100 : 0}%` }} />
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}