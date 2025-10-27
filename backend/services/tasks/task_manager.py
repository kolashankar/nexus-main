"""Task lifecycle management"""

from typing import Dict, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid


class TaskManager:
    """Manages task lifecycle, storage, and completion"""

    def __init__(self, db: AsyncIOMotorDatabase):
        """Initialize with database connection"""
        self.db = db
        self.tasks_collection = db['tasks']

    async def save_task(self, task: Dict) -> Dict:
        """
        Save a new task to the database.
        
        Args:
            task: Task dictionary
            
        Returns:
            Saved task
        """
        await self.tasks_collection.insert_one(task)
        return task

    async def get_current_task(self, player_id: str) -> Optional[Dict]:
        """
        Get the current active task for a player.
        
        Args:
            player_id: Player's ID
            
        Returns:
            Task dictionary or None
        """
        task = await self.tasks_collection.find_one({
            "player_id": player_id,
            "status": "active"
        })
        
        if task:
            # Check if task expired
            expires_at = datetime.fromisoformat(task['expires_at'])
            if datetime.utcnow() > expires_at:
                # Mark as expired
                await self.expire_task(task['task_id'])
                return None
        
        return task

    async def complete_task(self, task_id: str, actual_reward: int) -> bool:
        """
        Mark a task as completed and update rewards.
        
        Args:
            task_id: Task ID
            actual_reward: Final reward with bonuses applied
            
        Returns:
            True if successful
        """
        result = await self.tasks_collection.update_one(
            {"task_id": task_id},
            {
                "$set": {
                    "status": "completed",
                    "completed_at": datetime.utcnow().isoformat(),
                    "actual_reward": actual_reward
                }
            }
        )
        return result.modified_count > 0

    async def expire_task(self, task_id: str) -> bool:
        """
        Mark a task as expired.
        
        Args:
            task_id: Task ID
            
        Returns:
            True if successful
        """
        result = await self.tasks_collection.update_one(
            {"task_id": task_id},
            {"$set": {"status": "expired"}}
        )
        return result.modified_count > 0

    async def get_task_history(self, player_id: str, limit: int = 10) -> list:
        """
        Get task history for a player.
        
        Args:
            player_id: Player's ID
            limit: Maximum number of tasks to return
            
        Returns:
            List of tasks
        """
        cursor = self.tasks_collection.find(
            {"player_id": player_id}
        ).sort("created_at", -1).limit(limit)
        
        return await cursor.to_list(length=limit)
