"""Task Manager Service

Manages task lifecycle, completion, and rewards.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorDatabase
import uuid

logger = logging.getLogger(__name__)

class TaskManager:
    """Manage player tasks"""
    
    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.tasks_collection = db.tasks
        self.players_collection = db.players
    
    async def create_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new task"""
        try:
            task_data['_id'] = str(uuid.uuid4())
            task_data['created_at'] = datetime.utcnow().isoformat()
            
            result = await self.tasks_collection.insert_one(task_data)
            return task_data
        except Exception as e:
            logger.error(f"Error creating task: {e}")
            raise
    
    async def get_current_task(self, player_id: str) -> Optional[Dict[str, Any]]:
        """Get player's current active task"""
        try:
            task = await self.tasks_collection.find_one({
                'player_id': player_id,
                'status': 'active'
            })
            return task
        except Exception as e:
            logger.error(f"Error getting current task: {e}")
            return None
    
    async def complete_task(self, task_id: str, player_id: str) -> Dict[str, Any]:
        """Complete a task and distribute rewards"""
        try:
            # Get task
            task = await self.tasks_collection.find_one({'_id': task_id, 'player_id': player_id})
            if not task:
                raise ValueError("Task not found")
            
            if task['status'] != 'active':
                raise ValueError("Task is not active")
            
            # Get player
            player = await self.players_collection.find_one({'_id': player_id})
            if not player:
                raise ValueError("Player not found")
            
            # Calculate reward with bonuses
            base_reward = task.get('coin_reward', 100)
            bonus_percentage = await self._calculate_bonus_percentage(player)
            actual_reward = int(base_reward * (1 + bonus_percentage / 100))
            
            # Update player coins
            new_balance = player.get('currencies', {}).get('credits', 0) + actual_reward
            await self.players_collection.update_one(
                {'_id': player_id},
                {'$set': {'currencies.credits': new_balance}}
            )
            
            # Mark task as completed
            await self.tasks_collection.update_one(
                {'_id': task_id},
                {
                    '$set': {
                        'status': 'completed',
                        'completed_at': datetime.utcnow().isoformat(),
                        'actual_reward': actual_reward
                    }
                }
            )
            
            return {
                'success': True,
                'base_reward': base_reward,
                'bonus_percentage': bonus_percentage,
                'actual_reward': actual_reward,
                'new_balance': new_balance
            }
            
        except Exception as e:
            logger.error(f"Error completing task: {e}")
            raise
    
    async def _calculate_bonus_percentage(self, player: Dict[str, Any]) -> float:
        """Calculate bonus percentage from ornaments"""
        ornaments = player.get('ornaments', {})
        chains = ornaments.get('chains', 0)
        rings = ornaments.get('rings', 0)
        
        # Each chain: +3%, Each ring: +7%
        bonus = (chains * 3) + (rings * 7)
        return bonus
    
    async def expire_old_tasks(self) -> int:
        """Expire tasks past their expiration time"""
        try:
            result = await self.tasks_collection.update_many(
                {
                    'status': 'active',
                    'expires_at': {'$lt': datetime.utcnow().isoformat()}
                },
                {'$set': {'status': 'expired'}}
            )
            return result.modified_count
        except Exception as e:
            logger.error(f"Error expiring tasks: {e}")
            return 0
