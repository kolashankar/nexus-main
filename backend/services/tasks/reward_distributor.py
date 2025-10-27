"""Reward distribution with ornament bonuses"""

from typing import Dict
from motor.motor_asyncio import AsyncIOMotorDatabase


class RewardDistributor:
    """Handles coin distribution with ornament bonuses"""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection"""
        self.db = db
        self.players_collection = db['players']
        self.ornaments_collection = db['ornament_inventory']

    async def calculate_reward(self, player_id: str, base_reward: int) -> Dict:
        """
        Calculate final reward with ornament bonuses.
        
        Args:
            player_id: Player's ID
            base_reward: Base coin reward
            
        Returns:
            Dictionary with reward breakdown
        """
        # Get player's ornament inventory
        ornaments = await self.ornaments_collection.find_one({"player_id": player_id})
        
        if not ornaments:
            return {
                "base_reward": base_reward,
                "bonus_percentage": 0,
                "bonus_amount": 0,
                "total_reward": base_reward
            }
        
        # Calculate total bonus percentage
        chains = ornaments.get('chains', 0)
        rings = ornaments.get('rings', 0)
        
        # Each chain gives 3%, each ring gives 7%
        total_bonus_percentage = (chains * 3) + (rings * 7)
        
        # Calculate bonus amount
        bonus_amount = int(base_reward * (total_bonus_percentage / 100))
        total_reward = base_reward + bonus_amount
        
        return {
            "base_reward": base_reward,
            "bonus_percentage": total_bonus_percentage,
            "bonus_amount": bonus_amount,
            "total_reward": total_reward,
            "chains": chains,
            "rings": rings
        }

    async def distribute_reward(self, player_id: str, amount: int) -> bool:
        """
        Add coins to player's balance.
        
        Args:
            player_id: Player's ID
            amount: Coin amount to add
            
        Returns:
            True if successful
        """
        result = await self.players_collection.update_one(
            {"player_id": player_id},
            {"$inc": {"currencies.credits": amount}}
        )
        
        return result.modified_count > 0
