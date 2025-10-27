"""Ornament shop for buying chains and rings"""

from typing import Dict, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from datetime import datetime
import uuid


class OrnamentShop:
    """Handles ornament purchases and inventory"""

    # Base prices
    BASE_PRICES = {
        "chain": 2000,
        "ring": 5000
    }

    # Bonus percentages
    BONUSES = {
        "chain": 3,  # 3% per chain
        "ring": 7    # 7% per ring
    }

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection"""
        self.db = db
        self.players_collection = db['players']
        self.ornaments_collection = db['ornament_inventory']
        self.purchases_collection = db['ornament_purchases']

    async def get_inventory(self, player_id: str) -> Dict:
        """
        Get player's ornament inventory.
        
        Args:
            player_id: Player's ID
            
        Returns:
            Inventory dictionary
        """
        inventory = await self.ornaments_collection.find_one({"player_id": player_id})
        
        if not inventory:
            # Create new inventory
            inventory = {
                "player_id": player_id,
                "chains": 0,
                "rings": 0,
                "total_bonus_percentage": 0,
                "last_updated": datetime.utcnow().isoformat()
            }
            await self.ornaments_collection.insert_one(inventory)
        
        return inventory

    async def get_current_price(self, player_id: str, item_type: str) -> int:
        """
        Calculate current price for an item based on how many player already owns.
        
        Args:
            player_id: Player's ID
            item_type: "chain" or "ring"
            
        Returns:
            Current price
        """
        inventory = await self.get_inventory(player_id)
        owned_count = inventory.get(f"{item_type}s", 0)
        
        base_price = self.BASE_PRICES[item_type]
        
        # Price doubles for each subsequent purchase
        # 1st: base_price, 2nd: base_price * 2, 3rd: base_price * 4, etc.
        current_price = base_price * (2 ** owned_count)
        
        return current_price

    async def purchase_ornament(self, player_id: str, item_type: str) -> Dict:
        """
        Purchase an ornament.
        
        Args:
            player_id: Player's ID
            item_type: "chain" or "ring"
            
        Returns:
            Purchase result dictionary
        """
        if item_type not in ["chain", "ring"]:
            return {
                "success": False,
                "error": "Invalid item type"
            }
        
        # Get current price
        current_price = await self.get_current_price(player_id, item_type)
        
        # Check if player has enough coins
        player = await self.players_collection.find_one({"player_id": player_id})
        if not player:
            return {
                "success": False,
                "error": "Player not found"
            }
        
        current_balance = player.get('currencies', {}).get('credits', 0)
        
        if current_balance < current_price:
            return {
                "success": False,
                "error": "Insufficient coins",
                "required": current_price,
                "current": current_balance
            }
        
        # Deduct coins
        await self.players_collection.update_one(
            {"player_id": player_id},
            {"$inc": {"currencies.credits": -current_price}}
        )
        
        # Add ornament to inventory
        inventory = await self.get_inventory(player_id)
        item_field = f"{item_type}s"
        new_count = inventory.get(item_field, 0) + 1
        
        # Calculate new total bonus
        chains = inventory.get('chains', 0)
        rings = inventory.get('rings', 0)
        
        if item_type == "chain":
            chains += 1
        else:
            rings += 1
        
        total_bonus = (chains * self.BONUSES['chain']) + (rings * self.BONUSES['ring'])
        
        await self.ornaments_collection.update_one(
            {"player_id": player_id},
            {
                "$set": {
                    item_field: new_count,
                    "total_bonus_percentage": total_bonus,
                    "last_updated": datetime.utcnow().isoformat()
                }
            }
        )
        
        # Record purchase
        purchase_record = {
            "purchase_id": str(uuid.uuid4()),
            "player_id": player_id,
            "item_type": item_type,
            "price_paid": current_price,
            "purchase_number": new_count,
            "purchased_at": datetime.utcnow().isoformat()
        }
        await self.purchases_collection.insert_one(purchase_record)
        
        # Get new balance
        updated_player = await self.players_collection.find_one({"player_id": player_id})
        new_balance = updated_player.get('currencies', {}).get('credits', 0)
        
        # Calculate next price
        next_price = current_price * 2
        
        return {
            "success": True,
            "item_type": item_type,
            "price_paid": current_price,
            "new_balance": new_balance,
            "item_count": new_count,
            "next_price": next_price,
            "total_bonus_percentage": total_bonus
        }

    async def get_purchase_history(self, player_id: str, limit: int = 20) -> list:
        """
        Get purchase history for a player.
        
        Args:
            player_id: Player's ID
            limit: Maximum number of records
            
        Returns:
            List of purchase records
        """
        cursor = self.purchases_collection.find(
            {"player_id": player_id}
        ).sort("purchased_at", -1).limit(limit)
        
        return await cursor.to_list(length=limit)
