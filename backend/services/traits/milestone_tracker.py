"""Milestone tracking service."""

from datetime import datetime
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

class MilestoneTracker:
    """Tracks trait milestones for players."""
    
    MILESTONE_THRESHOLDS = [25, 50, 75, 100]
    
    async def check_milestones(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        old_traits: Dict[str, float],
        new_traits: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        """Check if any milestones were reached."""
        milestones_reached = []
        
        for trait, new_value in new_traits.items():
            old_value = old_traits.get(trait, 0)
            
            # Check each threshold
            for threshold in self.MILESTONE_THRESHOLDS:
                if old_value < threshold <= new_value:
                    milestone = await self._create_milestone(
                        db, player_id, trait, threshold, new_value
                    )
                    milestones_reached.append(milestone)
        
        return milestones_reached
    
    async def _create_milestone(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        trait: str,
        threshold: int,
        current_value: float
    ) -> Dict[str, Any]:
        """Create a milestone record."""
        # Calculate rewards
        rewards = self._calculate_milestone_rewards(trait, threshold)
        
        milestone = {
            "player_id": player_id,
            "trait": trait,
            "threshold": threshold,
            "value_at_milestone": current_value,
            "reached_at": datetime.utcnow(),
            "rewards": rewards,
            "acknowledged": False
        }
        
        # Save milestone
        await db.trait_milestones.insert_one(milestone)
        
        # Apply rewards
        await self._apply_milestone_rewards(db, player_id, rewards)
        
        logger.info(f"🎉 Milestone reached: {player_id} - {trait} level {threshold}")
        
        return milestone
    
    def _calculate_milestone_rewards(self, trait: str, threshold: int) -> Dict[str, Any]:
        """Calculate rewards for reaching a milestone."""
        base_xp = threshold * 2
        base_credits = threshold * 5
        
        rewards = {
            "xp": base_xp,
            "credits": base_credits,
            "karma": threshold // 10
        }
        
        # Special unlocks at major milestones
        if threshold == 50:
            rewards["unlocks"] = [f"{trait}_intermediate_ability"]
        elif threshold == 75:
            rewards["unlocks"] = [f"{trait}_advanced_ability"]
        elif threshold == 100:
            rewards["unlocks"] = [f"{trait}_master_ability", f"{trait}_title"]
        else:
            rewards["unlocks"] = []
        
        return rewards
    
    async def _apply_milestone_rewards(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        rewards: Dict[str, Any]
    ):
        """Apply milestone rewards to player."""
        update_data = {}
        
        if rewards.get("xp", 0) > 0:
            update_data["$inc"] = update_data.get("$inc", {})
            update_data["$inc"]["xp"] = rewards["xp"]
        
        if rewards.get("credits", 0) > 0:
            update_data["$inc"] = update_data.get("$inc", {})
            update_data["$inc"]["currencies.credits"] = rewards["credits"]
        
        if rewards.get("karma", 0) != 0:
            update_data["$inc"] = update_data.get("$inc", {})
            update_data["$inc"]["karma_points"] = rewards["karma"]
        
        # Add unlocks to player's unlocked abilities
        if rewards.get("unlocks"):
            update_data["$addToSet"] = update_data.get("$addToSet", {})
            update_data["$addToSet"]["unlocked_abilities"] = {
                "$each": rewards["unlocks"]
            }
        
        if update_data:
            await db.players.update_one(
                {"_id": player_id},
                update_data
            )
    
    async def get_player_milestones(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str,
        acknowledged_only: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all milestones for a player."""
        query = {"player_id": player_id}
        if acknowledged_only:
            query["acknowledged"] = False
        
        milestones = await db.trait_milestones.find(query).sort(
            "reached_at", -1
        ).to_list(length=None)
        
        return milestones
    
    async def acknowledge_milestone(
        self,
        db: AsyncIOMotorDatabase,
        milestone_id: str
    ):
        """Mark a milestone as acknowledged by player."""
        await db.trait_milestones.update_one(
            {"_id": milestone_id},
            {"$set": {"acknowledged": True}}
        )
    
    async def get_milestone_stats(
        self,
        db: AsyncIOMotorDatabase,
        player_id: str
    ) -> Dict[str, Any]:
        """Get milestone statistics for a player."""
        milestones = await self.get_player_milestones(db, player_id)
        
        stats = {
            "total_milestones": len(milestones),
            "by_threshold": {25: 0, 50: 0, 75: 0, 100: 0},
            "by_trait": {},
            "recent_milestones": milestones[:5],
            "unacknowledged_count": len([m for m in milestones if not m.get("acknowledged")])
        }
        
        for milestone in milestones:
            threshold = milestone.get("threshold")
            trait = milestone.get("trait")
            
            if threshold in stats["by_threshold"]:
                stats["by_threshold"][threshold] += 1
            
            if trait:
                stats["by_trait"][trait] = stats["by_trait"].get(trait, 0) + 1
        
        return stats
