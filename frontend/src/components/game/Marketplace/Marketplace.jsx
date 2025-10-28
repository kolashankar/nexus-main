import React, { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { ShoppingCart, Sparkles, TrendingUp, Coins } from 'lucide-react';
import './Marketplace.css';

const Marketplace = ({ player, isOpen, onClose, onPurchase }) => {
  const [marketInfo, setMarketInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchMarketplaceInfo();
    }
  }, [isOpen]);

  const fetchMarketplaceInfo = async () => {
    try {
      const response = await fetch('/api/marketplace/info', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      setMarketInfo(data);
    } catch (err) {
      console.error('Error fetching marketplace info:', err);
    } finally {
      setLoading(false);
    }
  };

  const purchaseOrnament = async (itemType) => {
    try {
      setPurchasing(itemType);
      const response = await fetch('/api/marketplace/purchase', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ item_type: itemType })
      });
      const data = await response.json();
      
      if (data.success) {
        alert(`Successfully purchased ${itemType}!\n` +
              `Spent: ${data.price_paid.toLocaleString()} coins\n` +
              `New balance: ${data.new_balance.toLocaleString()} coins\n` +
              `Total bonus: +${data.bonus_percentage}%`);
        
        // Refresh marketplace info
        await fetchMarketplaceInfo();
        
        // Notify parent
        if (onPurchase) {
          onPurchase(data);
        }
      } else {
        alert(data.error || 'Purchase failed');
      }
    } catch (err) {
      console.error('Error purchasing ornament:', err);
      alert('Network error. Please try again.');
    } finally {
      setPurchasing(null);
    }
  };

  if (loading || !isOpen) {
    return null;
  }

  return (
    <div className="marketplace-overlay" onClick={onClose}>
      <Card className="marketplace-modal" onClick={(e) => e.stopPropagation()}>
        <div className="marketplace-header">
          <ShoppingCart className="w-6 h-6" />
          <h2>Mystical Marketplace</h2>
          <button className="close-btn" onClick={onClose}>×</button>
        </div>

        <div className="marketplace-balance">
          <Coins className="w-5 h-5 text-yellow-400" />
          <span>Your Balance: {marketInfo?.balance?.toLocaleString() || 0} coins</span>
        </div>

        <div className="marketplace-info">
          <TrendingUp className="w-5 h-5 text-blue-400" />
          <p>Current Bonus: <strong className="text-green-400">+{marketInfo?.bonus_percentage || 0}%</strong> coins per task</p>
        </div>

        <div className="ornaments-grid">
          {/* Chain Card */}
          <Card className="ornament-card">
            <div className="ornament-icon chain-icon">
              <Sparkles className="w-8 h-8" />
            </div>
            <h3>Golden Chain</h3>
            <p className="ornament-desc">Enchanted necklace that boosts your earnings</p>
            
            <div className="ornament-stats">
              <div className="stat">
                <span className="stat-label">Bonus:</span>
                <span className="stat-value text-green-400">+3%</span>
              </div>
              <div className="stat">
                <span className="stat-label">Owned:</span>
                <span className="stat-value">{marketInfo?.ornaments?.chains || 0}</span>
              </div>
            </div>

            <div className="ornament-price">
              <Coins className="w-4 h-4" />
              <span>{marketInfo?.prices?.chain?.toLocaleString() || 0} coins</span>
            </div>

            <Button
              onClick={() => purchaseOrnament('chain')}
              disabled={!marketInfo?.can_afford?.chain || purchasing}
              className="purchase-btn"
            >
              {purchasing === 'chain' ? 'Purchasing...' : 'Purchase Chain'}
            </Button>

            {!marketInfo?.can_afford?.chain && (
              <p className="insufficient-funds">Insufficient funds</p>
            )}
          </Card>

          {/* Ring Card */}
          <Card className="ornament-card">
            <div className="ornament-icon ring-icon">
              <Sparkles className="w-8 h-8" />
            </div>
            <h3>Mystic Ring</h3>
            <p className="ornament-desc">Powerful ring that amplifies your fortune</p>
            
            <div className="ornament-stats">
              <div className="stat">
                <span className="stat-label">Bonus:</span>
                <span className="stat-value text-green-400">+7%</span>
              </div>
              <div className="stat">
                <span className="stat-label">Owned:</span>
                <span className="stat-value">{marketInfo?.ornaments?.rings || 0}</span>
              </div>
            </div>

            <div className="ornament-price">
              <Coins className="w-4 h-4" />
              <span>{marketInfo?.prices?.ring?.toLocaleString() || 0} coins</span>
            </div>

            <Button
              onClick={() => purchaseOrnament('ring')}
              disabled={!marketInfo?.can_afford?.ring || purchasing}
              className="purchase-btn"
            >
              {purchasing === 'ring' ? 'Purchasing...' : 'Purchase Ring'}
            </Button>

            {!marketInfo?.can_afford?.ring && (
              <p className="insufficient-funds">Insufficient funds</p>
            )}
          </Card>
        </div>

        <div className="marketplace-note">
          <p>💡 <strong>Tip:</strong> Each ornament you purchase doubles in price, but stacks your bonus!</p>
          <p>Example: 1st chain = 2,000 coins (+3%), 2nd chain = 4,000 coins (+6% total)</p>
        </div>
      </Card>
    </div>
  );
};

export default Marketplace;
