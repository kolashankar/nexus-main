"""Quest management service - handles quest lifecycle and operations."""

from datetime import datetime
from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class QuestManager:
    """Manages quest lifecycle and operations."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.quests = db.quests
        self.players = db.players
        self.quest_progress = db.quest_progress

    async def get_available_quests(
        self,
        player_id: str,
        quest_type: Optional[str] = None,
        player_level: Optional[int] = None,
        player_karma: Optional[int] = None,
        player_traits: Optional[Dict] = None,
        player_items: Optional[List[str]] = None
    ) -> List[Dict]:
        """Get available quests for a player."""
        try:
            # Get player data
            player = await self.players.find_one({"_id": player_id})
            if not player:
                return []

            # Build query
            query = {
                "status": "available",
                "$or": [
                    {"player_id": player_id},
                    {"player_id": None}  # World quests
                ]
            }

            if quest_type:
                query["quest_type"] = quest_type

            # Check requirements
            quests = []
            async for quest in self.quests.find(query):
                if await self._check_requirements(player, quest):
                    quests.append(quest)

            return quests

        except Exception as e:
            logger.error(f"Error getting available quests: {e}")
            return []

    async def accept_quest(self, player_id: str, quest_id: str) -> Dict:
        """Accept a quest."""
        try:
            # Get quest
            quest = await self.quests.find_one({"_id": ObjectId(quest_id)})
            if not quest:
                raise ValueError("Quest not found")

            # Check if already accepted
            existing = await self.quest_progress.find_one({
                "player_id": player_id,
                "quest_id": ObjectId(quest_id),
                "status": "active"
            })
            if existing:
                raise ValueError("Quest already accepted")

            # Create progress record
            progress = {
                "player_id": player_id,
                "quest_id": ObjectId(quest_id),
                "status": "active",
                "accepted_at": datetime.utcnow(),
                "objectives_progress": [
                    {
                        "objective_id": i,
                        "current": 0,
                        "required": obj.get("required", 1),
                        "completed": False
                    }
                    for i, obj in enumerate(quest.get("objectives", []))
                ]
            }

            result = await self.quest_progress.insert_one(progress)
            progress["_id"] = result.inserted_id

            # Update quest status
            await self.quests.update_one(
                {"_id": ObjectId(quest_id)},
                {"$set": {"status": "active"}}
            )

            return progress

        except Exception as e:
            logger.error(f"Error accepting quest: {e}")
            raise

    async def update_quest_progress(self, player_id: str, quest_id: str, objective_id: int, progress: int) -> Dict:
        """Update quest objective progress."""
        try:
            # Get progress record
            quest_progress = await self.quest_progress.find_one({
                "player_id": player_id,
                "quest_id": ObjectId(quest_id),
                "status": "active"
            })

            if not quest_progress:
                raise ValueError("Quest progress not found")

            # Update objective
            objectives = quest_progress["objectives_progress"]
            if objective_id >= len(objectives):
                raise ValueError("Invalid objective ID")

            objectives[objective_id]["current"] = min(
                progress,
                objectives[objective_id]["required"]
            )
            objectives[objective_id]["completed"] = (
                objectives[objective_id]["current"] >= objectives[objective_id]["required"]
            )

            # Update progress
            await self.quest_progress.update_one(
                {"_id": quest_progress["_id"]},
                {"$set": {"objectives_progress": objectives}}
            )

            # Check if all objectives completed
            if all(obj["completed"] for obj in objectives):
                await self._complete_quest(player_id, quest_id)

            return await self.quest_progress.find_one({"_id": quest_progress["_id"]})

        except Exception as e:
            logger.error(f"Error updating quest progress: {e}")
            raise

    async def abandon_quest(self, player_id: str, quest_id: str) -> bool:
        """Abandon a quest."""
        try:
            result = await self.quest_progress.update_one(
                {
                    "player_id": player_id,
                    "quest_id": ObjectId(quest_id),
                    "status": "active"
                },
                {
                    "$set": {
                        "status": "abandoned",
                        "abandoned_at": datetime.utcnow()
                    }
                }
            )

            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error abandoning quest: {e}")
            return False

    async def _check_requirements(self, player: Dict, quest: Dict) -> bool:
        """Check if player meets quest requirements."""
        requirements = quest.get("requirements", {})

        # Level requirement
        if "min_level" in requirements:
            if player.get("level", 1) < requirements["min_level"]:
                return False

        # Karma requirement
        if "min_karma" in requirements:
            if player.get("karma_points", 0) < requirements["min_karma"]:
                return False

        # Trait requirements
        if "required_traits" in requirements:
            player_traits = player.get("traits", {})
            for trait, min_value in requirements["required_traits"].items():
                if player_traits.get(trait, 0) < min_value:
                    return False

        return True

    async def _complete_quest(self, player_id: str, quest_id: str) -> None:
        """Complete a quest and distribute rewards."""
        try:
            # Update progress status
            await self.quest_progress.update_one(
                {
                    "player_id": player_id,
                    "quest_id": ObjectId(quest_id)
                },
                {
                    "$set": {
                        "status": "completed",
                        "completed_at": datetime.utcnow()
                    }
                }
            )

            # Get quest for rewards
            quest = await self.quests.find_one({"_id": ObjectId(quest_id)})
            if quest and "rewards" in quest:
                from .rewards import RewardDistributor
                distributor = RewardDistributor(self.db)
                await distributor.distribute_rewards(player_id, quest["rewards"])

        except Exception as e:
            logger.error(f"Error completing quest: {e}")
            raise

    async def get_player_quests(
        self,
        player_id: str,
        status: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """Get quests for a player with optional status filter."""
        try:
            query = {"player_id": player_id}
            if status:
                query["status"] = status
            
            quests = []
            async for quest in self.quest_progress.find(query).limit(limit):
                # Populate quest details
                quest_data = await self.quests.find_one({"_id": quest["quest_id"]})
                if quest_data:
                    quest_data["progress"] = quest
                    quests.append(quest_data)
            
            return quests
        except Exception as e:
            logger.error(f"Error getting player quests: {e}")
            return []

    async def get_quest(self, quest_id: str) -> Optional[Dict]:
        """Get a specific quest by ID."""
        try:
            return await self.quests.find_one({"_id": ObjectId(quest_id)})
        except Exception as e:
            logger.error(f"Error getting quest: {e}")
            return None

    async def update_objective_progress(
        self,
        player_id: str,
        quest_id: str,
        objective_id: int,
        progress: int
    ) -> Dict:
        """Update progress for a specific objective."""
        return await self.update_quest_progress(player_id, quest_id, objective_id, progress)

    async def complete_quest(self, player_id: str, quest_id: str) -> Dict:
        """Complete a quest and award rewards."""
        try:
            # Mark as complete
            await self._complete_quest(player_id, quest_id)
            
            # Get completed quest data
            quest_progress = await self.quest_progress.find_one({
                "player_id": player_id,
                "quest_id": ObjectId(quest_id),
                "status": "completed"
            })
            
            return quest_progress if quest_progress else {}
        except Exception as e:
            logger.error(f"Error completing quest: {e}")
            raise

    async def create_quest(self, player_id: str, quest_data: Dict) -> Dict:
        """Create a new quest for a player."""
        try:
            quest_data["player_id"] = player_id
            quest_data["status"] = "available"
            quest_data["created_at"] = datetime.utcnow()
            
            result = await self.quests.insert_one(quest_data)
            quest_data["_id"] = result.inserted_id
            
            return quest_data
        except Exception as e:
            logger.error(f"Error creating quest: {e}")
            raise


# Backward compatibility alias
QuestService = QuestManager
