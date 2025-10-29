import React, { useState, useEffect } from 'react';
import { X, Award, Coins, Star, TrendingUp } from 'lucide-react';
import initialTasksService from '../../../services/initialTasksService';
import './InitialTasksModal.css';

/**
 * Modal for displaying and completing initial tasks for new players
 */
const InitialTasksModal = ({ isOpen, onClose, onTaskCompleted }) => {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [completing, setCompleting] = useState(false);
  const [completionResult, setCompletionResult] = useState(null);

  useEffect(() => {
    if (isOpen) {
      loadTasks();
    }
  }, [isOpen]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await initialTasksService.getInitialTasks();
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to load initial tasks:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleTaskClick = (task) => {
    setSelectedTask(task);
    setCompletionResult(null);
  };

  const handleChoiceClick = async (choiceIndex) => {
    if (!selectedTask || completing) return;

    try {
      setCompleting(true);
      const result = await initialTasksService.completeTask(
        selectedTask.task_id,
        choiceIndex
      );
      
      setCompletionResult(result);
      
      // Remove completed task from list
      setTasks(tasks.filter(t => t.task_id !== selectedTask.task_id));
      
      // Notify parent component
      if (onTaskCompleted) {
        onTaskCompleted(result);
      }

      // Auto close after showing result
      setTimeout(() => {
        setSelectedTask(null);
        setCompletionResult(null);
      }, 3000);

    } catch (error) {
      console.error('Failed to complete task:', error);
      alert(error.userMessage || 'Failed to complete task. Please try again.');
    } finally {
      setCompleting(false);
    }
  };

  const getDifficultyColor = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'hard': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'moral_choice': return '🧐';
      case 'exploration': return '🧭';
      case 'skill_based': return '🛠️';
      case 'social': return '🤝';
      default: return '❔';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="initial-tasks-overlay">
      <div className="initial-tasks-modal">
        <div className="modal-header">
          <h2 className="modal-title">
            {selectedTask ? selectedTask.title : 'Your First Tasks'}
          </h2>
          <button className="close-button" onClick={onClose}>
            <X className="w-6 h-6" />
          </button>
        </div>

        {loading ? (
          <div className="modal-content loading">
            <div className="spinner"></div>
            <p>Loading tasks...</p>
          </div>
        ) : completionResult ? (
          <div className="modal-content completion-result">
            <div className="result-icon">&#x2705;</div>
            <h3>Task Completed!</h3>
            <p className="choice-text">{completionResult.choice_text}</p>
            
            <div className="rewards">
              <div className="reward-item">
                <Award className="w-5 h-5" />
                <span>+{completionResult.xp_gained} XP</span>
              </div>
              <div className="reward-item">
                <Coins className="w-5 h-5" />
                <span>+{completionResult.credits_gained} Credits</span>
              </div>
              {completionResult.karma_change !== 0 && (
                <div className={`reward-item ${completionResult.karma_change > 0 ? 'positive' : 'negative'}`}>
                  <Star className="w-5 h-5" />
                  <span>{completionResult.karma_change > 0 ? '+' : ''}{completionResult.karma_change} Karma</span>
                </div>
              )}
            </div>

            <div className="traits-changed">
              <h4><TrendingUp className="w-4 h-4" /> Traits Affected:</h4>
              <div className="trait-changes">
                {Object.entries(completionResult.traits_changed).map(([trait, change]) => {
                  if (trait === 'karma_points') return null;
                  return (
                    <div key={trait} className={`trait-change ${change > 0 ? 'positive' : 'negative'}`}>
                      <span className="trait-name">{trait.replace(/_/g, ' ')}</span>
                      <span className="trait-value">{change > 0 ? '+' : ''}{change}</span>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        ) : selectedTask ? (
          <div className="modal-content task-detail">
            <div className="task-header">
              <span className="task-type">{getTypeIcon(selectedTask.type)} {selectedTask.type.replace(/_/g, ' ')}</span>
              <span className={`task-difficulty ${getDifficultyColor(selectedTask.difficulty)}`}>
                {selectedTask.difficulty.toUpperCase()}
              </span>
            </div>

            <p className="task-description">{selectedTask.description}</p>

            <div className="task-rewards">
              <div className="reward">
                <Award className="w-4 h-4" />
                <span>{selectedTask.xp_reward} XP</span>
              </div>
              <div className="reward">
                <Coins className="w-4 h-4" />
                <span>{selectedTask.credits_reward} Credits</span>
              </div>
            </div>

            <div className="task-choices">
              <h4>What will you do?</h4>
              {selectedTask.choices.map((choice, index) => (
                <button
                  key={index}
                  className="choice-button"
                  onClick={() => handleChoiceClick(index)}
                  disabled={completing}
                >
                  {choice.text}
                </button>
              ))}
            </div>

            <button className="back-button" onClick={() => setSelectedTask(null)}>
              ← Back to Tasks
            </button>
          </div>
        ) : (
          <div className="modal-content">
            {tasks.length === 0 ? (
              <div className="no-tasks">
                <p>🎉 You've completed all initial tasks!</p>
                <p className="text-sm">Your character traits are now established. Continue playing to develop them further.</p>
              </div>
            ) : (
              <>
                <p className="intro-text">
                  Welcome! Complete these tasks to develop your character's traits and earn rewards.
                  Your choices will shape who you become in Karma Nexus.
                </p>
                <div className="tasks-list">
                  {tasks.map((task) => (
                    <div
                      key={task.id || task.task_id}
                      className="task-card"
                      onClick={() => handleTaskClick(task)}
                    >
                      <div className="task-card-header">
                        <span className="task-icon">{getTypeIcon(task.type)}</span>
                        <h3>{task.title}</h3>
                      </div>
                      <p className="task-summary">{task.description.substring(0, 100)}...</p>
                      <div className="task-card-footer">
                        <span className={`difficulty ${getDifficultyColor(task.difficulty)}`}>
                          {task.difficulty}
                        </span>
                        <span className="choices-count">
                          {task.choices?.length || 0} choices
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default InitialTasksModal;
