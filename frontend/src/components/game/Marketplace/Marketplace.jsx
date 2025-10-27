/**
 * Marketplace - Shop for ornaments (chains and rings)
 */
import React, { useState, useEffect } from 'react';
import './Marketplace.css';

const BACKEND_URL = import.meta.env.REACT_APP_BACKEND_URL || process.env.REACT_APP_BACKEND_URL;

const Marketplace = ({ player, isOpen, onClose, onPurchase }) => {
  const [inventory, setInventory] = useState(null);
  const [prices, setPrices] = useState(null);
  const [loading, setLoading] = useState(false);
  const [purchasing, setPurchasing] = useState(null);
  const [error, setError] = useState(null);
  const [coinBalance, setCoinBalance] = useState(player?.currencies?.credits || 0);

  useEffect(() => {
    if (isOpen) {
      fetchMarketplaceData();
    }
  }, [isOpen]);

  useEffect(() => {
    if (player?.currencies?.credits !== undefined) {
      setCoinBalance(player.currencies.credits);
    }
  }, [player]);

  const fetchMarketplaceData = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('token');

      // Fetch inventory and prices in parallel
      const [inventoryRes, pricesRes] = await Promise.all([
        fetch(`${BACKEND_URL}/api/marketplace/inventory`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }),
        fetch(`${BACKEND_URL}/api/marketplace/prices`, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
      ]);

      if (!inventoryRes.ok || !pricesRes.ok) {
        throw new Error('Failed to fetch marketplace data');
      }

      const inventoryData = await inventoryRes.json();
      const pricesData = await pricesRes.json();

      setInventory(inventoryData.inventory);
      setPrices(pricesData.prices);
    } catch (err) {
      console.error('Error fetching marketplace data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async (itemType) => {
    try {
      setPurchasing(itemType);
      setError(null);

      const token = localStorage.getItem('token');
      const response = await fetch(`${BACKEND_URL}/api/marketplace/purchase`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ item_type: itemType })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Purchase failed');
      }

      if (data.success) {
        // Update local state
        setCoinBalance(data.new_balance);
        
        // Show success message
        alert(`${itemType.charAt(0).toUpperCase() + itemType.slice(1)} purchased!\n\nPrice: ${data.price_paid} coins\nNew Balance: ${data.new_balance} coins\nTotal Bonus: +${data.total_bonus_percentage}%\nNext ${itemType} will cost: ${data.next_price} coins`);

        // Refresh marketplace data
        await fetchMarketplaceData();

        // Notify parent component
        if (onPurchase) {
          onPurchase(data);
        }
      }
    } catch (err) {
      console.error('Error purchasing ornament:', err);
      setError(err.message);
    } finally {
      setPurchasing(null);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="marketplace-overlay" onClick={onClose}>
      <div className="marketplace-modal" onClick={(e) => e.stopPropagation()}>
        <div className="marketplace-header">
          <h2>🏪 ORNAMENT MARKETPLACE</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>

        {loading ? (
          <div className="marketplace-loading">
            <div className="spinner"></div>
            <p>Loading marketplace...</p>
          </div>
        ) : (
          <div className="marketplace-content">
            {error && (
              <div className="marketplace-error">
                <p>{error}</p>
              </div>
            )}

            {/* Player Stats */}
            <div className="player-stats">
              <div className="stat-item">
                <span className="stat-icon">💰</span>
                <span className="stat-label">Coins:</span>
                <span className="stat-value">{coinBalance.toLocaleString()}</span>
              </div>
              {inventory && (
                <div className="stat-item">
                  <span className="stat-icon">✨</span>
                  <span className="stat-label">Total Bonus:</span>
                  <span className="stat-value bonus-highlight">+{inventory.total_bonus_percentage}%</span>
                </div>
              )}
            </div>

            {/* Ornaments Grid */}
            <div className="ornaments-grid">
              {/* Chain Card */}
              <div className="ornament-card">
                <div className="ornament-image chain-image">
                  <span className="ornament-emoji">🔗</span>
                </div>
                <div className="ornament-info">
                  <h3>Golden Chain</h3>
                  <p className="ornament-description">
                    A mystical chain that enhances your earning power
                  </p>
                  <div className="ornament-bonus">
                    <span className="bonus-label">Bonus:</span>
                    <span className="bonus-value">+3% coins per task</span>
                  </div>
                  <div className="ornament-owned">
                    <span>Owned: {inventory?.chains || 0}</span>
                  </div>
                  <div className="ornament-price">
                    <span className="price-icon">💰</span>
                    <span className="price-value">{prices?.chain?.toLocaleString() || 'Loading...'}</span>
                  </div>
                  <button
                    className="purchase-button"
                    onClick={() => handlePurchase('chain')}
                    disabled={purchasing || !prices || coinBalance < prices?.chain}
                  >
                    {purchasing === 'chain' ? 'Purchasing...' : 'Purchase'}
                  </button>
                  {prices && coinBalance < prices.chain && (
                    <p className="insufficient-funds">Insufficient coins</p>
                  )}
                </div>
              </div>

              {/* Ring Card */}
              <div className="ornament-card">
                <div className="ornament-image ring-image">
                  <span className="ornament-emoji">💍</span>
                </div>
                <div className="ornament-info">
                  <h3>Diamond Ring</h3>
                  <p className="ornament-description">
                    A powerful ring that greatly boosts your rewards
                  </p>
                  <div className="ornament-bonus">
                    <span className="bonus-label">Bonus:</span>
                    <span className="bonus-value">+7% coins per task</span>
                  </div>
                  <div className="ornament-owned">
                    <span>Owned: {inventory?.rings || 0}</span>
                  </div>
                  <div className="ornament-price">
                    <span className="price-icon">💰</span>
                    <span className="price-value">{prices?.ring?.toLocaleString() || 'Loading...'}</span>
                  </div>
                  <button
                    className="purchase-button"
                    onClick={() => handlePurchase('ring')}
                    disabled={purchasing || !prices || coinBalance < prices?.ring}
                  >
                    {purchasing === 'ring' ? 'Purchasing...' : 'Purchase'}
                  </button>
                  {prices && coinBalance < prices.ring && (
                    <p className="insufficient-funds">Insufficient coins</p>
                  )}
                </div>
              </div>
            </div>

            {/* Info Section */}
            <div className="marketplace-info">
              <h4>ℹ️ How It Works</h4>
              <ul>
                <li>Each chain adds <strong>+3%</strong> to your task rewards</li>
                <li>Each ring adds <strong>+7%</strong> to your task rewards</li>
                <li>Bonuses stack! (e.g., 2 chains + 1 ring = +13%)</li>
                <li>Prices double with each purchase (e.g., 2nd chain costs 4,000 coins)</li>
                <li>Ornaments are visible on your character in the game</li>
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Marketplace;
