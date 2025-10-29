import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { Users, Clock, Trophy, Target } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const CoopTasksPanel = () => {
  const [availableTasks, setAvailableTasks] = useState([]);
  const [myTasks, setMyTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [joinRole, setJoinRole] = useState('');

  useEffect(() => {
    loadAvailableTasks();
  }, []);

  const loadAvailableTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/tasks/multiplayer/coop/available');
      if (response.data.success) {
        setAvailableTasks(response.data.tasks);
      }
    } catch (error) {
      console.error('Error loading co-op tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const createCoopTask = async () => {
    try {
      const response = await apiClient.post('/api/tasks/multiplayer/coop/create', {});
      if (response.data.success) {
        alert('Co-op task created! Waiting for partners to join.');
        loadAvailableTasks();
      }
    } catch (error) {
      console.error('Error creating co-op task:', error);
      alert('Failed to create co-op task');
    }
  };

  const joinTask = async (taskId, role) => {
    try {
      const response = await apiClient.post('/api/tasks/multiplayer/coop/join', {
        task_id: taskId,
        selected_role: role
      });
      if (response.data.success) {
        alert('Successfully joined co-op task!');
        setSelectedTask(null);
        loadAvailableTasks();
      }
    } catch (error) {
      console.error('Error joining task:', error);
      alert(error.response?.data?.detail || 'Failed to join task');
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
            <Users className="w-6 h-6" />
            Co-op Tasks
          </h2>
          <p className="text-gray-400 text-sm">Team up with other players for bigger rewards</p>
        </div>
        <Button onClick={createCoopTask} className="bg-blue-600 hover:bg-blue-700">
          Create Co-op Task
        </Button>
      </div>

      {/* Available Tasks */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading co-op tasks...</p>
          </div>
        ) : availableTasks.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Users className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No co-op tasks available</p>
            <p className="text-gray-500 text-sm">Create one to get started!</p>
          </div>
        ) : (
          availableTasks.map((task) => (
            <Card key={task.task_id} className="bg-gray-900 border-gray-700 hover:border-blue-500 transition-all">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{task.title}</CardTitle>
                    <CardDescription className="text-sm mt-1">
                      {task.description.substring(0, 100)}...
                    </CardDescription>
                  </div>
                  <Badge className={`${getDifficultyColor(task.difficulty)} text-white`}>
                    {task.difficulty}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                {/* Task Info */}
                <div className="space-y-3">
                  {/* Players */}
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 flex items-center gap-1">
                      <Users className="w-4 h-4" />
                      Players
                    </span>
                    <span className="text-white font-medium">
                      {task.partners_joined?.length || 0 + 1}/{task.max_players}
                    </span>
                  </div>

                  {/* Duration */}
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 flex items-center gap-1">
                      <Clock className="w-4 h-4" />
                      Duration
                    </span>
                    <span className="text-white font-medium">
                      {task.duration_minutes} min
                    </span>
                  </div>

                  {/* Rewards */}
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400 flex items-center gap-1">
                      <Trophy className="w-4 h-4" />
                      Rewards
                    </span>
                    <div className="text-right">
                      <span className="text-yellow-400 font-medium">{task.rewards?.xp || 0} XP</span>
                      <span className="text-green-400 font-medium ml-2">{task.rewards?.credits || 0} Credits</span>
                    </div>
                  </div>

                  {/* Roles */}
                  <div className="mt-3 pt-3 border-t border-gray-700">
                    <p className="text-xs text-gray-400 mb-2">Available Roles:</p>
                    <div className="flex flex-wrap gap-1">
                      {task.roles?.map((role, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {role.name}
                        </Badge>
                      ))}
                    </div>
                  </div>

                  {/* Join Button */}
                  <Button
                    onClick={() => setSelectedTask(task)}
                    className="w-full mt-4 bg-blue-600 hover:bg-blue-700"
                    disabled={task.partners_joined?.length >= task.max_players - 1}
                  >
                    {task.partners_joined?.length >= task.max_players - 1 ? 'Full' : 'Join Task'}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Join Task Modal */}
      {selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <Card className="bg-gray-900 border-gray-700 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <CardTitle className="text-xl">{selectedTask.title}</CardTitle>
              <CardDescription>{selectedTask.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Select Role */}
              <div>
                <label className="text-sm text-gray-400 mb-2 block">Select Your Role:</label>
                <div className="grid grid-cols-1 gap-2">
                  {selectedTask.roles?.map((role, idx) => (
                    <button
                      key={idx}
                      onClick={() => setJoinRole(role.name)}
                      className={`p-3 rounded-lg border-2 text-left transition-all ${
                        joinRole === role.name
                          ? 'border-blue-500 bg-blue-500 bg-opacity-20'
                          : 'border-gray-700 hover:border-gray-600'
                      }`}
                    >
                      <div className="font-medium">{role.name}</div>
                      <div className="text-xs text-gray-400">
                        Required: {role.required_skill} (Level {role.min_level})
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Partners Already Joined */}
              {selectedTask.partners_joined?.length > 0 && (
                <div>
                  <label className="text-sm text-gray-400 mb-2 block">Partners Joined:</label>
                  <div className="space-y-2">
                    {selectedTask.partners_joined.map((partner, idx) => (
                      <div key={idx} className="bg-gray-800 p-2 rounded flex items-center justify-between">
                        <span className="text-sm">{partner.player_name}</span>
                        <Badge variant="outline" className="text-xs">{partner.role}</Badge>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Actions */}
              <div className="flex gap-2 pt-4">
                <Button
                  onClick={() => {
                    if (joinRole) {
                      joinTask(selectedTask.task_id, joinRole);
                    } else {
                      alert('Please select a role');
                    }
                  }}
                  className="flex-1 bg-blue-600 hover:bg-blue-700"
                  disabled={!joinRole}
                >
                  Confirm & Join
                </Button>
                <Button
                  onClick={() => {
                    setSelectedTask(null);
                    setJoinRole('');
                  }}
                  variant="outline"
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default CoopTasksPanel;
