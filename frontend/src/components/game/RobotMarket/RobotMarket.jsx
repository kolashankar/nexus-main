import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bot, Search, Filter, Loader2 } from 'lucide-react';
import RobotCard from './RobotCard';
import RobotFilters from './RobotFilters';
import './RobotMarket.css';

/**
 * Robot Market Component
 * Advanced robot marketplace with filtering and sorting
 */
const RobotMarket = ({ player, isOpen, onClose, onPurchase }) => {
  const [robots, setRobots] = useState([]);
  const [filteredRobots, setFilteredRobots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    type: 'all',
    priceRange: 'all',
    sortBy: 'price-asc'
  });

  // Robot types with enhanced data
  const robotTypes = [
    { 
      id: 'scout', 
      name: 'Scout Bot', 
      basePrice: 1000,
      type: 'utility',
      description: 'Fast reconnaissance unit',
      stats: { speed: 90, combat: 30, utility: 60 },
      color: '#2196F3',
      icon: '🔍',
      abilities: ['Explore territories', 'Detect hidden items', 'Map areas']
    },
    { 
      id: 'trader', 
      name: 'Trader Bot', 
      basePrice: 1500,
      type: 'economy',
      description: 'Commerce specialist',
      stats: { speed: 50, combat: 20, utility: 85 },
      color: '#FFB74D',
      icon: '💰',
      abilities: ['Increase coin rewards', 'Access special markets', 'Negotiate prices']
    },
    { 
      id: 'combat', 
      name: 'Combat Bot', 
      basePrice: 2500,
      type: 'combat',
      description: 'Battle-ready warrior',
      stats: { speed: 60, combat: 95, utility: 40 },
      color: '#F44336',
      icon: '⚔️',
      abilities: ['Win PvP battles', 'Protect from attacks', 'Raid territories']
    },
    { 
      id: 'medic', 
      name: 'Medic Bot', 
      basePrice: 2000,
      type: 'support',
      description: 'Healing and support',
      stats: { speed: 55, combat: 30, utility: 90 },
      color: '#4CAF50',
      icon: '🏥',
      abilities: ['Heal HP', 'Revive robots', 'Boost trait recovery']
    },
    { 
      id: 'hacker', 
      name: 'Hacker Bot', 
      basePrice: 3000,
      type: 'special',
      description: 'Cyber warfare unit',
      stats: { speed: 70, combat: 50, utility: 95 },
      color: '#9C27B0',
      icon: '💻',
      abilities: ['Hack systems', 'Steal data', 'Disable enemies']
    },
    { 
      id: 'guardian', 
      name: 'Guardian Bot', 
      basePrice: 2800,
      type: 'combat',
      description: 'Defensive powerhouse',
      stats: { speed: 40, combat: 85, utility: 70 },
      color: '#607D8B',
      icon: '🛡️',
      abilities: ['Defend territories', 'Block attacks', 'Protect assets']
    },
    { 
      id: 'harvester', 
      name: 'Harvester Bot', 
      basePrice: 1800,
      type: 'economy',
      description: 'Resource collector',
      stats: { speed: 50, combat: 25, utility: 88 },
      color: '#795548',
      icon: '⛏️',
      abilities: ['Gather resources', 'Increase income', 'Collect rare items']
    },
    { 
      id: 'tactical', 
      name: 'Tactical Bot', 
      basePrice: 3500,
      type: 'special',
      description: 'Strategic commander',
      stats: { speed: 65, combat: 75, utility: 80 },
      color: '#546E7A',
      icon: '🎯',
      abilities: ['Coordinate attacks', 'Boost team', 'Analyze battles']
    },
    { 
      id: 'assault', 
      name: 'Assault Bot', 
      basePrice: 4000,
      type: 'combat',
      description: 'Aggressive attacker',
      stats: { speed: 75, combat: 98, utility: 45 },
      color: '#E53935',
      icon: '💥',
      abilities: ['Maximum damage', 'Break defenses', 'Dominate combat']
    }
  ];

  useEffect(() => {
    if (isOpen) {
      setRobots(robotTypes);
      setFilteredRobots(robotTypes);
      setLoading(false);
    }
  }, [isOpen]);

  useEffect(() => {
    applyFilters();
  }, [searchTerm, filters, robots]);

  const applyFilters = () => {
    let filtered = [...robots];

    // Search filter
    if (searchTerm) {
      filtered = filtered.filter(robot => 
        robot.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        robot.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Type filter
    if (filters.type !== 'all') {
      filtered = filtered.filter(robot => robot.type === filters.type);
    }

    // Price range filter
    if (filters.priceRange !== 'all') {
      const ranges = {
        'low': [0, 2000],
        'medium': [2000, 3500],
        'high': [3500, 10000]
      };
      const [min, max] = ranges[filters.priceRange];
      filtered = filtered.filter(robot => robot.basePrice >= min && robot.basePrice < max);
    }

    // Sort
    switch (filters.sortBy) {
      case 'price-asc':
        filtered.sort((a, b) => a.basePrice - b.basePrice);
        break;
      case 'price-desc':
        filtered.sort((a, b) => b.basePrice - a.basePrice);
        break;
      case 'combat':
        filtered.sort((a, b) => b.stats.combat - a.stats.combat);
        break;
      case 'speed':
        filtered.sort((a, b) => b.stats.speed - a.stats.speed);
        break;
      case 'utility':
        filtered.sort((a, b) => b.stats.utility - a.stats.utility);
        break;
      default:
        break;
    }

    setFilteredRobots(filtered);
  };

  const handlePurchase = async (robot) => {
    try {
      const response = await fetch('/api/robots/purchase', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ robot_type: robot.id })
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`✅ Successfully purchased ${robot.name}!\nCost: $${robot.basePrice}\nNew balance: $${data.new_balance}`);
        if (onPurchase) onPurchase(data);
      } else {
        alert(`❌ ${data.error || 'Purchase failed'}`);
      }
    } catch (err) {
      console.error('Error purchasing robot:', err);
      alert('Network error. Please try again.');
    }
  };

  if (!isOpen) return null;

  return (
    <div className="robot-market-overlay" onClick={onClose}>
      <div className="robot-market-container" onClick={(e) => e.stopPropagation()}>
        <Card className="robot-market-modal">
          {/* Header */}
          <div className="robot-market-header">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6 text-purple-400" />
              <h2 className="text-2xl font-bold text-white">Robot Market</h2>
            </div>
            <button className="close-btn" onClick={onClose}>×</button>
          </div>

          {/* Balance Display */}
          <div className="balance-bar">
            <div className="balance-item">
              <span className="text-gray-400">Your Balance:</span>
              <span className="text-green-400 font-bold text-lg">
                ${player?.currencies?.credits?.toLocaleString() || 0}
              </span>
            </div>
          </div>

          {/* Search & Filters */}
          <div className="market-controls">
            <div className="search-bar">
              <Search className="w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search robots..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <RobotFilters filters={filters} setFilters={setFilters} />
          </div>

          {/* Results Count */}
          <div className="results-count">
            <p className="text-gray-400 text-sm">
              Showing {filteredRobots.length} of {robots.length} robots
            </p>
          </div>

          {/* Robots Grid */}
          <div className="robots-grid">
            {loading ? (
              <div className="loading-state">
                <Loader2 className="w-12 h-12 animate-spin text-purple-400" />
                <p className="text-gray-400 mt-4">Loading robots...</p>
              </div>
            ) : filteredRobots.length === 0 ? (
              <div className="empty-state">
                <Bot className="w-16 h-16 text-gray-600 mb-4" />
                <p className="text-gray-400">No robots found matching your criteria</p>
              </div>
            ) : (
              filteredRobots.map(robot => (
                <RobotCard
                  key={robot.id}
                  robot={robot}
                  player={player}
                  onPurchase={handlePurchase}
                />
              ))
            )}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default RobotMarket;