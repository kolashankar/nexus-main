"""Background task for spawning world items periodically."""

import asyncio
import random
from motor.motor_asyncio import AsyncIOMotorClient
from backend.services.world.item_spawn_service import ItemSpawnService
import os

class WorldItemSpawnerTask:
    """Background task that spawns items periodically."""
    
    def __init__(self):
        # Get MongoDB connection
        mongo_url = os.getenv("MONGO_URL", "mongodb://localhost:27017")
        self.client = AsyncIOMotorClient(mongo_url)
        self.db = self.client.karma_nexus
        self.spawn_service = ItemSpawnService(self.db)
        self.running = False
    
    async def start(self):
        """Start the spawner task."""
        self.running = True
        print("[WorldItemSpawner] Starting...")
        
        # Run all spawners concurrently
        await asyncio.gather(
            self._spawn_skills(),
            self._spawn_superpower_tools(),
            self._spawn_meta_traits(),
            self._cleanup_expired()
        )
    
    async def stop(self):
        """Stop the spawner task."""
        self.running = False
        print("[WorldItemSpawner] Stopping...")
    
    async def _spawn_skills(self):
        """Spawn skills every 2-5 minutes."""
        while self.running:
            try:
                # Random interval between 2-5 minutes
                interval = random.randint(120, 300)
                await asyncio.sleep(interval)
                
                if not self.running:
                    break
                
                item = await self.spawn_service.spawn_random_item("skill")
                if item:
                    print(f"[WorldItemSpawner] Spawned skill: {item.item_name} at {item.position.model_dump()}")
            
            except Exception as e:
                print(f"[WorldItemSpawner] Error spawning skill: {e}")
                await asyncio.sleep(30)  # Wait before retrying
    
    async def _spawn_superpower_tools(self):
        """Spawn superpower tools every 10-15 minutes."""
        while self.running:
            try:
                # Random interval between 10-15 minutes
                interval = random.randint(600, 900)
                await asyncio.sleep(interval)
                
                if not self.running:
                    break
                
                item = await self.spawn_service.spawn_random_item("superpower_tool")
                if item:
                    print(f"[WorldItemSpawner] Spawned superpower tool: {item.item_name} at {item.position.model_dump()}")
            
            except Exception as e:
                print(f"[WorldItemSpawner] Error spawning superpower tool: {e}")
                await asyncio.sleep(30)
    
    async def _spawn_meta_traits(self):
        """Spawn meta traits every 30-60 minutes."""
        while self.running:
            try:
                # Random interval between 30-60 minutes
                interval = random.randint(1800, 3600)
                await asyncio.sleep(interval)
                
                if not self.running:
                    break
                
                item = await self.spawn_service.spawn_random_item("meta_trait")
                if item:
                    print(f"[WorldItemSpawner] Spawned meta trait: {item.item_name} at {item.position.model_dump()}")
            
            except Exception as e:
                print(f"[WorldItemSpawner] Error spawning meta trait: {e}")
                await asyncio.sleep(30)
    
    async def _cleanup_expired(self):
        """Clean up expired items every 5 minutes."""
        while self.running:
            try:
                await asyncio.sleep(300)  # 5 minutes
                
                if not self.running:
                    break
                
                count = await self.spawn_service.cleanup_expired_items()
                if count > 0:
                    print(f"[WorldItemSpawner] Cleaned up {count} expired items")
            
            except Exception as e:
                print(f"[WorldItemSpawner] Error cleaning up: {e}")
                await asyncio.sleep(30)

# Global instance
_spawner_task = None

async def start_spawner():
    """Start the world item spawner."""
    global _spawner_task
    if _spawner_task is None:
        _spawner_task = WorldItemSpawnerTask()
        asyncio.create_task(_spawner_task.start())

async def stop_spawner():
    """Stop the world item spawner."""
    global _spawner_task
    if _spawner_task:
        await _spawner_task.stop()
        _spawner_task = None
