"""Player inventory management service."""

from typing import Dict, Any, List, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId


class InventoryManager:
    """Manage player inventory operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize inventory manager.
        
        Args:
            db: MongoDB database instance
        """
        self.db = db
        self.players = db.players

    async def add_item(
        self,
        player_id: str,
        item_id: str,
        quantity: int = 1,
        item_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Add item to player inventory.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            quantity: Quantity to add
            item_data: Optional item metadata
            
        Returns:
            Updated inventory item
        """
        player = await self.players.find_one({'_id': ObjectId(player_id)})
        if not player:
            raise ValueError(f'Player {player_id} not found')

        inventory = player.get('items', [])

        # Check if item already exists
        existing_item = None
        for item in inventory:
            if item['item_id'] == item_id:
                existing_item = item
                break

        if existing_item:
            # Update quantity
            await self.players.update_one(
                {'_id': ObjectId(player_id), 'items.item_id': item_id},
                {'$inc': {'items.$.quantity': quantity}}
            )
            existing_item['quantity'] += quantity
            return existing_item
        else:
            # Add new item
            new_item = {
                'item_id': item_id,
                'quantity': quantity,
                'equipped': False,
                'acquired_at': datetime.utcnow(),
                **(item_data or {})
            }

            await self.players.update_one(
                {'_id': ObjectId(player_id)},
                {'$push': {'items': new_item}}
            )

            return new_item

    async def remove_item(
        self,
        player_id: str,
        item_id: str,
        quantity: int = 1
    ) -> bool:
        """Remove item from player inventory.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            quantity: Quantity to remove
            
        Returns:
            True if item was removed
        """
        player = await self.players.find_one({'_id': ObjectId(player_id)})
        if not player:
            raise ValueError(f'Player {player_id} not found')

        inventory = player.get('items', [])

        for item in inventory:
            if item['item_id'] == item_id:
                if item['quantity'] <= quantity:
                    # Remove entire item
                    await self.players.update_one(
                        {'_id': ObjectId(player_id)},
                        {'$pull': {'items': {'item_id': item_id}}}
                    )
                else:
                    # Decrease quantity
                    await self.players.update_one(
                        {'_id': ObjectId(player_id), 'items.item_id': item_id},
                        {'$inc': {'items.$.quantity': -quantity}}
                    )
                return True

        return False

    async def equip_item(self, player_id: str, item_id: str) -> bool:
        """Equip an item.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            
        Returns:
            True if item was equipped
        """
        result = await self.players.update_one(
            {'_id': ObjectId(player_id), 'items.item_id': item_id},
            {'$set': {'items.$.equipped': True}}
        )

        return result.modified_count > 0

    async def unequip_item(self, player_id: str, item_id: str) -> bool:
        """Unequip an item.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            
        Returns:
            True if item was unequipped
        """
        result = await self.players.update_one(
            {'_id': ObjectId(player_id), 'items.item_id': item_id},
            {'$set': {'items.$.equipped': False}}
        )

        return result.modified_count > 0

    async def get_inventory(self, player_id: str) -> List[Dict[str, Any]]:
        """Get player's full inventory.
        
        Args:
            player_id: Player ID
            
        Returns:
            List of inventory items
        """
        player = await self.players.find_one(
            {'_id': ObjectId(player_id)},
            {'items': 1}
        )

        return player.get('items', []) if player else []

    async def get_equipped_items(self, player_id: str) -> List[Dict[str, Any]]:
        """Get player's equipped items.
        
        Args:
            player_id: Player ID
            
        Returns:
            List of equipped items
        """
        inventory = await self.get_inventory(player_id)
        return [item for item in inventory if item.get('equipped', False)]

    async def has_item(self, player_id: str, item_id: str, quantity: int = 1) -> bool:
        """Check if player has specific item.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            quantity: Required quantity
            
        Returns:
            True if player has the item in required quantity
        """
        player = await self.players.find_one(
            {
                '_id': ObjectId(player_id),
                'items': {
                    '$elemMatch': {
                        'item_id': item_id,
                        'quantity': {'$gte': quantity}
                    }
                }
            }
        )

        return player is not None

    async def get_item_count(self, player_id: str, item_id: str) -> int:
        """Get count of specific item in inventory.
        
        Args:
            player_id: Player ID
            item_id: Item identifier
            
        Returns:
            Item quantity
        """
        inventory = await self.get_inventory(player_id)

        for item in inventory:
            if item['item_id'] == item_id:
                return item.get('quantity', 0)

        return 0
