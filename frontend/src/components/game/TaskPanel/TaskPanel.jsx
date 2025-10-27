/**
 * TaskPanel - Right-side panel showing current AI-generated task
 */
import React, { useState, useEffect } from 'react';
import './TaskPanel.css';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

const TaskPanel = ({ player, onTaskComplete }) => {
  const [currentTask, setCurrentTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [completing, setCompleting] = useState(false);
  const [coinBalance, setCoinBalance] = useState(player?.currencies?.credits || 0);

  // Fetch current task on mount
  useEffect(() => {
    fetchCurrentTask();
  }, []);

  // Update coin balance when player changes
  useEffect(() => {
    if (player?.currencies?.credits !== undefined) {
      setCoinBalance(player.currencies.credits);
    }
  }, [player]);

  const fetchCurrentTask = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch(`${BACKEND_URL}/api/tasks/current`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch current task');
      }

      const data = await response.json();
      setCurrentTask(data.task);

      // If no task, generate a new one
      if (!data.task) {
        await generateNewTask();
      }
    } catch (err) {
      console.error('Error fetching task:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const generateNewTask = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch(`${BACKEND_URL}/api/tasks/generate`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to generate task');
      }

      const data = await response.json();
      if (data.success) {
        setCurrentTask(data.task);
      } else {
        setError(data.error || 'Failed to generate task');
      }
    } catch (err) {
      console.error('Error generating task:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const completeTask = async () => {
    if (!currentTask) return;

    try {
      setCompleting(true);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch(`${BACKEND_URL}/api/tasks/complete`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_id: currentTask.task_id })
      });

      if (!response.ok) {
        throw new Error('Failed to complete task');
      }

      const data = await response.json();
      
      if (data.success) {
        // Update coin balance
        const newBalance = coinBalance + data.reward_breakdown.total_reward;
        setCoinBalance(newBalance);

        // Show success message
        alert(`Task completed! +${data.reward_breakdown.total_reward} coins!\n\nBase: ${data.reward_breakdown.base_reward}\nBonus: ${data.reward_breakdown.bonus_amount} (+${data.reward_breakdown.bonus_percentage}%)`);

        // Clear current task and generate new one
        setCurrentTask(null);
        
        // Notify parent component
        if (onTaskComplete) {
          onTaskComplete(data.reward_breakdown);
        }

        // Auto-generate new task after a short delay
        setTimeout(() => {
          generateNewTask();
        }, 1000);
      }
    } catch (err) {
      console.error('Error completing task:', err);
      setError(err.message);
    } finally {
      setCompleting(false);
    }
  };

  const getTimeRemaining = () => {
    if (!currentTask?.expires_at) return 'N/A';
    
    const expiresAt = new Date(currentTask.expires_at);
    const now = new Date();
    const diff = expiresAt - now;

    if (diff <= 0) {
      return 'Expired';
    }

    const minutes = Math.floor(diff / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const getTaskTypeIcon = (taskType) => {
    switch (taskType) {
      case 'good':
        return '✨';
      case 'bad':
        return '💀';
      default:
        return '⚡';
    }
  };

  const getTaskTypeLabel = (taskType) => {
    switch (taskType) {
      case 'good':
        return 'Virtuous Task';
      case 'bad':
        return 'Dark Task';
      default:
        return 'Neutral Task';
    }
  };

  if (loading && !currentTask) {
    return (
      <div className="task-panel">
        <div className="task-panel-header">
          <h3>🎯 CURRENT TASK</h3>
        </div>
        <div className="task-panel-content">
          <div className="task-loading">
            <div className="spinner"></div>
            <p>Loading task...</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="task-panel">
      <div className="task-panel-header">
        <h3>🎯 CURRENT TASK</h3>
      </div>

      <div className="task-panel-content">
        {error && (
          <div className="task-error">
            <p>{error}</p>
            <button onClick={generateNewTask} disabled={loading}>
              Try Again
            </button>
          </div>
        )}

        {currentTask ? (
          <div className="task-card">
            <div className="task-type">
              <span className="task-type-icon">{getTaskTypeIcon(currentTask.task_type)}</span>
              <span className="task-type-label">{getTaskTypeLabel(currentTask.task_type)}</span>
            </div>

            <div className="task-description">
              <p>{currentTask.description}</p>
            </div>

            <div className="task-reward">
              <span className="reward-icon">💰</span>
              <span className="reward-amount">Reward: {currentTask.base_reward} coins</span>
            </div>

            <div className="task-timer">
              <span className="timer-icon">⏱️</span>
              <span className="timer-value">Expires: {getTimeRemaining()}</span>
            </div>

            <button 
              className="task-complete-button"
              onClick={completeTask}
              disabled={completing}
            >
              {completing ? 'Completing...' : 'Complete Task'}
            </button>
          </div>
        ) : (
          <div className="no-task">
            <p>No active task</p>
            <button onClick={generateNewTask} disabled={loading}>
              {loading ? 'Generating...' : 'Get New Task'}
            </button>
          </div>
        )}
      </div>

      <div className="task-panel-footer">
        <div className="coin-balance">
          <span className="coin-icon">💰</span>
          <span className="coin-amount">Coins: {coinBalance.toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};

export default TaskPanel;
