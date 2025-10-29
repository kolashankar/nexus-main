"""Task cooldown manager service."""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.models.tasks.task_types import TaskType
import logging

logger = logging.getLogger(__name__)

class CooldownManager:
    """Manages task type cooldowns to prevent grinding."""
    
    # Cooldown durations by task type (in hours)
    COOLDOWN_DURATIONS = {
        TaskType.COMBAT: 2,
        TaskType.ECONOMIC: 4,
        TaskType.RELATIONSHIP: 3,
        TaskType.GUILD: 6,
        TaskType.ETHICAL_DILEMMA: 8,
        TaskType.MORAL_CHOICE: 1,
        TaskType.EXPLORATION: 2,
        TaskType.SKILL_BASED: 3,
        TaskType.SOCIAL: 2
    }
    
    # Max completions before cooldown kicks in
    MAX_COMPLETIONS = {
        TaskType.COMBAT: 5,
        TaskType.ECONOMIC: 3,
        TaskType.RELATIONSHIP: 4,
        TaskType.GUILD: 2,
        TaskType.ETHICAL_DILEMMA: 2,
        TaskType.MORAL_CHOICE: 10,
        TaskType.EXPLORATION: 8,
        TaskType.SKILL_BASED: 6,
        TaskType.SOCIAL: 5
    }
    
    async def check_cooldown(self, db: AsyncIOMotorDatabase, player_id: str, task_type: str) -> Dict[str, Any]:
        """Check if a task type is on cooldown for a player."""
        try:
            task_type_enum = TaskType(task_type)
        except ValueError:
            return {"on_cooldown": False, "can_attempt": True}
        
        # Find cooldown record
        cooldown = await db.task_cooldowns.find_one({
            "player_id": player_id,
            "task_type": task_type
        })
        
        if not cooldown:
            return {
                "on_cooldown": False,
                "can_attempt": True,
                "remaining_attempts": self.MAX_COMPLETIONS.get(task_type_enum, 3)
            }
        
        # Check if cooldown has expired
        now = datetime.utcnow()
        cooldown_ends = cooldown.get("cooldown_ends_at")
        
        if cooldown_ends and now < cooldown_ends:
            # Still on cooldown
            seconds_remaining = (cooldown_ends - now).total_seconds()
            return {
                "on_cooldown": True,
                "can_attempt": False,
                "seconds_remaining": int(seconds_remaining),
                "cooldown_ends_at": cooldown_ends.isoformat()
            }
        
        # Cooldown expired, reset
        await self._reset_cooldown(db, player_id, task_type)
        
        return {
            "on_cooldown": False,
            "can_attempt": True,
            "remaining_attempts": self.MAX_COMPLETIONS.get(task_type_enum, 3)
        }
    
    async def record_task_completion(self, db: AsyncIOMotorDatabase, player_id: str, task_type: str):
        """Record a task completion and update cooldown if needed."""
        try:
            task_type_enum = TaskType(task_type)
        except ValueError:
            return
        
        max_completions = self.MAX_COMPLETIONS.get(task_type_enum, 3)
        cooldown_hours = self.COOLDOWN_DURATIONS.get(task_type_enum, 2)
        
        # Find or create cooldown record
        cooldown = await db.task_cooldowns.find_one({
            "player_id": player_id,
            "task_type": task_type
        })
        
        now = datetime.utcnow()
        
        if not cooldown:
            # First completion
            await db.task_cooldowns.insert_one({
                "player_id": player_id,
                "task_type": task_type,
                "last_completed_at": now,
                "completed_count": 1,
                "max_completions": max_completions,
                "cooldown_ends_at": None  # No cooldown yet
            })
            logger.info(f"  ➡️ First {task_type} completion for player {player_id}")
            return
        
        # Check if we need to reset cooldown period
        cooldown_ends = cooldown.get("cooldown_ends_at")
        if cooldown_ends and now >= cooldown_ends:
            # Reset the counter
            await self._reset_cooldown(db, player_id, task_type)
            cooldown = await db.task_cooldowns.find_one({
                "player_id": player_id,
                "task_type": task_type
            })
        
        # Increment completion count
        completed_count = cooldown.get("completed_count", 0) + 1
        
        update_data = {
            "last_completed_at": now,
            "completed_count": completed_count
        }
        
        # Check if we've hit the max
        if completed_count >= max_completions:
            cooldown_ends_at = now + timedelta(hours=cooldown_hours)
            update_data["cooldown_ends_at"] = cooldown_ends_at
            logger.info(f"  ⏰ {task_type} cooldown activated for player {player_id} (expires in {cooldown_hours}h)")
        
        await db.task_cooldowns.update_one(
            {"player_id": player_id, "task_type": task_type},
            {"$set": update_data}
        )
    
    async def _reset_cooldown(self, db: AsyncIOMotorDatabase, player_id: str, task_type: str):
        """Reset cooldown counter for a task type."""
        try:
            task_type_enum = TaskType(task_type)
            max_completions = self.MAX_COMPLETIONS.get(task_type_enum, 3)
        except ValueError:
            max_completions = 3
        
        await db.task_cooldowns.update_one(
            {"player_id": player_id, "task_type": task_type},
            {
                "$set": {
                    "completed_count": 0,
                    "cooldown_ends_at": None,
                    "max_completions": max_completions
                }
            },
            upsert=True
        )
    
    async def get_all_cooldowns(self, db: AsyncIOMotorDatabase, player_id: str) -> Dict[str, Dict[str, Any]]:
        """Get all active cooldowns for a player."""
        cooldowns = await db.task_cooldowns.find({"player_id": player_id}).to_list(length=None)
        
        result = {}
        now = datetime.utcnow()
        
        for cooldown in cooldowns:
            task_type = cooldown.get("task_type")
            cooldown_ends = cooldown.get("cooldown_ends_at")
            completed_count = cooldown.get("completed_count", 0)
            max_completions = cooldown.get("max_completions", 3)
            
            if cooldown_ends and now < cooldown_ends:
                seconds_remaining = (cooldown_ends - now).total_seconds()
                result[task_type] = {
                    "on_cooldown": True,
                    "seconds_remaining": int(seconds_remaining),
                    "cooldown_ends_at": cooldown_ends.isoformat()
                }
            else:
                result[task_type] = {
                    "on_cooldown": False,
                    "completed_count": completed_count,
                    "remaining_attempts": max(0, max_completions - completed_count)
                }
        
        return result
