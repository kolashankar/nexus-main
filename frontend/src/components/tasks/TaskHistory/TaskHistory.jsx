import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { History, Filter, ChevronDown, ChevronUp, Calendar, Trophy, TrendingUp } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const TaskHistory = () => {
  const [history, setHistory] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(false);
  const [filter, setFilter] = useState('all');
  const [expandedTask, setExpandedTask] = useState(null);
  const [periodDays, setPeriodDays] = useState(30);

  useEffect(() => {
    loadHistory();
    loadStats();
  }, [filter, periodDays]);

  const loadHistory = async () => {
    try {
      setLoading(true);
      const params = filter !== 'all' ? { task_type: filter } : {};
      const response = await apiClient.get('/api/tasks/analytics/history', { params });
      if (response.data.success) {
        setHistory(response.data.history);
      }
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const response = await apiClient.get('/api/tasks/analytics/history/stats', {
        params: { period_days: periodDays }
      });
      if (response.data.success) {
        setStats(response.data.stats);
      }
    } catch (error) {
      console.error('Error loading stats:', error);
    }
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      'easy': 'bg-green-500',
      'medium': 'bg-yellow-500',
      'hard': 'bg-orange-500',
      'legendary': 'bg-purple-500'
    };
    return colors[difficulty?.toLowerCase()] || 'bg-gray-500';
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold flex items-center gap-2">
            <History className="w-8 h-8" />
            Task History
          </h2>
          <p className="text-gray-400 text-sm mt-1">View all your completed tasks and achievements</p>
        </div>
      </div>

      {/* Stats Summary */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card className="bg-gradient-to-br from-blue-900 to-blue-800 border-blue-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-blue-200 text-sm">Total Completed</p>
                  <p className="text-3xl font-bold text-white">{stats.total_tasks_completed}</p>
                </div>
                <Trophy className="w-12 h-12 text-blue-300 opacity-50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-green-900 to-green-800 border-green-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-green-200 text-sm">Success Rate</p>
                  <p className="text-3xl font-bold text-white">{stats.success_rate.toFixed(1)}%</p>
                </div>
                <TrendingUp className="w-12 h-12 text-green-300 opacity-50" />
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-yellow-900 to-yellow-800 border-yellow-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-yellow-200 text-sm">Total XP</p>
                  <p className="text-3xl font-bold text-white">{stats.total_xp_gained.toLocaleString()}</p>
                </div>
                <div className="text-4xl opacity-50">⚡</div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-900 to-purple-800 border-purple-700">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-purple-200 text-sm">Karma Change</p>
                  <p className={`text-3xl font-bold ${stats.total_karma_change >= 0 ? 'text-green-300' : 'text-red-300'}`}>
                    {stats.total_karma_change > 0 ? '+' : ''}{stats.total_karma_change}
                  </p>
                </div>
                <div className="text-4xl opacity-50">☯</div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Filters */}
      <div className="flex items-center gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <span className="text-sm text-gray-400">Filter:</span>
        </div>
        {['all', 'moral_choice', 'combat', 'economic', 'coop', 'competitive'].map((filterType) => (
          <Button
            key={filterType}
            onClick={() => setFilter(filterType)}
            variant={filter === filterType ? 'default' : 'outline'}
            size="sm"
            className={filter === filterType ? 'bg-blue-600' : ''}
          >
            {filterType.replace('_', ' ').toUpperCase()}
          </Button>
        ))}
      </div>

      {/* History List */}
      <div className="space-y-3">
        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading history...</p>
          </div>
        ) : history.length === 0 ? (
          <Card className="bg-gray-900 border-gray-700">
            <CardContent className="p-12 text-center">
              <History className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No tasks completed yet</p>
              <p className="text-gray-500 text-sm">Start completing tasks to see your history</p>
            </CardContent>
          </Card>
        ) : (
          history.map((task) => (
            <Card key={task._id} className="bg-gray-900 border-gray-700 hover:border-blue-500 transition-all">
              <CardHeader
                className="cursor-pointer"
                onClick={() => setExpandedTask(expandedTask === task._id ? null : task._id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3">
                      <CardTitle className="text-lg">{task.task_title}</CardTitle>
                      <Badge className={`${getDifficultyColor(task.difficulty)} text-white`}>
                        {task.difficulty}
                      </Badge>
                      <Badge variant="outline" className="text-xs">
                        {task.task_type?.replace('_', ' ')}
                      </Badge>
                      {task.success && (
                        <Badge className="bg-green-600 text-white">✓ Success</Badge>
                      )}
                    </div>
                    <div className="flex items-center gap-4 mt-2 text-sm text-gray-400">
                      <span className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        {formatDate(task.completed_at)}
                      </span>
                      {task.xp_gained > 0 && (
                        <span className="text-yellow-400">+{task.xp_gained} XP</span>
                      )}
                      {task.karma_change !== 0 && (
                        <span className={task.karma_change > 0 ? 'text-green-400' : 'text-red-400'}>
                          {task.karma_change > 0 ? '+' : ''}{task.karma_change} Karma
                        </span>
                      )}
                    </div>
                  </div>
                  <button className="text-gray-400 hover:text-white">
                    {expandedTask === task._id ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                </div>
              </CardHeader>

              {expandedTask === task._id && (
                <CardContent className="border-t border-gray-700 pt-4">
                  <div className="space-y-4">
                    {/* Description */}
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Description:</p>
                      <p className="text-gray-200">{task.task_description}</p>
                    </div>

                    {/* Choice Made */}
                    {task.choice_made && (
                      <div>
                        <p className="text-sm text-gray-400 mb-1">Your Choice:</p>
                        <div className="bg-gray-800 p-3 rounded-lg">
                          <p className="text-white">{task.choice_made.text}</p>
                        </div>
                      </div>
                    )}

                    {/* Rewards */}
                    {task.rewards_received && (
                      <div>
                        <p className="text-sm text-gray-400 mb-2">Rewards:</p>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                          {task.rewards_received.xp && (
                            <div className="bg-yellow-500 bg-opacity-20 p-2 rounded">
                              <p className="text-xs text-gray-400">XP</p>
                              <p className="text-yellow-400 font-bold">+{task.rewards_received.xp}</p>
                            </div>
                          )}
                          {task.rewards_received.credits && (
                            <div className="bg-green-500 bg-opacity-20 p-2 rounded">
                              <p className="text-xs text-gray-400">Credits</p>
                              <p className="text-green-400 font-bold">+{task.rewards_received.credits}</p>
                            </div>
                          )}
                          {task.rewards_received.karma && (
                            <div className="bg-blue-500 bg-opacity-20 p-2 rounded">
                              <p className="text-xs text-gray-400">Karma</p>
                              <p className="text-blue-400 font-bold">
                                {task.rewards_received.karma > 0 ? '+' : ''}{task.rewards_received.karma}
                              </p>
                            </div>
                          )}
                        </div>
                      </div>
                    )}

                    {/* Trait Changes */}
                    {task.trait_changes && Object.keys(task.trait_changes).length > 0 && (
                      <div>
                        <p className="text-sm text-gray-400 mb-2">Trait Changes:</p>
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(task.trait_changes).map(([trait, change]) => (
                            <Badge
                              key={trait}
                              className={change > 0 ? 'bg-green-600' : 'bg-red-600'}
                            >
                              {trait}: {change > 0 ? '+' : ''}{change}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </CardContent>
              )}
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default TaskHistory;
