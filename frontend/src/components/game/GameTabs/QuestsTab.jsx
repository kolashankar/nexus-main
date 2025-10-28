import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Target, Clock, Coins, CheckCircle, Loader2 } from 'lucide-react';

const QuestsTab = ({ player }) => {
  const [quests, setQuests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuests();
  }, []);

  const fetchQuests = async () => {
    try {
      const response = await fetch('/api/quests/active', {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      const data = await response.json();
      setQuests(data.quests || []);
    } catch (err) {
      console.error('Error fetching quests:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="tab-content-wrapper">
      <h3 className="tab-content-title">Active Quests</h3>
      {loading ? (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="w-12 h-12 animate-spin text-purple-400" />
        </div>
      ) : quests.length === 0 ? (
        <Card className="p-12 text-center bg-black/20 border-purple-500/20">
          <Target className="w-16 h-16 text-gray-600 mx-auto mb-4" />
          <p className="text-gray-400">No active quests</p>
        </Card>
      ) : (
        <div className="grid gap-4">
          {quests.map(quest => (
            <Card key={quest._id} className="p-6 bg-black/30 border-purple-500/30">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h4 className="text-xl font-bold text-white mb-2">{quest.title}</h4>
                  <p className="text-gray-400">{quest.description}</p>
                </div>
                <span className="px-3 py-1 bg-purple-500/20 text-purple-300 rounded-lg text-sm">
                  {quest.difficulty || 'Medium'}
                </span>
              </div>
              <div className="flex items-center gap-6 text-sm">
                <div className="flex items-center gap-2 text-yellow-400">
                  <Coins className="w-4 h-4" />
                  <span>{quest.reward || 100} coins</span>
                </div>
                <div className="flex items-center gap-2 text-blue-400">
                  <Clock className="w-4 h-4" />
                  <span>{quest.timeLimit || 'No limit'}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
      <style jsx>{`
        .tab-content-wrapper { padding: 0; }
        .tab-content-title {
          font-size: 24px;
          font-weight: bold;
          color: white;
          margin-bottom: 24px;
        }
      `}</style>
    </div>
  );
};

export default QuestsTab;