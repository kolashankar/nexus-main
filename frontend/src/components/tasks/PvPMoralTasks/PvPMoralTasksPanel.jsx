import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { AlertCircle, User, Coins, Heart, XCircle } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const PvPMoralTasksPanel = () => {
  const [moralTasks, setMoralTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);

  useEffect(() => {
    loadPendingTasks();
  }, []);

  const loadPendingTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/tasks/multiplayer/pvp-moral/pending');
      if (response.data.success) {
        setMoralTasks(response.data.tasks);
      }
    } catch (error) {
      console.error('Error loading PvP moral tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const makeChoice = async (taskId, choiceIndex) => {
    try {
      const response = await apiClient.post('/api/tasks/multiplayer/pvp-moral/complete', {
        task_id: taskId,
        choice_index: choiceIndex
      });
      if (response.data.success) {
        alert('Choice made! Both players have been affected.');
        setSelectedTask(null);
        loadPendingTasks();
      }
    } catch (error) {
      console.error('Error making choice:', error);
      alert(error.response?.data?.detail || 'Failed to make choice');
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

  const getKarmaColor = (karma) => {
    if (karma > 10) return 'text-green-400';
    if (karma < -10) return 'text-red-400';
    return 'text-gray-400';
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold flex items-center gap-2">
            <AlertCircle className="w-6 h-6 text-orange-500" />
            PvP Moral Choices
          </h2>
          <p className="text-gray-400 text-sm">Your choices will affect other players</p>
        </div>
      </div>

      {/* Pending Tasks */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading moral choices...</p>
          </div>
        ) : moralTasks.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <AlertCircle className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No pending moral choices</p>
            <p className="text-gray-500 text-sm">These appear randomly during gameplay</p>
          </div>
        ) : (
          moralTasks.map((task) => (
            <Card
              key={task.task_id}
              className="bg-gray-900 border-gray-700 hover:border-orange-500 transition-all cursor-pointer"
              onClick={() => setSelectedTask(task)}
            >
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
                <div className="space-y-3">
                  {/* Target Player */}
                  <div className="bg-gray-800 p-3 rounded-lg">
                    <p className="text-xs text-gray-400 mb-1">Affects:</p>
                    <div className="flex items-center gap-2">
                      <User className="w-4 h-4 text-blue-400" />
                      <span className="font-medium">{task.target_player?.player_name}</span>
                      <Badge variant="outline" className="text-xs">
                        Lvl {task.target_player?.player_level}
                      </Badge>
                    </div>
                  </div>

                  {/* Choices Count */}
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-gray-400">Choices</span>
                    <span className="text-white font-medium">{task.choices?.length || 0} options</span>
                  </div>

                  {/* Make Choice Button */}
                  <Button
                    onClick={(e) => {
                      e.stopPropagation();
                      setSelectedTask(task);
                    }}
                    className="w-full mt-4 bg-orange-600 hover:bg-orange-700"
                  >
                    Make Your Choice
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>

      {/* Choice Details Modal */}
      {selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <Card className="bg-gray-900 border-gray-700 max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <AlertCircle className="w-6 h-6 text-orange-500" />
                {selectedTask.title}
              </CardTitle>
              <CardDescription className="text-base">{selectedTask.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Target Player Info */}
              <div className="bg-blue-500 bg-opacity-20 border border-blue-500 p-4 rounded-lg">
                <p className="text-xs text-gray-400 mb-2">This choice will affect:</p>
                <div className="flex items-center gap-2">
                  <User className="w-5 h-5 text-blue-400" />
                  <span className="font-bold text-lg">{selectedTask.target_player?.player_name}</span>
                  <Badge className="bg-blue-600">Level {selectedTask.target_player?.player_level}</Badge>
                </div>
              </div>

              {/* Choices */}
              <div className="space-y-3">
                <h3 className="font-bold text-lg">Choose Your Action:</h3>
                {selectedTask.choices?.map((choice, index) => (
                  <div
                    key={choice.id}
                    className="bg-gray-800 border-2 border-gray-700 hover:border-orange-500 p-4 rounded-lg cursor-pointer transition-all"
                    onClick={() => {
                      if (window.confirm(`Are you sure you want to: ${choice.text}?`)) {
                        makeChoice(selectedTask.task_id, choice.id);
                      }
                    }}
                  >
                    {/* Choice Text */}
                    <p className="font-medium mb-3">{choice.text}</p>

                    {/* Effects Grid */}
                    <div className="grid grid-cols-2 gap-4">
                      {/* Your Effects */}
                      <div className="bg-gray-900 p-3 rounded">
                        <p className="text-xs text-gray-400 mb-2 font-bold">You Get:</p>
                        <div className="space-y-1 text-sm">
                          <div className="flex items-center justify-between">
                            <span>XP:</span>
                            <span className="font-bold text-yellow-400">
                              {choice.player_effects?.xp || 0}
                            </span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span>Credits:</span>
                            <span className="font-bold text-green-400">
                              {choice.player_effects?.credits || 0}
                            </span>
                          </div>
                          <div className="flex items-center justify-between">
                            <span>Karma:</span>
                            <span className={`font-bold ${getKarmaColor(choice.player_effects?.karma)}`}>
                              {choice.player_effects?.karma > 0 ? '+' : ''}{choice.player_effects?.karma || 0}
                            </span>
                          </div>
                        </div>
                      </div>

                      {/* Target Effects */}
                      <div className="bg-gray-900 p-3 rounded">
                        <p className="text-xs text-gray-400 mb-2 font-bold">
                          {selectedTask.target_player?.player_name} Gets:
                        </p>
                        <div className="space-y-1 text-sm">
                          {choice.target_effects?.credits !== undefined && (
                            <div className="flex items-center justify-between">
                              <span>Credits:</span>
                              <span className={`font-bold ${
                                choice.target_effects.credits >= 0 ? 'text-green-400' : 'text-red-400'
                              }`}>
                                {choice.target_effects.credits > 0 ? '+' : ''}{choice.target_effects.credits}
                              </span>
                            </div>
                          )}
                          {choice.target_effects?.karma !== undefined && (
                            <div className="flex items-center justify-between">
                              <span>Karma:</span>
                              <span className={`font-bold ${getKarmaColor(choice.target_effects?.karma)}`}>
                                {choice.target_effects.karma > 0 ? '+' : ''}{choice.target_effects.karma}
                              </span>
                            </div>
                          )}
                          {choice.target_effects?.relationship_change !== undefined && (
                            <div className="flex items-center justify-between">
                              <span>Relationship:</span>
                              <span className={`font-bold ${
                                choice.target_effects.relationship_change >= 0 ? 'text-green-400' : 'text-red-400'
                              }`}>
                                {choice.target_effects.relationship_change > 0 ? '+' : ''}
                                {choice.target_effects.relationship_change}
                              </span>
                            </div>
                          )}
                        </div>
                      </div>
                    </div>

                    {/* Trait Changes */}
                    {choice.player_effects?.traits && Object.keys(choice.player_effects.traits).length > 0 && (
                      <div className="mt-3 pt-3 border-t border-gray-700">
                        <p className="text-xs text-gray-400 mb-2">Your Trait Changes:</p>
                        <div className="flex flex-wrap gap-2">
                          {Object.entries(choice.player_effects.traits).map(([trait, value]) => (
                            <Badge
                              key={trait}
                              className={value > 0 ? 'bg-green-600' : 'bg-red-600'}
                            >
                              {trait}: {value > 0 ? '+' : ''}{value}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              {/* Cancel Button */}
              <Button
                onClick={() => setSelectedTask(null)}
                variant="outline"
                className="w-full"
              >
                Close
              </Button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default PvPMoralTasksPanel;
