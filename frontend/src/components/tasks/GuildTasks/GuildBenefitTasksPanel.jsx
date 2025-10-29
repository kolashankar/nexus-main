import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { Shield, Users, TrendingUp, Star, CheckCircle } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const GuildTasksPanel = () => {
  const [guildTasks, setGuildTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
    loadGuildTasks();
  }, []);

  const loadGuildTasks = async () => {
    try {
      setLoading(true);
      // TODO: Implement guild tasks endpoint
      // const response = await apiClient.get('/api/guilds/tasks');
      // if (response.data.success) {
      //   setGuildTasks(response.data.tasks);
      // }
      
      // Mock data for now
      setGuildTasks([
        {
          task_id: 'guild_1',
          title: 'Guild Vault Security Upgrade',
          description: 'Complete a series of security challenges to upgrade your guild\'s vault protection.',
          difficulty: 'hard',
          duration_minutes: 45,
          required_contributions: 3,
          current_contributions: 1,
          progress_percentage: 33,
          contributors: [
            { player_name: 'Player1', contribution_type: 'complete_challenge' }
          ],
          rewards_per_contributor: {
            xp: 400,
            credits: 1000,
            karma: 15,
            guild_reputation: 50
          },
          guild_benefits: {
            vault_capacity: '+20%',
            vault_protection: '+15%',
            description: 'Guild vault can hold 20% more items and has 15% better protection'
          },
          status: 'active'
        }
      ]);
    } catch (error) {
      console.error('Error loading guild tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const contribute = async (taskId, contributionType) => {
    try {
      // TODO: Implement contribution endpoint
      // await apiClient.post('/api/guilds/tasks/contribute', {
      //   task_id: taskId,
      //   contribution_type: contributionType
      // });
      alert('Contribution successful!');
      loadGuildTasks();
    } catch (error) {
      console.error('Error contributing:', error);
      alert('Failed to contribute');
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

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <Shield className="w-6 h-6 text-purple-500" />
            Guild Tasks
          </h2>
          <p className="text-gray-400 text-sm">Work together to benefit the entire guild</p>
        </div>
      </div>

      {/* Active Guild Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading guild tasks...</p>
          </div>
        ) : guildTasks.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Shield className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No active guild tasks</p>
            <p className="text-gray-500 text-sm">Guild leaders can create new tasks</p>
          </div>
        ) : (
          guildTasks.map((task) => (
            <Card key={task.task_id} className="bg-gray-900 border-gray-700">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{task.title}</CardTitle>
                    <p className="text-sm text-gray-400 mt-1">{task.description}</p>
                  </div>
                  <Badge className={`${getDifficultyColor(task.difficulty)} text-white`}>
                    {task.difficulty}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Progress Bar */}
                <div>
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span className="text-gray-400">Progress</span>
                    <span className="text-white font-medium">
                      {task.current_contributions}/{task.required_contributions} contributions
                    </span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3 overflow-hidden">
                    <div
                      className="bg-purple-600 h-full transition-all duration-500 rounded-full flex items-center justify-end pr-2"
                      style={{ width: `${task.progress_percentage}%` }}
                    >
                      {task.progress_percentage >= 15 && (
                        <span className="text-xs font-bold text-white">{task.progress_percentage}%</span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Contributors */}
                {task.contributors && task.contributors.length > 0 && (
                  <div>
                    <p className="text-xs text-gray-400 mb-2">Contributors:</p>
                    <div className="flex flex-wrap gap-2">
                      {task.contributors.map((contributor, idx) => (
                        <div key={idx} className="bg-gray-800 px-3 py-1 rounded-full flex items-center gap-2">
                          <CheckCircle className="w-3 h-3 text-green-400" />
                          <span className="text-xs">{contributor.player_name}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Rewards */}
                <div className="bg-purple-500 bg-opacity-10 border border-purple-500 p-3 rounded-lg">
                  <p className="text-xs text-gray-400 mb-2">Rewards per contributor:</p>
                  <div className="grid grid-cols-2 gap-2 text-sm">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-300">XP:</span>
                      <span className="text-yellow-400 font-bold">{task.rewards_per_contributor.xp}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-300">Credits:</span>
                      <span className="text-green-400 font-bold">{task.rewards_per_contributor.credits}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-300">Karma:</span>
                      <span className="text-blue-400 font-bold">{task.rewards_per_contributor.karma}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-300">Guild Rep:</span>
                      <span className="text-purple-400 font-bold">{task.rewards_per_contributor.guild_reputation}</span>
                    </div>
                  </div>
                </div>

                {/* Guild Benefits */}
                <div className="bg-yellow-500 bg-opacity-10 border border-yellow-500 p-3 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <Star className="w-4 h-4 text-yellow-400" />
                    <p className="text-xs text-yellow-400 font-bold">Guild Benefits:</p>
                  </div>
                  <p className="text-sm text-gray-200">{task.guild_benefits.description}</p>
                </div>

                {/* Contribute Button */}
                <Button
                  onClick={() => setSelectedTask(task)}
                  className="w-full bg-purple-600 hover:bg-purple-700"
                  disabled={task.status !== 'active'}
                >
                  {task.status === 'active' ? 'Contribute to Task' : 'Completed'}
                </Button>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Contribution Modal */}
      {selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <Card className="bg-gray-900 border-gray-700 max-w-2xl w-full">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <Shield className="w-6 h-6 text-purple-500" />
                Contribute to {selectedTask.title}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-gray-400">Choose how you want to contribute:</p>
              
              {/* Contribution Options */}
              <div className="space-y-2">
                {selectedTask.contribution_types?.map((type, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      contribute(selectedTask.task_id, type);
                      setSelectedTask(null);
                    }}
                    className="w-full p-4 bg-gray-800 hover:bg-gray-700 border-2 border-gray-700 hover:border-purple-500 rounded-lg text-left transition-all"
                  >
                    <p className="font-medium capitalize">{type.replace('_', ' ')}</p>
                  </button>
                ))}
              </div>

              {/* Cancel */}
              <Button
                onClick={() => setSelectedTask(null)}
                variant="outline"
                className="w-full"
              >
                Cancel
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default GuildTasksPanel;
