import React from 'react';
import { Card } from '@/components/ui/card';
import { Package, Bot, Wrench, Sparkles } from 'lucide-react';

const InventoryTab = ({ player }) => {
  const inventoryItems = [
    { type: 'robots', count: player?.robots_count || 0, icon: Bot, color: '#8b5cf6' },
    { type: 'chips', count: player?.chips_count || 0, icon: Wrench, color: '#3b82f6' },
    { type: 'ornaments', count: player?.ornaments_count || 0, icon: Sparkles, color: '#f59e0b' },
    { type: 'items', count: player?.items_count || 0, icon: Package, color: '#10b981' }
  ];

  return (
    <div className="tab-content-wrapper">
      <h3 className="tab-content-title">Inventory</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {inventoryItems.map(item => {
          const Icon = item.icon;
          return (
            <Card key={item.type} className="p-6 bg-black/30 border-purple-500/30 text-center">
              <div className="w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center"
                   style={{ backgroundColor: item.color + '20', border: `2px solid ${item.color}40` }}>
                <Icon className="w-8 h-8" style={{ color: item.color }} />
              </div>
              <h4 className="text-white font-bold text-lg mb-2 capitalize">{item.type}</h4>
              <p className="text-3xl font-bold" style={{ color: item.color }}>{item.count}</p>
            </Card>
          );
        })}
      </div>
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

export default InventoryTab;