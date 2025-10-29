"""Task refresh scheduler service."""

import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

logger = logging.getLogger(__name__)

class TaskRefreshScheduler:
    """Manages daily task refresh and rotation."""
    
    def __init__(self):
        self.refresh_interval = 24 * 60 * 60  # 24 hours in seconds
        self.is_running = False
    
    async def start(self, db: AsyncIOMotorDatabase):
        """Start the task refresh scheduler."""
        if self.is_running:
            logger.warning("Task refresh scheduler is already running")
            return
        
        self.is_running = True
        logger.info("✅ Task refresh scheduler started")
        
        while self.is_running:
            try:
                await self._refresh_daily_tasks(db)
                await asyncio.sleep(self.refresh_interval)
            except Exception as e:
                logger.error(f"❌ Error in task refresh scheduler: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retry
    
    async def stop(self):
        """Stop the task refresh scheduler."""
        self.is_running = False
        logger.info("🛑 Task refresh scheduler stopped")
    
    async def _refresh_daily_tasks(self, db: AsyncIOMotorDatabase):
        """Refresh daily tasks for all players."""
        logger.info("🔄 Starting daily task refresh...")
        
        # Expire old daily tasks
        result = await db.advanced_tasks.update_many(
            {
                "category": "daily",
                "status": "active",
                "created_at": {"$lt": datetime.utcnow() - timedelta(hours=24)}
            },
            {"$set": {"status": "expired"}}
        )
        
        logger.info(f"  ➡️ Expired {result.modified_count} old daily tasks")
        
        # Get all active players
        active_players = await db.players.find(
            {"last_login": {"$gte": datetime.utcnow() - timedelta(days=7)}}
        ).to_list(length=None)
        
        logger.info(f"  ➡️ Found {len(active_players)} active players")
        
        # Generate new daily tasks for each player
        tasks_generated = 0
        for player in active_players:
            try:
                await self._generate_daily_tasks_for_player(db, player)
                tasks_generated += 1
            except Exception as e:
                logger.error(f"  ❌ Failed to generate tasks for player {player.get('username')}: {e}")
        
        logger.info(f"✅ Daily task refresh complete: {tasks_generated} players received new tasks")
    
    async def _generate_daily_tasks_for_player(self, db: AsyncIOMotorDatabase, player: Dict[str, Any]):
        """Generate daily tasks for a specific player."""
        player_id = player.get("_id")
        player_level = player.get("level", 1)
        
        # Check if player already has active daily tasks
        existing_count = await db.advanced_tasks.count_documents({
            "player_id": player_id,
            "category": "daily",
            "status": "active"
        })
        
        if existing_count >= 3:
            return  # Player already has daily tasks
        
        # Generate 3 daily tasks
        from backend.services.tasks.combat_task_generator import CombatTaskGenerator
        from backend.services.tasks.economic_task_generator import EconomicTaskGenerator
        from backend.services.tasks.relationship_task_generator import RelationshipTaskGenerator
        
        generators = [
            CombatTaskGenerator(),
            EconomicTaskGenerator(),
            RelationshipTaskGenerator()
        ]
        
        player_traits = player.get("traits", {})
        player_credits = player.get("currencies", {}).get("credits", 1000)
        
        for generator in generators:
            try:
                if isinstance(generator, EconomicTaskGenerator):
                    task = generator.generate_economic_task(player_level, player_credits, player_traits)
                else:
                    task = generator.generate_relationship_task(player_level, player_traits) if isinstance(generator, RelationshipTaskGenerator) else generator.generate_combat_task(player_level, player_traits)
                
                # Add daily task metadata
                task["player_id"] = player_id
                task["category"] = "daily"
                task["status"] = "active"
                task["created_at"] = datetime.utcnow()
                task["expires_at"] = datetime.utcnow() + timedelta(hours=24)
                
                await db.advanced_tasks.insert_one(task)
            except Exception as e:
                logger.error(f"    ❌ Failed to generate task: {e}")
    
    async def get_daily_tasks(self, db: AsyncIOMotorDatabase, player_id: str) -> List[Dict[str, Any]]:
        """Get player's active daily tasks."""
        tasks = await db.advanced_tasks.find({
            "player_id": player_id,
            "category": "daily",
            "status": "active"
        }).to_list(length=None)
        
        return tasks
    
    async def get_time_until_refresh(self, db: AsyncIOMotorDatabase, player_id: str) -> int:
        """Get seconds until next daily task refresh."""
        # Find the oldest daily task
        oldest_task = await db.advanced_tasks.find_one(
            {
                "player_id": player_id,
                "category": "daily",
                "status": "active"
            },
            sort=[("created_at", 1)]
        )
        
        if not oldest_task:
            return 0  # No tasks, can refresh now
        
        created_at = oldest_task.get("created_at")
        next_refresh = created_at + timedelta(hours=24)
        time_remaining = (next_refresh - datetime.utcnow()).total_seconds()
        
        return max(0, int(time_remaining))
