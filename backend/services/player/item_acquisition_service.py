"""Service for managing item acquisition process."""

from typing import Optional, Dict, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.player.item_acquisition import ItemAcquisition
from backend.models.world.world_item import WorldItem
from backend.services.world.item_spawn_service import ItemSpawnService
from backend.services.world.item_discovery_service import ItemDiscoveryService
import uuid

class ItemAcquisitionService:
    """Manages player's item acquisition process."""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.spawn_service = ItemSpawnService(db)
        self.discovery_service = ItemDiscoveryService(db)
    
    async def start_acquisition(
        self,
        player_id: str,
        world_item_id: str,
        player_level: int,
        player_credits: int
    ) -> tuple[bool, str, Optional[ItemAcquisition]]:
        """Start acquiring an item."""
        
        # Check if player can acquire
        can_acquire, message = await self.discovery_service.can_player_acquire(
            world_item_id, player_id, player_level, player_credits
        )
        
        if not can_acquire:
            return False, message, None
        
        # Get item details
        item_data = await self.db.world_items.find_one({"_id": world_item_id})
        if not item_data:
            return False, "Item not found", None
        
        item = WorldItem(**item_data)
        
        # Calculate completion time based on item type
        acquisition_seconds = self.spawn_service.get_acquisition_time(item.item_type)
        completes_at = datetime.utcnow() + timedelta(seconds=acquisition_seconds)
        
        # Create acquisition record
        acquisition = ItemAcquisition(
            id=str(uuid.uuid4()),
            player_id=player_id,
            world_item_id=world_item_id,
            item_type=item.item_type,
            item_name=item.item_name,
            item_id=item.item_id,
            cost_paid=item.cost,
            status="investing",
            started_at=datetime.utcnow(),
            completes_at=completes_at,
            progress_percentage=0.0
        )
        
        # Save acquisition
        await self.db.item_acquisitions.insert_one(acquisition.model_dump(by_alias=True))
        
        # Deduct credits from player
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"currencies.credits": -item.cost}}
        )
        
        # Reserve item (mark as being acquired)
        await self.discovery_service.mark_item_claimed(world_item_id, player_id)
        
        return True, "Acquisition started", acquisition
    
    async def get_player_acquisitions(
        self,
        player_id: str,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Get all acquisitions for a player."""
        
        query = {"player_id": player_id}
        if status:
            query["status"] = status
        
        cursor = self.db.item_acquisitions.find(query).sort("started_at", -1)
        acquisitions_data = await cursor.to_list(length=None)
        
        results = []
        for acq_data in acquisitions_data:
            acquisition = ItemAcquisition(**acq_data)
            
            # Calculate progress
            if acquisition.status == "investing":
                total_time = (acquisition.completes_at - acquisition.started_at).total_seconds()
                elapsed_time = (datetime.utcnow() - acquisition.started_at).total_seconds()
                progress = min(100.0, (elapsed_time / total_time) * 100)
                
                # Update progress in database
                await self.db.item_acquisitions.update_one(
                    {"_id": acquisition.id},
                    {"$set": {"progress_percentage": progress}}
                )
                
                # Check if completed
                if datetime.utcnow() >= acquisition.completes_at:
                    await self.db.item_acquisitions.update_one(
                        {"_id": acquisition.id},
                        {"$set": {"status": "completed", "progress_percentage": 100.0}}
                    )
                    acquisition.status = "completed"
                    acquisition.progress_percentage = 100.0
                else:
                    acquisition.progress_percentage = progress
            
            # Calculate time remaining
            time_remaining = max(0, int((acquisition.completes_at - datetime.utcnow()).total_seconds()))
            
            results.append({
                "id": acquisition.id,
                "item_type": acquisition.item_type,
                "item_name": acquisition.item_name,
                "cost_paid": acquisition.cost_paid,
                "status": acquisition.status,
                "started_at": acquisition.started_at,
                "completes_at": acquisition.completes_at,
                "time_remaining": time_remaining,
                "progress_percentage": round(acquisition.progress_percentage, 2)
            })
        
        return results
    
    async def claim_acquisition(self, player_id: str, acquisition_id: str) -> tuple[bool, str]:
        """Claim a completed acquisition."""
        
        # Get acquisition
        acq_data = await self.db.item_acquisitions.find_one({
            "_id": acquisition_id,
            "player_id": player_id
        })
        
        if not acq_data:
            return False, "Acquisition not found"
        
        acquisition = ItemAcquisition(**acq_data)
        
        # Check if completed
        if acquisition.status != "completed":
            if acquisition.status == "claimed":
                return False, "Already claimed"
            elif acquisition.status == "investing":
                return False, "Acquisition not yet completed"
            else:
                return False, "Cannot claim this acquisition"
        
        # Apply item to player based on type
        success, message = await self._apply_item_to_player(player_id, acquisition)
        
        if not success:
            return False, message
        
        # Mark as claimed
        await self.db.item_acquisitions.update_one(
            {"_id": acquisition_id},
            {"$set": {"status": "claimed", "claimed_at": datetime.utcnow()}}
        )
        
        return True, f"Successfully acquired {acquisition.item_name}!"
    
    async def _apply_item_to_player(
        self,
        player_id: str,
        acquisition: ItemAcquisition
    ) -> tuple[bool, str]:
        """Apply the acquired item to player's profile."""
        
        # Get player
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return False, "Player not found"
        
        if acquisition.item_type == "skill":
            # Increase skill trait by 10 points (or configure as needed)
            skill_name = acquisition.item_name
            field_name = f"traits.{skill_name}"
            
            # Get current value
            current_value = player.get("traits", {}).get(skill_name, 50.0)
            new_value = min(100.0, current_value + 10.0)  # Cap at 100
            
            await self.db.players.update_one(
                {"_id": player_id},
                {"$set": {field_name: new_value}}
            )
            
            return True, f"Skill '{skill_name}' increased to {new_value}"
        
        elif acquisition.item_type == "superpower_tool":
            # Add to player's superpowers (assuming we have a superpowers list)
            # For now, we'll add to a simple list
            await self.db.players.update_one(
                {"_id": player_id},
                {"$addToSet": {"superpowers": acquisition.item_id}}
            )
            
            return True, f"Superpower tool '{acquisition.item_name}' acquired"
        
        elif acquisition.item_type == "meta_trait":
            # Increase meta trait by 15 points (higher bonus for rarer items)
            meta_name = acquisition.item_name
            field_name = f"meta_traits.{meta_name}"
            
            # Get current value
            current_value = player.get("meta_traits", {}).get(meta_name, 50.0)
            new_value = min(100.0, current_value + 15.0)  # Cap at 100
            
            await self.db.players.update_one(
                {"_id": player_id},
                {"$set": {field_name: new_value}}
            )
            
            return True, f"Meta trait '{meta_name}' increased to {new_value}"
        
        return False, "Unknown item type"
    
    async def cancel_acquisition(self, player_id: str, acquisition_id: str) -> tuple[bool, str]:
        """Cancel an ongoing acquisition (with penalty)."""
        
        acq_data = await self.db.item_acquisitions.find_one({
            "_id": acquisition_id,
            "player_id": player_id,
            "status": "investing"
        })
        
        if not acq_data:
            return False, "Acquisition not found or cannot be cancelled"
        
        acquisition = ItemAcquisition(**acq_data)
        
        # Refund 50% of cost (penalty for cancelling)
        refund_amount = acquisition.cost_paid // 2
        
        await self.db.players.update_one(
            {"_id": player_id},
            {"$inc": {"currencies.credits": refund_amount}}
        )
        
        # Mark as cancelled
        await self.db.item_acquisitions.update_one(
            {"_id": acquisition_id},
            {"$set": {"status": "cancelled"}}
        )
        
        # Release the world item
        await self.db.world_items.update_one(
            {"_id": acquisition.world_item_id},
            {"$set": {"status": "active", "claimed_by": None}}
        )
        
        return True, f"Acquisition cancelled. Refunded {refund_amount} credits (50% penalty)"
