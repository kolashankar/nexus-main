import React from 'react';
import { Filter } from 'lucide-react';

/**
 * RobotFilters Component
 * Filtering and sorting controls for robot marketplace
 */
const RobotFilters = ({ filters, setFilters }) => {
  const updateFilter = (key, value) => {
    setFilters(prev => ({ ...prev, [key]: value }));
  };

  return (
    <div className="robot-filters">
      <div className="filter-icon">
        <Filter className="w-5 h-5 text-purple-400" />
      </div>

      {/* Type Filter */}
      <select
        value={filters.type}
        onChange={(e) => updateFilter('type', e.target.value)}
        className="filter-select"
      >
        <option value="all">All Types</option>
        <option value="combat">Combat</option>
        <option value="utility">Utility</option>
        <option value="economy">Economy</option>
        <option value="support">Support</option>
        <option value="special">Special</option>
      </select>

      {/* Price Range Filter */}
      <select
        value={filters.priceRange}
        onChange={(e) => updateFilter('priceRange', e.target.value)}
        className="filter-select"
      >
        <option value="all">All Prices</option>
        <option value="low">Under $2,000</option>
        <option value="medium">$2,000 - $3,500</option>
        <option value="high">Over $3,500</option>
      </select>

      {/* Sort By */}
      <select
        value={filters.sortBy}
        onChange={(e) => updateFilter('sortBy', e.target.value)}
        className="filter-select"
      >
        <option value="price-asc">Price: Low to High</option>
        <option value="price-desc">Price: High to Low</option>
        <option value="combat">Highest Combat</option>
        <option value="speed">Highest Speed</option>
        <option value="utility">Highest Utility</option>
      </select>

      <style jsx>{`
        .robot-filters {
          display: flex;
          align-items: center;
          gap: 12px;
          flex-wrap: wrap;
        }

        .filter-icon {
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .filter-select {
          background: rgba(0, 0, 0, 0.3);
          border: 1px solid rgba(139, 92, 246, 0.3);
          border-radius: 8px;
          padding: 10px 14px;
          color: white;
          font-size: 14px;
          cursor: pointer;
          transition: all 0.2s;
          outline: none;
          min-width: 160px;
        }

        .filter-select:hover {
          border-color: rgba(139, 92, 246, 0.5);
          background: rgba(0, 0, 0, 0.5);
        }

        .filter-select:focus {
          border-color: rgba(139, 92, 246, 0.8);
          box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        }

        .filter-select option {
          background: #1a1a2e;
          color: white;
          padding: 8px;
        }

        @media (max-width: 768px) {
          .robot-filters {
            width: 100%;
            flex-direction: column;
          }

          .filter-select {
            width: 100%;
          }
        }
      `}</style>
    </div>
  );
};

export default RobotFilters;