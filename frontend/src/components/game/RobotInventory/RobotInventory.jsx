import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bot, TrendingUp, Trash2, Edit2, Loader2, Shield, Zap, Activity } from 'lucide-react';
import './RobotInventory.css';

/**
 * Robot Inventory Component
 * View and manage player's owned robots
 */
const RobotInventory = ({ player, isOpen, onClose, onUpdate }) => {
  const [robots, setRobots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRobot, setSelectedRobot] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchMyRobots();
    }
  }, [isOpen]);

  const fetchMyRobots = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/robots/my-robots', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        setRobots(data.robots || []);
      }
    } catch (err) {
      console.error('Error fetching robots:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteRobot = async (robotId) => {
    if (!confirm('Are you sure you want to scrap this robot? This cannot be undone.')) {
      return;
    }

    try {
      const response = await fetch(`/api/robots/${robotId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        alert('✅ Robot scrapped successfully!');
        await fetchMyRobots();
        if (onUpdate) onUpdate();
      } else {
        alert(`❌ ${data.error || 'Failed to scrap robot'}`);
      }
    } catch (err) {
      console.error('Error deleting robot:', err);
      alert('Network error. Please try again.');
    }
  };

  const renameRobot = async (robot) => {
    const newName = prompt('Enter new name for robot:', robot.name || robot.type);
    if (!newName || newName === robot.name) return;

    try {
      const response = await fetch(`/api/robots/${robot._id}/name`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ new_name: newName })
      });
      const data = await response.json();
      
      if (data.success) {
        alert('✅ Robot renamed successfully!');
        await fetchMyRobots();
      } else {
        alert(`❌ ${data.error || 'Failed to rename robot'}`);
      }
    } catch (err) {
      console.error('Error renaming robot:', err);
      alert('Network error. Please try again.');
    }
  };

  const getRobotColor = (type) => {
    const colors = {
      scout: '#2196F3',
      trader: '#FFB74D',
      combat: '#F44336',
      medic: '#4CAF50',
      hacker: '#9C27B0',
      guardian: '#607D8B',
      harvester: '#795548',
      tactical: '#546E7A',
      assault: '#E53935'
    };
    return colors[type] || '#8B5CF6';
  };

  const getRobotIcon = (type) => {
    const icons = {
      scout: '🔍',
      trader: '💰',
      combat: '⚔️',
      medic: '🏥',
      hacker: '💻',
      guardian: '🛡️',
      harvester: '⛏️',
      tactical: '🎯',
      assault: '💥'
    };
    return icons[type] || '🤖';
  };

  if (!isOpen) return null;

  return (
    <div className="robot-inventory-overlay" onClick={onClose}>
      <div className="robot-inventory-container" onClick={(e) => e.stopPropagation()}>
        <Card className="robot-inventory-modal">
          {/* Header */}
          <div className="inventory-header">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6 text-purple-400" />
              <h2 className="text-2xl font-bold text-white">My Robots</h2>
              <span className="robot-count">{robots.length}</span>
            </div>
            <button className="close-btn" onClick={onClose}>×</button>
          </div>

          {/* Content */}
          <div className="inventory-content">
            {loading ? (
              <div className="loading-state">
                <Loader2 className="w-12 h-12 animate-spin text-purple-400" />
                <p className="text-gray-400 mt-4">Loading your robots...</p>
              </div>
            ) : robots.length === 0 ? (
              <div className="empty-state">
                <Bot className="w-20 h-20 text-gray-600 mb-4" />
                <h3 className="text-xl font-bold text-gray-400 mb-2">No Robots Yet</h3>
                <p className="text-gray-500 mb-6">Visit the Robot Market to purchase your first robot!</p>
                <Button onClick={onClose} className="bg-purple-600 hover:bg-purple-700">
                  Go to Market
                </Button>
              </div>
            ) : (
              <div className="robots-inventory-grid">
                {robots.map(robot => {
                  const color = getRobotColor(robot.type);
                  const icon = getRobotIcon(robot.type);
                  
                  return (
                    <Card 
                      key={robot._id} 
                      className="inventory-robot-card"
                      style={{ borderColor: color + '40' }}
                    >
                      {/* Robot Header */}
                      <div className="robot-inventory-header" style={{ background: `linear-gradient(135deg, ${color}20, transparent)` }}>
                        <div className="robot-inventory-icon" style={{ backgroundColor: color + '20' }}>
                          <span className="text-3xl">{icon}</span>
                        </div>
                        <div className="robot-level-badge" style={{ backgroundColor: color + '30', borderColor: color }}>
                          <TrendingUp className="w-3 h-3" />
                          <span>Lv {robot.level || 1}</span>
                        </div>
                      </div>

                      {/* Robot Info */}
                      <div className="robot-inventory-body">
                        <h3 className="robot-inventory-name" style={{ color }}>
                          {robot.name || robot.type}
                        </h3>
                        <p className="robot-inventory-type">{robot.type?.toUpperCase()}</p>

                        {/* Stats */}
                        <div className="robot-inventory-stats">
                          <div className="inventory-stat">
                            <Activity className="w-4 h-4 text-blue-400" />
                            <div>
                              <span className="stat-label">Speed</span>
                              <span className="stat-value">{robot.stats?.speed || 50}</span>
                            </div>
                          </div>

                          <div className="inventory-stat">
                            <Shield className="w-4 h-4 text-red-400" />
                            <div>
                              <span className="stat-label">Combat</span>
                              <span className="stat-value">{robot.stats?.combat || 50}</span>
                            </div>
                          </div>

                          <div className="inventory-stat">
                            <Zap className="w-4 h-4 text-yellow-400" />
                            <div>
                              <span className="stat-label">Utility</span>
                              <span className="stat-value">{robot.stats?.utility || 50}</span>
                            </div>
                          </div>
                        </div>

                        {/* Purchase Info */}
                        <div className="robot-purchase-info">
                          <span className="purchase-label">Purchased:</span>
                          <span className="purchase-value">
                            {new Date(robot.created_at).toLocaleDateString()}
                          </span>
                        </div>
                      </div>

                      {/* Actions */}
                      <div className="robot-inventory-actions">
                        <Button
                          onClick={() => renameRobot(robot)}
                          variant="outline"
                          size="sm"
                          className="action-btn rename-btn"
                        >
                          <Edit2 className="w-4 h-4" />
                        </Button>
                        <Button
                          onClick={() => deleteRobot(robot._id)}
                          variant="outline"
                          size="sm"
                          className="action-btn delete-btn"
                        >
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </Card>
                  );
                })}
              </div>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default RobotInventory;