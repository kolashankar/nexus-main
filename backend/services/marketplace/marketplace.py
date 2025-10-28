"""Marketplace Service

Manages ornament purchases and pricing.
"""

import logging
from typing import Dict, Any
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime

logger = logging.getLogger(__name__)

class MarketplaceService:
    """Manage marketplace transactions"""
    
    # Base prices
    CHAIN_BASE_PRICE = 2000
    RING_BASE_PRICE = 5000
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.players_collection = db.players
        self.purchases_collection = db.purchases
    
    async def purchase_ornament(self, player_id: str, item_type: str) -> Dict[str, Any]:
        """Purchase a chain or ring"""
        try:
            # Validate item type
            if item_type not in ['chain', 'ring']:
                raise ValueError("Invalid item type")
            
            # Get player
            player = await self.players_collection.find_one({'_id': player_id})
            if not player:
                raise ValueError("Player not found")
            
            # Get current ornaments
            ornaments = player.get('ornaments', {'chains': 0, 'rings': 0})
            current_count = ornaments.get(f'{item_type}s', 0)
            
            # Calculate price (doubles each time)
            if item_type == 'chain':
                price = self.CHAIN_BASE_PRICE * (2 ** current_count)
            else:
                price = self.RING_BASE_PRICE * (2 ** current_count)
            
            # Check if player has enough coins
            balance = player.get('currencies', {}).get('credits', 0)
            if balance < price:
                return {
                    'success': False,
                    'error': 'Insufficient funds',
                    'required': price,
                    'balance': balance
                }
            
            # Deduct coins
            new_balance = balance - price
            
            # Add ornament
            new_count = current_count + 1
            ornaments[f'{item_type}s'] = new_count
            
            # Calculate new bonus
            bonus_percentage = (ornaments.get('chains', 0) * 3) + (ornaments.get('rings', 0) * 7)
            
            # Update player
            await self.players_collection.update_one(
                {'_id': player_id},
                {
                    '$set': {
                        'currencies.credits': new_balance,
                        'ornaments': ornaments
                    }
                }
            )
            
            # Record purchase
            await self.purchases_collection.insert_one({
                'player_id': player_id,
                'item_type': item_type,
                'price_paid': price,
                'purchase_number': new_count,
                'purchased_at': datetime.utcnow().isoformat()
            })
            
            # Calculate next price
            next_price = price * 2
            
            return {
                'success': True,
                'item_type': item_type,
                'price_paid': price,
                'new_balance': new_balance,
                'item_count': new_count,
                'next_price': next_price,
                'bonus_percentage': bonus_percentage
            }
            
        except Exception as e:
            logger.error(f"Error purchasing ornament: {e}")
            raise
    
    async def get_marketplace_info(self, player_id: str) -> Dict[str, Any]:
        """Get marketplace info for player"""
        try:
            player = await self.players_collection.find_one({'_id': player_id})
            if not player:
                raise ValueError("Player not found")
            
            ornaments = player.get('ornaments', {'chains': 0, 'rings': 0})
            chains_count = ornaments.get('chains', 0)
            rings_count = ornaments.get('rings', 0)
            
            # Calculate current prices
            chain_price = self.CHAIN_BASE_PRICE * (2 ** chains_count)
            ring_price = self.RING_BASE_PRICE * (2 ** rings_count)
            
            # Calculate bonus
            bonus_percentage = (chains_count * 3) + (rings_count * 7)
            
            balance = player.get('currencies', {}).get('credits', 0)
            
            return {
                'balance': balance,
                'ornaments': {
                    'chains': chains_count,
                    'rings': rings_count
                },
                'prices': {
                    'chain': chain_price,
                    'ring': ring_price
                },
                'bonus_percentage': bonus_percentage,
                'can_afford': {
                    'chain': balance >= chain_price,
                    'ring': balance >= ring_price
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting marketplace info: {e}")
            raise
