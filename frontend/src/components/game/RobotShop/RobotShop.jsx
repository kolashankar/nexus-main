import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bot, ShoppingCart, DollarSign, Wrench, TrendingUp, Zap } from 'lucide-react';
import './RobotShop.css';

/**
 * Robot Shop Component
 * Buy, sell, and upgrade robots
 */
const RobotShop = ({ player, isOpen, onClose, onTransaction }) => {
  const [robots, setRobots] = useState([]);
  const [playerRobots, setPlayerRobots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('buy'); // 'buy', 'sell', 'upgrade'

  // Robot types with base stats
  const robotTypes = [
    { 
      id: 'scout', 
      name: 'Scout Bot', 
      basePrice: 1000,
      upgradeCost: 500,
      description: 'Fast reconnaissance unit',
      stats: { speed: 90, combat: 30, utility: 60 },
      color: '#2196F3',
      uses: 'Explore territories, gather intel, detect hidden items'
    },
    { 
      id: 'trader', 
      name: 'Trader Bot', 
      basePrice: 1500,
      upgradeCost: 750,
      description: 'Commerce specialist',
      stats: { speed: 50, combat: 20, utility: 85 },
      color: '#FFB74D',
      uses: 'Increase coin rewards, access special markets, negotiate prices'
    },
    { 
      id: 'combat', 
      name: 'Combat Bot', 
      basePrice: 2500,
      upgradeCost: 1250,
      description: 'Battle-ready warrior',
      stats: { speed: 60, combat: 95, utility: 40 },
      color: '#F44336',
      uses: 'Win PvP battles, protect from attacks, raid territories'
    },
    { 
      id: 'medic', 
      name: 'Medic Bot', 
      basePrice: 2000,
      upgradeCost: 1000,
      description: 'Healing and support',
      stats: { speed: 55, combat: 30, utility: 90 },
      color: '#4CAF50',
      uses: 'Heal HP, revive defeated robots, boost trait recovery'
    },
    { 
      id: 'hacker', 
      name: 'Hacker Bot', 
      basePrice: 3000,
      upgradeCost: 1500,
      description: 'Cyber warfare unit',
      stats: { speed: 70, combat: 50, utility: 95 },
      color: '#9C27B0',
      uses: 'Hack systems, steal data, disable enemy robots, bypass security'
    },
    { 
      id: 'guardian', 
      name: 'Guardian Bot', 
      basePrice: 2800,
      upgradeCost: 1400,
      description: 'Defensive powerhouse',
      stats: { speed: 40, combat: 85, utility: 70 },
      color: '#607D8B',
      uses: 'Defend territories, block attacks, protect assets'
    },
    { 
      id: 'harvester', 
      name: 'Harvester Bot', 
      basePrice: 1800,
      upgradeCost: 900,
      description: 'Resource collector',
      stats: { speed: 50, combat: 25, utility: 88 },
      color: '#795548',
      uses: 'Gather resources passively, increase income, collect rare items'
    },
    { 
      id: 'tactical', 
      name: 'Tactical Bot', 
      basePrice: 3500,
      upgradeCost: 1750,
      description: 'Strategic commander',
      stats: { speed: 65, combat: 75, utility: 80 },
      color: '#546E7A',
      uses: 'Coordinate attacks, boost team performance, analyze battles'
    },
    { 
      id: 'assault', 
      name: 'Assault Bot', 
      basePrice: 4000,
      upgradeCost: 2000,
      description: 'Aggressive attacker',
      stats: { speed: 75, combat: 98, utility: 45 },
      color: '#E53935',
      uses: 'Maximum damage, break defenses, dominate combat'
    }
  ];

  useEffect(() => {
    if (isOpen) {
      fetchRobotData();
    }
  }, [isOpen, activeTab]);

  const fetchRobotData = async () => {
    try {
      setLoading(true);
      
      // Fetch player's robots
      const response = await fetch('/api/robots/my-robots', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      
      if (data.success) {
        setPlayerRobots(data.robots || []);
      }
    } catch (err) {
      console.error('Error fetching robot data:', err);
    } finally {
      setLoading(false);
    }
  };

  const buyRobot = async (robotType) => {
    try {
      const response = await fetch('/api/robots/purchase', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ robot_type: robotType.id })
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Successfully purchased ${robotType.name}!\n` +
              `Cost: $${robotType.basePrice}\n` +
              `New balance: $${data.new_balance}`);
        
        await fetchRobotData();
        if (onTransaction) onTransaction(data);
      } else {
        alert(`❌ ${data.error || 'Purchase failed'}`);
      }
    } catch (err) {
      console.error('Error purchasing robot:', err);
      alert('Network error. Please try again.');
    }
  };

  const sellRobot = async (robot) => {
    const sellPrice = Math.floor(robot.purchase_price * 0.6); // 60% of purchase price
    
    if (!confirm(`Sell ${robot.name} for $${sellPrice}?`)) return;
    
    try {
      const response = await fetch('/api/robots/sell', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ robot_id: robot._id })
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Sold ${robot.name} for $${sellPrice}!`);
        await fetchRobotData();
        if (onTransaction) onTransaction(data);
      } else {
        alert(`❌ ${data.error || 'Sale failed'}`);
      }
    } catch (err) {
      console.error('Error selling robot:', err);
      alert('Network error. Please try again.');
    }
  };

  const upgradeRobot = async (robot) => {
    const robotType = robotTypes.find(r => r.id === robot.type);
    const upgradeCost = robotType?.upgradeCost || 500;
    
    if (!confirm(`Upgrade ${robot.name} for ${upgradeCost} coins?\n+10% to all stats`)) return;
    
    try {
      const response = await fetch('/api/robots/upgrade', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ robot_id: robot._id })
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ ${robot.name} upgraded to level ${data.robot.level}!\n` +
              `New stats: Speed ${data.robot.stats.speed}, Combat ${data.robot.stats.combat}, Utility ${data.robot.stats.utility}`);
        await fetchRobotData();
        if (onTransaction) onTransaction(data);
      } else {
        alert(`❌ ${data.error || 'Upgrade failed'}`);
      }
    } catch (err) {
      console.error('Error upgrading robot:', err);
      alert('Network error. Please try again.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="robot-shop-overlay" onClick={onClose}>
      <Card className="robot-shop-modal" onClick={(e) => e.stopPropagation()}>
        <div className="robot-shop-header">
          <Bot className="w-6 h-6" />
          <h2>Robot Shop</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        {/* Balance Display */}
        <div className="balance-display">
          <div className="balance-item">
            <DollarSign className="w-5 h-5 text-green-400" />
            <span>Cash: ${player?.currencies?.credits?.toLocaleString() || 0}</span>
          </div>
          <div className="balance-item">
            <Zap className="w-5 h-5 text-yellow-400" />
            <span>Coins: {player?.coins?.toLocaleString() || 0}</span>
          </div>
        </div>

        {/* Tabs */}
        <div className="robot-shop-tabs">
          <button 
            className={`tab ${activeTab === 'buy' ? 'active' : ''}`}
            onClick={() => setActiveTab('buy')}
          >
            <ShoppingCart className="w-4 h-4" />
            Buy Robots
          </button>
          <button 
            className={`tab ${activeTab === 'sell' ? 'active' : ''}`}
            onClick={() => setActiveTab('sell')}
          >
            <DollarSign className="w-4 h-4" />
            Sell Robots
          </button>
          <button 
            className={`tab ${activeTab === 'upgrade' ? 'active' : ''}`}
            onClick={() => setActiveTab('upgrade')}
          >
            <Wrench className="w-4 h-4" />
            Upgrade Robots
          </button>
        </div>

        {/* Content */}
        <div className="robot-shop-content">
          {loading ? (
            <div className="loading">Loading...</div>
          ) : (
            <>
              {activeTab === 'buy' && (
                <div className="robots-grid">
                  {robotTypes.map(robot => (
                    <Card key={robot.id} className="robot-card" style={{ borderColor: robot.color }}>
                      <div className="robot-icon" style={{ backgroundColor: robot.color + '20' }}>
                        <Bot className="w-12 h-12" style={{ color: robot.color }} />
                      </div>
                      <h3>{robot.name}</h3>
                      <p className="robot-description">{robot.description}</p>
                      
                      <div className="robot-stats">
                        <div className="stat">
                          <span>Speed</span>
                          <div className="stat-bar">
                            <div className="stat-fill" style={{ width: `${robot.stats.speed}%`, backgroundColor: robot.color }}></div>
                          </div>
                          <span>{robot.stats.speed}</span>
                        </div>
                        <div className="stat">
                          <span>Combat</span>
                          <div className="stat-bar">
                            <div className="stat-fill" style={{ width: `${robot.stats.combat}%`, backgroundColor: robot.color }}></div>
                          </div>
                          <span>{robot.stats.combat}</span>
                        </div>
                        <div className="stat">
                          <span>Utility</span>
                          <div className="stat-bar">
                            <div className="stat-fill" style={{ width: `${robot.stats.utility}%`, backgroundColor: robot.color }}></div>
                          </div>
                          <span>{robot.stats.utility}</span>
                        </div>
                      </div>
                      
                      <div className="robot-uses">
                        <strong>Uses:</strong>
                        <p>{robot.uses}</p>
                      </div>
                      
                      <div className="robot-price">
                        <DollarSign className="w-5 h-5" />
                        <span>${robot.basePrice}</span>
                      </div>
                      
                      <Button onClick={() => buyRobot(robot)} className="buy-button">
                        Purchase
                      </Button>
                    </Card>
                  ))}
                </div>
              )}

              {activeTab === 'sell' && (
                <div className="robots-grid">
                  {playerRobots.length === 0 ? (
                    <div className="empty-state">
                      <Bot className="w-16 h-16 opacity-30" />
                      <p>You don't own any robots yet!</p>
                      <Button onClick={() => setActiveTab('buy')}>Buy Robots</Button>
                    </div>
                  ) : (
                    playerRobots.map(robot => {
                      const robotType = robotTypes.find(r => r.id === robot.type);
                      const sellPrice = Math.floor(robot.purchase_price * 0.6);
                      
                      return (
                        <Card key={robot._id} className="robot-card owned" style={{ borderColor: robotType?.color }}>
                          <div className="robot-icon" style={{ backgroundColor: robotType?.color + '20' }}>
                            <Bot className="w-12 h-12" style={{ color: robotType?.color }} />
                          </div>
                          <h3>{robot.name}</h3>
                          <p className="robot-level">Level {robot.level || 1}</p>
                          
                          <div className="robot-stats">
                            <div className="stat">
                              <span>Speed</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.speed || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.speed || 50}</span>
                            </div>
                            <div className="stat">
                              <span>Combat</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.combat || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.combat || 50}</span>
                            </div>
                            <div className="stat">
                              <span>Utility</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.utility || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.utility || 50}</span>
                            </div>
                          </div>
                          
                          <div className="robot-price sell">
                            <DollarSign className="w-5 h-5" />
                            <span>${sellPrice}</span>
                            <span className="sell-note">(60% of purchase price)</span>
                          </div>
                          
                          <Button onClick={() => sellRobot(robot)} variant="destructive" className="sell-button">
                            Sell
                          </Button>
                        </Card>
                      );
                    })
                  )}
                </div>
              )}

              {activeTab === 'upgrade' && (
                <div className="robots-grid">
                  {playerRobots.length === 0 ? (
                    <div className="empty-state">
                      <Wrench className="w-16 h-16 opacity-30" />
                      <p>You don't own any robots to upgrade!</p>
                      <Button onClick={() => setActiveTab('buy')}>Buy Robots</Button>
                    </div>
                  ) : (
                    playerRobots.map(robot => {
                      const robotType = robotTypes.find(r => r.id === robot.type);
                      const upgradeCost = robotType?.upgradeCost || 500;
                      const currentLevel = robot.level || 1;
                      const maxLevel = 10;
                      
                      return (
                        <Card key={robot._id} className="robot-card upgrade" style={{ borderColor: robotType?.color }}>
                          <div className="robot-icon" style={{ backgroundColor: robotType?.color + '20' }}>
                            <Bot className="w-12 h-12" style={{ color: robotType?.color }} />
                          </div>
                          <h3>{robot.name}</h3>
                          <p className="robot-level">Level {currentLevel} / {maxLevel}</p>
                          
                          <div className="robot-stats">
                            <div className="stat">
                              <span>Speed</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.speed || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.speed || 50}</span>
                              <TrendingUp className="w-4 h-4 text-green-400" />
                            </div>
                            <div className="stat">
                              <span>Combat</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.combat || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.combat || 50}</span>
                              <TrendingUp className="w-4 h-4 text-green-400" />
                            </div>
                            <div className="stat">
                              <span>Utility</span>
                              <div className="stat-bar">
                                <div className="stat-fill" style={{ width: `${robot.stats?.utility || 50}%`, backgroundColor: robotType?.color }}></div>
                              </div>
                              <span>{robot.stats?.utility || 50}</span>
                              <TrendingUp className="w-4 h-4 text-green-400" />
                            </div>
                          </div>
                          
                          <div className="upgrade-info">
                            <Wrench className="w-5 h-5 text-yellow-400" />
                            <span>+10% to all stats</span>
                          </div>
                          
                          <div className="robot-price upgrade-cost">
                            <Zap className="w-5 h-5 text-yellow-400" />
                            <span>{upgradeCost} coins</span>
                          </div>
                          
                          {currentLevel >= maxLevel ? (
                            <Button disabled className="max-level-button">
                              Max Level Reached
                            </Button>
                          ) : (
                            <Button onClick={() => upgradeRobot(robot)} className="upgrade-button">
                              Upgrade
                            </Button>
                          )}
                        </Card>
                      );
                    })
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </Card>
    </div>
  );
};

export default RobotShop;
