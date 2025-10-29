import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../../ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Activity } from 'lucide-react';
import { apiClient } from '../../../services/api/client';

const TraitEvolutionChart = ({ traitName }) => {
  const [evolutionData, setEvolutionData] = useState(null);
  const [selectedTrait, setSelectedTrait] = useState(traitName || 'kindness');
  const [loading, setLoading] = useState(false);
  const [days, setDays] = useState(30);

  useEffect(() => {
    if (selectedTrait) {
      loadEvolution();
    }
  }, [selectedTrait, days]);

  const loadEvolution = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/api/tasks/analytics/traits/evolution', {
        params: {
          trait_name: selectedTrait,
          days: days
        }
      });
      if (response.data.success) {
        setEvolutionData(response.data.evolution);
      }
    } catch (error) {
      console.error('Error loading trait evolution:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatChartData = () => {
    if (!evolutionData || !evolutionData.data_points) return [];
    
    return evolutionData.data_points.map(point => ({
      date: new Date(point.timestamp).toLocaleDateString(),
      value: point.value
    }));
  };

  const getTrendColor = (trend) => {
    if (trend === 'increasing') return 'text-green-400';
    if (trend === 'decreasing') return 'text-red-400';
    return 'text-gray-400';
  };

  const getTrendIcon = (trend) => {
    if (trend === 'increasing') return '↑';
    if (trend === 'decreasing') return '↓';
    return '→';
  };

  // Common traits for selection
  const commonTraits = [
    'kindness', 'courage', 'wisdom', 'strength', 'intelligence',
    'compassion', 'cunning', 'loyalty', 'greed', 'honesty'
  ];

  return (
    <div className="space-y-4">
      {/* Trait Selector */}
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-sm text-gray-400">Select Trait:</span>
        {commonTraits.map((trait) => (
          <button
            key={trait}
            onClick={() => setSelectedTrait(trait)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-all ${
              selectedTrait === trait
                ? 'bg-blue-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            {trait.charAt(0).toUpperCase() + trait.slice(1)}
          </button>
        ))}
      </div>

      {/* Period Selector */}
      <div className="flex items-center gap-2">
        <span className="text-sm text-gray-400">Period:</span>
        {[7, 14, 30, 90].map((period) => (
          <button
            key={period}
            onClick={() => setDays(period)}
            className={`px-3 py-1 rounded-lg text-sm font-medium transition-all ${
              days === period
                ? 'bg-purple-600 text-white'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
            }`}
          >
            {period} days
          </button>
        ))}
      </div>

      {/* Chart Card */}
      <Card className="bg-gray-900 border-gray-700">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Activity className="w-5 h-5" />
            {selectedTrait ? `${selectedTrait.charAt(0).toUpperCase() + selectedTrait.slice(1)} Evolution` : 'Trait Evolution'}
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading ? (
            <div className="text-center py-12">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
              <p className="text-gray-400 mt-4">Loading evolution data...</p>
            </div>
          ) : evolutionData && evolutionData.data_points && evolutionData.data_points.length > 0 ? (
            <>
              {/* Summary */}
              {evolutionData.summary && (
                <div className="grid grid-cols-4 gap-4 mb-6">
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <p className="text-xs text-gray-400">Start Value</p>
                    <p className="text-2xl font-bold text-white">{evolutionData.summary.start_value}</p>
                  </div>
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <p className="text-xs text-gray-400">Current Value</p>
                    <p className="text-2xl font-bold text-white">{evolutionData.summary.end_value}</p>
                  </div>
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <p className="text-xs text-gray-400">Total Change</p>
                    <p className={`text-2xl font-bold ${
                      evolutionData.summary.total_change > 0 ? 'text-green-400' : 'text-red-400'
                    }`}>
                      {evolutionData.summary.total_change > 0 ? '+' : ''}{evolutionData.summary.total_change}
                    </p>
                  </div>
                  <div className="bg-gray-800 p-4 rounded-lg">
                    <p className="text-xs text-gray-400">Trend</p>
                    <p className={`text-2xl font-bold flex items-center gap-1 ${getTrendColor(evolutionData.summary.trend)}`}>
                      <span>{getTrendIcon(evolutionData.summary.trend)}</span>
                      <span className="capitalize">{evolutionData.summary.trend}</span>
                    </p>
                  </div>
                </div>
              )}

              {/* Chart */}
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={formatChartData()}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis 
                    dataKey="date" 
                    stroke="#9CA3AF"
                    style={{ fontSize: '12px' }}
                  />
                  <YAxis 
                    stroke="#9CA3AF"
                    domain={[0, 100]}
                    style={{ fontSize: '12px' }}
                  />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                    labelStyle={{ color: '#F3F4F6' }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="value" 
                    stroke="#3B82F6" 
                    strokeWidth={3}
                    dot={{ fill: '#3B82F6', r: 4 }}
                    activeDot={{ r: 6 }}
                    name={selectedTrait.charAt(0).toUpperCase() + selectedTrait.slice(1)}
                  />
                </LineChart>
              </ResponsiveContainer>
            </>
          ) : (
            <div className="text-center py-12">
              <Activity className="w-16 h-16 text-gray-600 mx-auto mb-4" />
              <p className="text-gray-400">No evolution data available</p>
              <p className="text-gray-500 text-sm">Complete more tasks to see trait changes</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TraitEvolutionChart;
