import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Coins, Clock, Target, RefreshCw, Loader2 } from 'lucide-react';
import './TaskPanel.css';

const TaskPanel = ({ player }) => {
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [completing, setCompleting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchCurrentTask();
  }, []);

  const fetchCurrentTask = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/tasks/current', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      if (data.success && data.task) {
        setTask(data.task);
      } else {
        setTask(null);
      }
    } catch (err) {
      console.error('Error fetching task:', err);
    } finally {
      setLoading(false);
    }
  };

  const generateNewTask = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch('/api/tasks/generate', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      
      if (data.success) {
        setTask(data.task);
      } else {
        setError(data.error || 'Failed to generate task');
      }
    } catch (err) {
      setError('Network error. Please try again.');
      console.error('Error generating task:', err);
    } finally {
      setLoading(false);
    }
  };

  const completeTask = async () => {
    if (!task) return;
    
    try {
      setCompleting(true);
      const response = await fetch('/api/tasks/complete', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ task_id: task._id })
      });
      const data = await response.json();
      
      if (data.success) {
        // Show reward notification
        alert(`Task completed! You earned ${data.actual_reward} coins!\n` + 
              `${data.bonus_percentage > 0 ? `(+${data.bonus_percentage}% bonus from ornaments)` : ''}`);
        
        // Clear task and fetch new one
        setTask(null);
        setTimeout(() => {
          fetchCurrentTask();
        }, 1000);
      }
    } catch (err) {
      console.error('Error completing task:', err);
      alert('Failed to complete task. Please try again.');
    } finally {
      setCompleting(false);
    }
  };

  const getTaskTypeColor = () => {
    if (!task) return 'neutral';
    switch (task.task_type) {
      case 'good': return 'text-green-400';
      case 'bad': return 'text-red-400';
      default: return 'text-yellow-400';
    }
  };

  const formatTimeRemaining = () => {
    if (!task || !task.expires_at) return 'N/A';
    const now = new Date();
    const expires = new Date(task.expires_at);
    const diff = expires - now;
    
    if (diff <= 0) return 'Expired';
    
    const hours = Math.floor(diff / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    
    return `${hours}h ${minutes}m`;
  };

  return (
    <div className="task-panel">
      <Card className="task-card">
        <div className="task-header">
          <Target className="w-5 h-5" />
          <h3>Current Task</h3>
        </div>

        {loading && (
          <div className="task-loading">
            <Loader2 className="w-8 h-8 animate-spin" />
            <p>Loading task...</p>
          </div>
        )}

        {error && (
          <div className="task-error">
            <p>{error}</p>
          </div>
        )}

        {!loading && !task && !error && (
          <div className="no-task">
            <p>No active task</p>
            <Button onClick={generateNewTask} disabled={loading}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Generate Task
            </Button>
          </div>
        )}

        {!loading && task && (
          <div className="task-content">
            <div className={`task-type ${getTaskTypeColor()}`}>
              {task.task_type?.toUpperCase() || 'TASK'}
            </div>

            <h4 className="task-title">{task.title}</h4>
            <p className="task-description">{task.description}</p>

            <div className="task-details">
              <div className="task-detail">
                <Coins className="w-4 h-4" />
                <span>Reward: {task.coin_reward} coins</span>
              </div>

              <div className="task-detail">
                <Clock className="w-4 h-4" />
                <span>Expires: {formatTimeRemaining()}</span>
              </div>
            </div>

            <div className="task-actions">
              <Button 
                onClick={completeTask} 
                disabled={completing}
                className="complete-btn"
              >
                {completing ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Completing...
                  </>
                ) : (
                  'Complete Task'
                )}
              </Button>
            </div>
          </div>
        )}
      </Card>

      <div className="coin-display">
        <Coins className="w-5 h-5 text-yellow-400" />
        <span>Coins: {player?.currencies?.credits?.toLocaleString() || 0}</span>
      </div>
    </div>
  );
};

export default TaskPanel;
