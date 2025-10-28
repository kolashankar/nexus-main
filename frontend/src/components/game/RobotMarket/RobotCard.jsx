import React from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Bot, Zap, Sword, Wrench, ShoppingCart } from 'lucide-react';

/**
 * RobotCard Component
 * Individual robot display card in marketplace
 */
const RobotCard = ({ robot, player, onPurchase }) => {
  const canAfford = (player?.currencies?.credits || 0) >= robot.basePrice;

  const getTypeIcon = () => {
    switch (robot.type) {
      case 'combat': return <Sword className="w-4 h-4" />;
      case 'utility': return <Wrench className="w-4 h-4" />;
      case 'economy': return <Zap className="w-4 h-4" />;
      case 'support': return <Bot className="w-4 h-4" />;
      case 'special': return <Zap className="w-4 h-4" />;
      default: return <Bot className="w-4 h-4" />;
    }
  };

  const getTypeColor = () => {
    switch (robot.type) {
      case 'combat': return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'utility': return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      case 'economy': return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'support': return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'special': return 'bg-purple-500/20 text-purple-400 border-purple-500/30';
      default: return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
    }
  };

  return (
    <Card className="robot-card-item" style={{ borderColor: robot.color + '40' }}>
      {/* Header */}
      <div className="robot-card-header" style={{ background: `linear-gradient(135deg, ${robot.color}20, transparent)` }}>
        <div className="robot-icon" style={{ backgroundColor: robot.color + '20' }}>
          <span className="text-4xl">{robot.icon}</span>
        </div>
        <div className={`robot-type-badge ${getTypeColor()}`}>
          {getTypeIcon()}
          <span className="text-xs uppercase font-semibold">{robot.type}</span>
        </div>
      </div>

      {/* Name & Description */}
      <div className="robot-card-body">
        <h3 className="robot-card-title" style={{ color: robot.color }}>
          {robot.name}
        </h3>
        <p className="robot-card-description">{robot.description}</p>

        {/* Stats */}
        <div className="robot-stats-grid">
          <div className="stat-item">
            <span className="stat-label">Speed</span>
            <div className="stat-bar-container">
              <div 
                className="stat-bar" 
                style={{ 
                  width: `${robot.stats.speed}%`,
                  backgroundColor: robot.color 
                }}
              />
            </div>
            <span className="stat-value">{robot.stats.speed}</span>
          </div>

          <div className="stat-item">
            <span className="stat-label">Combat</span>
            <div className="stat-bar-container">
              <div 
                className="stat-bar" 
                style={{ 
                  width: `${robot.stats.combat}%`,
                  backgroundColor: robot.color 
                }}
              />
            </div>
            <span className="stat-value">{robot.stats.combat}</span>
          </div>

          <div className="stat-item">
            <span className="stat-label">Utility</span>
            <div className="stat-bar-container">
              <div 
                className="stat-bar" 
                style={{ 
                  width: `${robot.stats.utility}%`,
                  backgroundColor: robot.color 
                }}
              />
            </div>
            <span className="stat-value">{robot.stats.utility}</span>
          </div>
        </div>

        {/* Abilities */}
        <div className="robot-abilities">
          <h4 className="abilities-title">Abilities:</h4>
          <ul className="abilities-list">
            {robot.abilities.map((ability, index) => (
              <li key={index} className="ability-item">
                <span className="ability-bullet" style={{ backgroundColor: robot.color }}>•</span>
                {ability}
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Footer */}
      <div className="robot-card-footer">
        <div className="robot-price">
          <span className="price-label">Price:</span>
          <span className="price-value" style={{ color: robot.color }}>
            ${robot.basePrice.toLocaleString()}
          </span>
        </div>
        <Button
          onClick={() => onPurchase(robot)}
          disabled={!canAfford}
          className={`purchase-btn ${canAfford ? 'can-afford' : 'cannot-afford'}`}
          style={canAfford ? {
            background: `linear-gradient(135deg, ${robot.color}, ${robot.color}CC)`,
            borderColor: robot.color
          } : {}}
        >
          <ShoppingCart className="w-4 h-4" />
          {canAfford ? 'Purchase' : 'Not Enough Credits'}
        </Button>
      </div>

      <style jsx>{`
        .robot-card-item {
          background: rgba(26, 26, 46, 0.95);
          border: 2px solid;
          border-radius: 16px;
          overflow: hidden;
          transition: all 0.3s ease;
          display: flex;
          flex-direction: column;
        }

        .robot-card-item:hover {
          transform: translateY(-4px);
          box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
        }

        .robot-card-header {
          padding: 20px;
          display: flex;
          align-items: flex-start;
          justify-content: space-between;
          gap: 12px;
        }

        .robot-icon {
          width: 64px;
          height: 64px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          border: 2px solid rgba(255, 255, 255, 0.1);
        }

        .robot-type-badge {
          display: flex;
          align-items: center;
          gap: 6px;
          padding: 6px 12px;
          border-radius: 20px;
          border: 1px solid;
          font-weight: 600;
        }

        .robot-card-body {
          padding: 0 20px 20px;
          flex: 1;
        }

        .robot-card-title {
          font-size: 20px;
          font-weight: bold;
          margin-bottom: 8px;
        }

        .robot-card-description {
          color: #9ca3af;
          font-size: 14px;
          margin-bottom: 16px;
          line-height: 1.5;
        }

        .robot-stats-grid {
          display: flex;
          flex-direction: column;
          gap: 12px;
          margin-bottom: 16px;
        }

        .stat-item {
          display: grid;
          grid-template-columns: 60px 1fr 40px;
          align-items: center;
          gap: 8px;
        }

        .stat-label {
          font-size: 12px;
          color: #9ca3af;
          font-weight: 600;
        }

        .stat-bar-container {
          height: 6px;
          background: rgba(255, 255, 255, 0.1);
          border-radius: 3px;
          overflow: hidden;
        }

        .stat-bar {
          height: 100%;
          border-radius: 3px;
          transition: width 0.3s ease;
        }

        .stat-value {
          font-size: 12px;
          color: #fff;
          font-weight: 700;
          text-align: right;
        }

        .robot-abilities {
          background: rgba(0, 0, 0, 0.3);
          border-radius: 8px;
          padding: 12px;
        }

        .abilities-title {
          font-size: 12px;
          color: #9ca3af;
          font-weight: 600;
          margin-bottom: 8px;
        }

        .abilities-list {
          list-style: none;
          padding: 0;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 6px;
        }

        .ability-item {
          font-size: 12px;
          color: #d1d5db;
          display: flex;
          align-items: flex-start;
          gap: 8px;
          line-height: 1.4;
        }

        .ability-bullet {
          flex-shrink: 0;
          width: 6px;
          height: 6px;
          border-radius: 50%;
          margin-top: 5px;
        }

        .robot-card-footer {
          padding: 16px 20px;
          border-top: 1px solid rgba(139, 92, 246, 0.2);
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
        }

        .robot-price {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .price-label {
          font-size: 12px;
          color: #9ca3af;
        }

        .price-value {
          font-size: 20px;
          font-weight: bold;
        }

        .purchase-btn {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 10px 20px;
          border-radius: 8px;
          font-weight: 600;
          transition: all 0.2s;
          border: 2px solid;
          font-size: 14px;
        }

        .purchase-btn.can-afford:hover {
          transform: scale(1.05);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        }

        .purchase-btn.cannot-afford {
          background: rgba(107, 114, 128, 0.2);
          border-color: rgba(107, 114, 128, 0.4);
          color: #9ca3af;
          cursor: not-allowed;
        }
      `}</style>
    </Card>
  );
};

export default RobotCard;