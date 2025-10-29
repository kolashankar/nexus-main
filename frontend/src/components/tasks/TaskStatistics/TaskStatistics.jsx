import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { BarChart, PieChart, TrendingUp, Users } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const TaskStatistics = () => {
  const [statistics, setStatistics] = useState(null);
  const [popularTasks, setPopularTasks] = useState([]);
  const [comparison, setComparison] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadStatistics();
  }, []);

  const loadStatistics = async () => {
    try {
      setLoading(true);
      
      // Load choice statistics
      const statsRes = await apiClient.get('/api/tasks/analytics/statistics/choices');
      if (statsRes.data.success) {
        setStatistics(statsRes.data.statistics);
      }

      // Load popular tasks
      const popularRes = await apiClient.get('/api/tasks/analytics/statistics/popular-tasks');
      if (popularRes.data.success) {
        setPopularTasks(popularRes.data.popular_tasks);
      }

      // Load player comparison
      const comparisonRes = await apiClient.get('/api/tasks/analytics/statistics/comparison');
      if (comparisonRes.data.success) {
        setComparison(comparisonRes.data.comparison);
      }
    } catch (error) {
      console.error('Error loading statistics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6 text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p className="text-gray-400 mt-4">Loading statistics...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div>
        <h2 className="text-3xl font-bold flex items-center gap-2">
          <BarChart className="w-8 h-8" />
          Task Statistics
        </h2>
        <p className="text-gray-400 text-sm mt-1">See how your choices compare to other players</p>
      </div>

      {/* Player Comparison */}
      {comparison && (
        <Card className="bg-gradient-to-br from-purple-900 to-purple-800 border-purple-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Users className="w-5 h-5" />
              Your Performance vs Global Average
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-purple-200 text-sm">Your Tasks Completed</p>
                <p className="text-4xl font-bold text-white">{comparison.player_tasks_completed}</p>
              </div>
              <div className="text-center">
                <p className="text-purple-200 text-sm">Global Average</p>
                <p className="text-4xl font-bold text-purple-300">{comparison.global_average_tasks}</p>
              </div>
              <div className="text-center">
                <p className="text-purple-200 text-sm">Your Percentile</p>
                <p className="text-4xl font-bold text-yellow-400">{comparison.percentile}%</p>
              </div>
            </div>
            <div className="mt-4 text-center">
              <p className="text-lg font-bold text-white">{comparison.comparison}</p>
              <p className="text-sm text-purple-200">
                Rank #{comparison.rank_among_players} out of {comparison.total_active_players} players
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Popular Tasks */}
      <Card className="bg-gray-900 border-gray-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5" />
            Most Popular Tasks
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {popularTasks.slice(0, 10).map((task, index) => (
              <div key={index} className="flex items-center justify-between bg-gray-800 p-3 rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center font-bold">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-medium">{task.task_title}</p>
                    <p className="text-xs text-gray-400">
                      {task.task_type} • {task.difficulty}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-bold text-blue-400">{task.completions}</p>
                  <p className="text-xs text-gray-400">completions</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Choice Breakdown */}
      {statistics && statistics.choice_breakdown && (
        <Card className="bg-gray-900 border-gray-700">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PieChart className="w-5 h-5" />
              Choice Statistics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-gray-400 mb-4">
              See what choices other players made across different tasks
            </p>
            <div className="space-y-6">
              {Object.entries(statistics.choice_breakdown).slice(0, 5).map(([taskTitle, data]) => (
                <div key={taskTitle} className="border-b border-gray-700 pb-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium">{taskTitle}</h4>
                    <span className="text-xs text-gray-400">{data.total_completions} players</span>
                  </div>
                  <div className="space-y-2">
                    {data.choices.map((choice, idx) => (
                      <div key={idx}>
                        <div className="flex items-center justify-between text-sm mb-1">
                          <span className="text-gray-300">{choice.choice}</span>
                          <span className="font-bold">{choice.percentage}%</span>
                        </div>
                        <div className="w-full bg-gray-700 rounded-full h-2">
                          <div
                            className="bg-blue-600 h-2 rounded-full transition-all duration-500"
                            style={{ width: `${choice.percentage}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Popular Choices */}
      {statistics && statistics.popular_choices && (
        <Card className="bg-gray-900 border-gray-700">
          <CardHeader>
            <CardTitle>Most Common Choices</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {statistics.popular_choices.map((choice, index) => (
                <div key={index} className="flex items-center justify-between bg-gray-800 p-3 rounded">
                  <span className="text-sm">{choice.choice}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-gray-400 text-sm">{choice.count} times</span>
                    <span className="font-bold text-blue-400">{choice.percentage}%</span>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default TaskStatistics;
