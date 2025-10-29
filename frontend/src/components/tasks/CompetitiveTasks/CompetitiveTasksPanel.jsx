import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../../ui/card';
import { Button } from '../../ui/button';
import { Badge } from '../../ui/badge';
import { Swords, Trophy, Clock, Target, Zap } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const CompetitiveTasksPanel = () => {
  const [challenges, setChallenges] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedChallenge, setSelectedChallenge] = useState(null);

  useEffect(() => {
    loadChallenges();
  }, []);

  const loadChallenges = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/tasks/multiplayer/competitive/challenges');
      if (response.data.success) {
        setChallenges(response.data.challenges);
      }
    } catch (error) {
      console.error('Error loading challenges:', error);
    } finally {
      setLoading(false);
    }
  };

  const createChallenge = async () => {
    try {
      const response = await apiClient.post('/api/tasks/multiplayer/competitive/create', {});
      if (response.data.success) {
        alert('Challenge created! Waiting for an opponent.');
        loadChallenges();
      }
    } catch (error) {
      console.error('Error creating challenge:', error);
      alert('Failed to create challenge');
    }
  };

  const acceptChallenge = async (taskId) => {
    try {
      const response = await apiClient.post('/api/tasks/multiplayer/competitive/accept', {
        task_id: taskId
      });
      if (response.data.success) {
        alert('Challenge accepted! Prepare for battle!');
        setSelectedChallenge(null);
        loadChallenges();
      }
    } catch (error) {
      console.error('Error accepting challenge:', error);
      alert(error.response?.data?.detail || 'Failed to accept challenge');
    }
  };

  const getCategoryIcon = (category) => {
    const icons = {
      'combat': Swords,
      'speed_challenge': Zap,
      'economic': Trophy,
      'social': Target
    };
    return icons[category] || Target;
  };

  const getCategoryColor = (category) => {
    const colors = {
      'combat': 'text-red-500',
      'speed_challenge': 'text-yellow-500',
      'economic': 'text-green-500',
      'social': 'text-blue-500'
    };
    return colors[category] || 'text-gray-500';
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
            <Swords className="w-6 h-6" />
            Competitive Challenges
          </h2>
          <p className="text-gray-400 text-sm">Face off against other players in skill-based competitions</p>
        </div>
        <Button onClick={createChallenge} className="bg-red-600 hover:bg-red-700">
          Create Challenge
        </Button>
      </div>

      {/* Available Challenges */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {loading ? (
          <div className="col-span-full text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-red-500 mx-auto"></div>
            <p className="text-gray-400 mt-4">Loading challenges...</p>
          </div>
        ) : challenges.length === 0 ? (
          <div className="col-span-full text-center py-12">
            <Swords className="w-16 h-16 text-gray-600 mx-auto mb-4" />
            <p className="text-gray-400">No challenges available</p>
            <p className="text-gray-500 text-sm">Be the first to create one!</p>
          </div>
        ) : (
          challenges.map((challenge) => {
            const CategoryIcon = getCategoryIcon(challenge.category);
            const categoryColor = getCategoryColor(challenge.category);

            return (
              <Card
                key={challenge.task_id}
                className="bg-gray-900 border-gray-700 hover:border-red-500 transition-all cursor-pointer"
                onClick={() => setSelectedChallenge(challenge)}
              >
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg flex items-center gap-2">
                        <CategoryIcon className={`w-5 h-5 ${categoryColor}`} />
                        {challenge.title}
                      </CardTitle>
                      <CardDescription className="text-sm mt-1">
                        {challenge.description.substring(0, 100)}...
                      </CardDescription>
                    </div>
                    <Badge className={`${getDifficultyColor(challenge.difficulty)} text-white`}>
                      {challenge.difficulty}
                    </Badge>
                  </div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {/* Category */}
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-400">Category</span>
                      <span className="text-white font-medium capitalize">
                        {challenge.category?.replace('_', ' ')}
                      </span>
                    </div>

                    {/* Duration */}
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-400 flex items-center gap-1">
                        <Clock className="w-4 h-4" />
                        Duration
                      </span>
                      <span className="text-white font-medium">
                        {challenge.duration_minutes} min
                      </span>
                    </div>

                    {/* Required Skill */}
                    <div className="flex items-center justify-between text-sm">
                      <span className="text-gray-400">Required Skill</span>
                      <span className="text-white font-medium capitalize">
                        {challenge.required_skill} {challenge.min_skill_level}+
                      </span>
                    </div>

                    {/* Winner Rewards */}
                    <div className="mt-3 pt-3 border-t border-gray-700">
                      <p className="text-xs text-gray-400 mb-2">Winner Gets:</p>
                      <div className="flex items-center gap-3 text-sm">
                        <span className="text-yellow-400 font-medium">
                          {challenge.winner_rewards?.xp || 0} XP
                        </span>
                        <span className="text-green-400 font-medium">
                          {challenge.winner_rewards?.credits || 0} Credits
                        </span>
                        {challenge.winner_rewards?.items?.length > 0 && (
                          <Badge variant="outline" className="text-xs">
                            +Items
                          </Badge>
                        )}
                      </div>
                    </div>

                    {/* Accept Button */}
                    <Button
                      onClick={(e) => {
                        e.stopPropagation();
                        acceptChallenge(challenge.task_id);
                      }}
                      className="w-full mt-4 bg-red-600 hover:bg-red-700"
                    >
                      Accept Challenge
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>

      {/* Challenge Details Modal */}
      {selectedChallenge && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <Card className="bg-gray-900 border-gray-700 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
            <CardHeader>
              <CardTitle className="text-xl flex items-center gap-2">
                <Swords className="w-6 h-6 text-red-500" />
                {selectedChallenge.title}
              </CardTitle>
              <CardDescription>{selectedChallenge.description}</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Challenge Details */}
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-xs text-gray-400">Category</p>
                  <p className="text-lg font-bold capitalize">
                    {selectedChallenge.category?.replace('_', ' ')}
                  </p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-xs text-gray-400">Difficulty</p>
                  <p className="text-lg font-bold capitalize">{selectedChallenge.difficulty}</p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-xs text-gray-400">Duration</p>
                  <p className="text-lg font-bold">{selectedChallenge.duration_minutes} minutes</p>
                </div>
                <div className="bg-gray-800 p-4 rounded-lg">
                  <p className="text-xs text-gray-400">Required Skill</p>
                  <p className="text-lg font-bold capitalize">
                    {selectedChallenge.required_skill} {selectedChallenge.min_skill_level}+
                  </p>
                </div>
              </div>

              {/* Rewards Comparison */}
              <div className="space-y-2">
                <h3 className="font-bold">Rewards:</h3>
                <div className="grid grid-cols-2 gap-4">
                  {/* Winner */}
                  <div className="bg-yellow-500 bg-opacity-20 border border-yellow-500 p-4 rounded-lg">
                    <div className="flex items-center gap-2 mb-2">
                      <Trophy className="w-5 h-5 text-yellow-400" />
                      <p className="font-bold text-yellow-400">Winner</p>
                    </div>
                    <div className="space-y-1 text-sm">
                      <p>XP: <span className="font-bold">{selectedChallenge.winner_rewards?.xp || 0}</span></p>
                      <p>Credits: <span className="font-bold">{selectedChallenge.winner_rewards?.credits || 0}</span></p>
                      <p>Karma: <span className="font-bold">{selectedChallenge.winner_rewards?.karma || 0}</span></p>
                    </div>
                  </div>

                  {/* Loser */}
                  <div className="bg-gray-800 border border-gray-700 p-4 rounded-lg">
                    <p className="font-bold text-gray-400 mb-2">Runner-up</p>
                    <div className="space-y-1 text-sm text-gray-400">
                      <p>XP: <span className="font-bold">{selectedChallenge.loser_rewards?.xp || 0}</span></p>
                      <p>Credits: <span className="font-bold">{selectedChallenge.loser_rewards?.credits || 0}</span></p>
                      <p>Karma: <span className="font-bold">{selectedChallenge.loser_rewards?.karma || 0}</span></p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="flex gap-2 pt-4">
                <Button
                  onClick={() => acceptChallenge(selectedChallenge.task_id)}
                  className="flex-1 bg-red-600 hover:bg-red-700"
                >
                  Accept Challenge
                </Button>
                <Button
                  onClick={() => setSelectedChallenge(null)}
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

export default CompetitiveTasksPanel;
