import React from 'react';
import { Card } from '../ui/card';
import { X, Package, Sword, Shirt, Shield } from 'lucide-react';

/**
 * Inventory Modal Component
 */
const InventoryModal = ({ onClose, player }) => {
  // Sample inventory items
  const inventoryItems = [
    { id: 1, name: 'Energy Sword', type: 'weapon', icon: Sword, rarity: 'legendary' },
    { id: 2, name: 'Combat Armor', type: 'armor', icon: Shield, rarity: 'rare' },
    { id: 3, name: 'Casual Outfit', type: 'clothing', icon: Shirt, rarity: 'common' },
    { id: 4, name: 'Health Pack', type: 'consumable', icon: Package, rarity: 'common', quantity: 5 },
  ];

  const rarityColors = {
    legendary: 'border-yellow-500 bg-yellow-500/10',
    rare: 'border-blue-500 bg-blue-500/10',
    common: 'border-gray-500 bg-gray-500/10',
  };

  return (
    <div className="fixed inset-0 bg-black/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <Card className="bg-gray-900 border-purple-500/30 p-6 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-3xl font-bold text-white flex items-center gap-2">
            <Package className="w-8 h-8" />
            Inventory
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white transition-colors"
          >
            <X className="w-6 h-6" />
          </button>
        </div>

        {/* Inventory Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {inventoryItems.map((item) => {
            const Icon = item.icon;
            return (
              <div
                key={item.id}
                className={`p-4 rounded-lg border-2 ${rarityColors[item.rarity]} hover:scale-105 transition-transform cursor-pointer`}
              >
                <div className="flex flex-col items-center gap-2">
                  <Icon className="w-12 h-12 text-white" />
                  <h3 className="text-white font-semibold text-center text-sm">{item.name}</h3>
                  <p className="text-gray-400 text-xs capitalize">{item.type}</p>
                  {item.quantity && (
                    <span className="text-purple-400 text-xs">x{item.quantity}</span>
                  )}
                </div>
              </div>
            );
          })}
        </div>

        {/* Stats */}
        <div className="mt-6 p-4 bg-black/30 rounded-lg border border-purple-500/30">
          <h3 className="text-white font-semibold mb-2">Inventory Stats</h3>
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-400">Total Items:</span>
              <span className="text-white ml-2">{inventoryItems.reduce((sum, item) => sum + (item.quantity || 1), 0)}</span>
            </div>
            <div>
              <span className="text-gray-400">Capacity:</span>
              <span className="text-white ml-2">50</span>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default InventoryModal;
