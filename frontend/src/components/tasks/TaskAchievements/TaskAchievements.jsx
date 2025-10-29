import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { Badge } from '../../ui/badge';
import { Trophy, Lock, Star, CheckCircle } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const TaskAchievements = () => {
  const [achievements, setAchievements] = useState({ earned: [], locked: [] });
  const [loading, setLoading] = useState(false);
  const [selectedAchievement, setSelectedAchievement] = useState(null);
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    loadAchievements();
  }, []);

  const loadAchievements = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/tasks/analytics/achievements');
      if (response.data.success) {
        setAchievements(response.data.achievements);
      }
    } catch (error) {
      console.error('Error loading achievements:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadProgress = async (achievementId) => {
    try {
      const response = await apiClient.get(`/api/tasks/analytics/achievements/${achievementId}/progress`);
      if (response.data.success) {
        setProgress(response.data.progress);
      }
    } catch (error) {
      console.error('Error loading progress:', error);
    }
  };

  const checkForNewAchievements = async () => {
    try {
      const response = await apiClient.post('/api/tasks/analytics/achievements/check');
      if (response.data.success && response.data.newly_earned.length > 0) {
        alert(`🏆 New Achievement${response.data.newly_earned.length > 1 ? 's' : ''} Unlocked!\n${response.data.newly_earned.map(a => a.name).join(', ')}`);
        loadAchievements();
      } else {
        alert('No new achievements unlocked. Keep completing tasks!');
      }
    } catch (error) {
      console.error('Error checking achievements:', error);
    }
  };

  const handleAchievementClick = (achievement, isLocked) => {
    setSelectedAchievement(achievement);
    if (isLocked) {
      loadProgress(achievement.id);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-3xl font-bold flex items-center gap-2">
            <Trophy className="w-8 h-8 text-yellow-500" />
            Task Achievements
          </h2>
          <p className="text-gray-400 text-sm mt-1">Track your accomplishments and milestones</p>
        </div>
        <button
          onClick={checkForNewAchievements}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-all"
        >
          Check for New
        </button>
      </div>

      {/* Progress Summary */}
      <Card className="bg-gradient-to-br from-yellow-900 to-yellow-800 border-yellow-700">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-yellow-200 text-sm">Achievements Unlocked</p>
              <p className="text-4xl font-bold text-white">
                {achievements.total_earned} / {achievements.total_available}
              </p>
            </div>
            <div className="text-right">
              <p className="text-yellow-200 text-sm">Completion</p>
              <p className="text-4xl font-bold text-yellow-300">{achievements.completion_percentage}%</p>
            </div>
            <div className="w-32 h-32">
              <svg viewBox="0 0 100 100" className="transform -rotate-90">
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="none"
                  stroke="rgba(255,255,255,0.2)"
                  strokeWidth="8"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="40"
                  fill="none"
                  stroke="#FCD34D"
                  strokeWidth="8"
                  strokeDasharray={`${(achievements.completion_percentage || 0) * 2.51} 251`}
                  strokeLinecap="round"
                />
              </svg>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Earned Achievements */}
      <div>
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <CheckCircle className="w-5 h-5 text-green-500" />
          Earned ({achievements.total_earned})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {loading ? (
            <div className="col-span-full text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto"></div>
            </div>
          ) : achievements.earned.length === 0 ? (
            <div className="col-span-full text-center py-12">
              <Trophy className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No achievements earned yet</p>
            </div>
          ) : (
            achievements.earned.map((achievement) => (
              <Card
                key={achievement.id}
                className="bg-gradient-to-br from-green-900 to-green-800 border-green-700 cursor-pointer hover:scale-105 transition-all"
                onClick={() => handleAchievementClick(achievement, false)}
              >
                <CardContent className="p-4">
                  <div className="text-center">
                    <div className="text-5xl mb-2">{achievement.icon}</div>
                    <h4 className="font-bold text-lg text-white">{achievement.name}</h4>
                    <p className="text-sm text-green-200 mt-1">{achievement.description}</p>
                    
                    {/* Rewards */}
                    <div className="mt-3 pt-3 border-t border-green-700">
                      <div className="flex items-center justify-center gap-2 flex-wrap">
                        {achievement.rewards?.xp && (
                          <Badge className="bg-yellow-600">+{achievement.rewards.xp} XP</Badge>
                        )}
                        {achievement.rewards?.credits && (
                          <Badge className="bg-green-600">+{achievement.rewards.credits} Credits</Badge>
                        )}
                        {achievement.rewards?.items && (
                          <Badge className="bg-purple-600">+Items</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>
      </div>

      {/* Locked Achievements */}
      <div>
        <h3 className="text-xl font-bold mb-4 flex items-center gap-2">
          <Lock className="w-5 h-5 text-gray-500" />
          Locked ({achievements.locked?.length || 0})
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {achievements.locked && achievements.locked.length > 0 ? (
            achievements.locked.map((achievement) => (
              <Card
                key={achievement.id}
                className="bg-gray-900 border-gray-700 cursor-pointer hover:border-gray-600 transition-all"
                onClick={() => handleAchievementClick(achievement, true)}
              >
                <CardContent className="p-4">
                  <div className="text-center opacity-60">
                    <div className="text-5xl mb-2 filter grayscale">{achievement.icon}</div>
                    <h4 className="font-bold text-lg text-gray-300">{achievement.name}</h4>
                    <p className="text-sm text-gray-400 mt-1">{achievement.description}</p>
                    
                    {/* Rewards */}
                    <div className="mt-3 pt-3 border-t border-gray-700">
                      <div className="flex items-center justify-center gap-2 flex-wrap">
                        {achievement.rewards?.xp && (
                          <Badge variant="outline" className="text-xs">+{achievement.rewards.xp} XP</Badge>
                        )}
                        {achievement.rewards?.credits && (
                          <Badge variant="outline" className="text-xs">+{achievement.rewards.credits} Credits</Badge>
                        )}
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))
          ) : (
            <div className="col-span-full text-center py-12">
              <Star className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">All achievements unlocked! 🎉</p>
            </div>
          )}
        </div>
      </div>

      {/* Achievement Detail Modal */}
      {selectedAchievement && (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4">
          <Card className="bg-gray-900 border-gray-700 max-w-md w-full">
            <CardHeader>
              <CardTitle className="text-center">
                <div className="text-6xl mb-2">{selectedAchievement.icon}</div>
                <p className="text-xl">{selectedAchievement.name}</p>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-center text-gray-300 mb-4">{selectedAchievement.description}</p>
              
              {/* Progress Bar (for locked achievements) */}
              {progress && !progress.completed && (
                <div className="mb-4">
                  <div className="flex items-center justify-between text-sm mb-2">
                    <span>Progress</span>
                    <span className="font-bold">{progress.current} / {progress.target}</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                      style={{ width: `${progress.percentage}%` }}
                    ></div>
                  </div>
                  <p className="text-center text-sm text-gray-400 mt-2">{progress.percentage}% complete</p>
                </div>
              )}

              {/* Rewards */}
              <div className="bg-gray-800 p-4 rounded-lg">
                <p className="text-sm text-gray-400 mb-2">Rewards:</p>
                <div className="space-y-1">
                  {selectedAchievement.rewards?.xp && (
                    <p className="text-yellow-400">+{selectedAchievement.rewards.xp} XP</p>
                  )}
                  {selectedAchievement.rewards?.credits && (
                    <p className="text-green-400">+{selectedAchievement.rewards.credits} Credits</p>
                  )}
                  {selectedAchievement.rewards?.karma && (
                    <p className="text-blue-400">+{selectedAchievement.rewards.karma} Karma</p>
                  )}
                  {selectedAchievement.rewards?.items && (
                    <p className="text-purple-400">Special Items</p>
                  )}
                </div>
              </div>

              <button
                onClick={() => {
                  setSelectedAchievement(null);
                  setProgress(null);
                }}
                className="w-full mt-4 px-4 py-2 bg-gray-700 hover:bg-gray-600 rounded-lg transition-all"
              >
                Close
              </button>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

export default TaskAchievements;
