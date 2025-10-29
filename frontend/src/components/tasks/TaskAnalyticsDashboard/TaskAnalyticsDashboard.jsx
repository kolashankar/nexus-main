import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../../ui/tabs';
import { BarChart, History, TrendingUp, Trophy } from 'lucide-react';
import TaskHistory from '../TaskHistory/TaskHistory';
import TaskStatistics from '../TaskStatistics/TaskStatistics';
import TraitEvolutionChart from '../TraitEvolution/TraitEvolutionChart';
import TaskAchievements from '../TaskAchievements/TaskAchievements';
import { apiClient } from '../../../services/api/client';

const TaskAnalyticsDashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [streak, setStreak] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      // Load streak
      const streakRes = await apiClient.get('/api/tasks/analytics/history/streak');
      if (streakRes.data.success) {
        setStreak(streakRes.data.streak);
      }

      // Load recent activity
      const historyRes = await apiClient.get('/api/tasks/analytics/history', {
        params: { limit: 5 }
      });
      if (historyRes.data.success) {
        setRecentActivity(historyRes.data.history);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white p-6">
      {/* Dashboard Header */}
      <div className="mb-6">
        <h1 className="text-4xl font-bold mb-2">Task Analytics Dashboard</h1>
        <p className="text-gray-400">Comprehensive overview of your task performance</p>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
        <TabsList className="bg-gray-900 border border-gray-700">
          <TabsTrigger value="overview" className="data-[state=active]:bg-blue-600">
            <BarChart className="w-4 h-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="history" className="data-[state=active]:bg-blue-600">
            <History className="w-4 h-4 mr-2" />
            History
          </TabsTrigger>
          <TabsTrigger value="statistics" className="data-[state=active]:bg-blue-600">
            <TrendingUp className="w-4 h-4 mr-2" />
            Statistics
          </TabsTrigger>
          <TabsTrigger value="traits" className="data-[state=active]:bg-blue-600">
            <TrendingUp className="w-4 h-4 mr-2" />
            Trait Evolution
          </TabsTrigger>
          <TabsTrigger value="achievements" className="data-[state=active]:bg-blue-600">
            <Trophy className="w-4 h-4 mr-2" />
            Achievements
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          {/* Streak Card */}
          {streak && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card className="bg-gradient-to-br from-orange-900 to-orange-800 border-orange-700">
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <div className="text-2xl">🔥</div>
                    Current Streak
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-center">
                    <p className="text-6xl font-bold text-white">{streak.current_streak}</p>
                    <p className="text-orange-200 mt-2">consecutive days</p>
                    <p className="text-sm text-orange-300 mt-4">
                      Longest streak: {streak.longest_streak} days
                    </p>
                  </div>
                </CardContent>
              </Card>

              <Card className="bg-gradient-to-br from-blue-900 to-blue-800 border-blue-700">
                <CardHeader>
                  <CardTitle>Recent Activity</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {recentActivity.length > 0 ? (
                      recentActivity.map((task, idx) => (
                        <div key={idx} className="bg-blue-800 bg-opacity-50 p-2 rounded text-sm">
                          <p className="font-medium truncate">{task.task_title}</p>
                          <p className="text-xs text-blue-200">{formatDate(task.completed_at)}</p>
                        </div>
                      ))
                    ) : (
                      <p className="text-blue-200 text-center py-4">No recent activity</p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>
          )}

          {/* Quick Stats Preview */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* History Preview */}
            <Card className="bg-gray-900 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <History className="w-5 h-5" />
                  Task History
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-400 text-sm mb-3">View all completed tasks with detailed breakdown</p>
                <button
                  onClick={() => setActiveTab('history')}
                  className="w-full bg-blue-600 hover:bg-blue-700 py-2 rounded-lg transition-all"
                >
                  View History
                </button>
              </CardContent>
            </Card>

            {/* Statistics Preview */}
            <Card className="bg-gray-900 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart className="w-5 h-5" />
                  Statistics
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-400 text-sm mb-3">Compare your choices with other players</p>
                <button
                  onClick={() => setActiveTab('statistics')}
                  className="w-full bg-purple-600 hover:bg-purple-700 py-2 rounded-lg transition-all"
                >
                  View Stats
                </button>
              </CardContent>
            </Card>

            {/* Achievements Preview */}
            <Card className="bg-gray-900 border-gray-700">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Trophy className="w-5 h-5" />
                  Achievements
                </CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-400 text-sm mb-3">Track milestones and unlock rewards</p>
                <button
                  onClick={() => setActiveTab('achievements')}
                  className="w-full bg-yellow-600 hover:bg-yellow-700 py-2 rounded-lg transition-all"
                >
                  View Achievements
                </button>
              </CardContent>
            </Card>
          </div>

          {/* Trait Evolution Preview */}
          <Card className="bg-gray-900 border-gray-700">
            <CardHeader>
              <CardTitle>Trait Evolution</CardTitle>
            </CardHeader>
            <CardContent>
              <TraitEvolutionChart traitName="kindness" />
            </CardContent>
          </Card>
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history">
          <TaskHistory />
        </TabsContent>

        {/* Statistics Tab */}
        <TabsContent value="statistics">
          <TaskStatistics />
        </TabsContent>

        {/* Trait Evolution Tab */}
        <TabsContent value="traits">
          <Card className="bg-gray-900 border-gray-700">
            <CardHeader>
              <CardTitle>Trait Evolution Over Time</CardTitle>
            </CardHeader>
            <CardContent>
              <TraitEvolutionChart />
            </CardContent>
          </Card>
        </TabsContent>

        {/* Achievements Tab */}
        <TabsContent value="achievements">
          <TaskAchievements />
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TaskAnalyticsDashboard;
