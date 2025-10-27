"""Hidden quest discovery service."""

from datetime import datetime
from typing import Dict, List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
import random
import logging

logger = logging.getLogger(__name__)

class HiddenQuestDiscoverer:
    """Manages hidden quest discovery mechanics."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.quests = db.quests
        self.players = db.players
        self.quest_progress = db.quest_progress

    async def check_discovery_triggers(self, player_id: str, action_data: Dict) -> Optional[Dict]:
        """Check if player action triggers hidden quest discovery."""
        try:
            # Get player data
            player = await self.players.find_one({"_id": player_id})
            if not player:
                return None

            # Get undiscovered hidden quests
            discovered_ids = await self._get_discovered_quest_ids(player_id)

            hidden_quests = await self.quests.find({
                "quest_type": "hidden",
                "_id": {"$nin": discovered_ids}
            }).to_list(None)

            # Check each quest for discovery
            for quest in hidden_quests:
                if await self._check_discovery_conditions(player, quest, action_data):
                    # Quest discovered!
                    discovered = await self._discover_quest(player_id, quest)
                    return discovered

            return None

        except Exception as e:
            logger.error(f"Error checking discovery triggers: {e}")
            return None

    async def _get_discovered_quest_ids(self, player_id: str) -> List[str]:
        """Get list of already discovered hidden quest IDs."""
        try:
            discovered = await self.quest_progress.find({
                "player_id": player_id,
                "quest_type": "hidden"
            }).to_list(None)

            return [str(q["quest_id"]) for q in discovered]

        except Exception as e:
            logger.error(f"Error getting discovered quests: {e}")
            return []

    async def _check_discovery_conditions(self, player: Dict, quest: Dict, action_data: Dict) -> bool:
        """Check if discovery conditions are met."""
        discovery = quest.get("discovery_conditions", {})

        # Location-based discovery
        if "location" in discovery:
            required_location = discovery["location"]
            player_location = player.get("location", {})

            if not self._is_at_location(player_location, required_location):
                return False

        # Action-based discovery
        if "action_type" in discovery:
            if action_data.get("type") != discovery["action_type"]:
                return False

        # Trait-based discovery
        if "required_traits" in discovery:
            player_traits = player.get("traits", {})
            for trait, min_value in discovery["required_traits"].items():
                if player_traits.get(trait, 0) < min_value:
                    return False

        # Time-based discovery
        if "time_window" in discovery:
            current_hour = datetime.utcnow().hour
            time_window = discovery["time_window"]

            if not (time_window["start"] <= current_hour <= time_window["end"]):
                return False

        # Karma-based discovery
        if "karma_range" in discovery:
            karma = player.get("karma_points", 0)
            karma_range = discovery["karma_range"]

            if not (karma_range["min"] <= karma <= karma_range["max"]):
                return False

        # Random chance
        if "discovery_chance" in discovery:
            chance = discovery["discovery_chance"]
            if random.random() > chance:
                return False

        return True

    def _is_at_location(self, player_location: Dict, required_location: Dict) -> bool:
        """Check if player is at required location."""
        # Check territory
        if "territory_id" in required_location:
            if player_location.get("territory_id") != required_location["territory_id"]:
                return False

        # Check coordinates (within radius)
        if "coordinates" in required_location:
            coords = required_location["coordinates"]
            radius = required_location.get("radius", 10)

            player_x = player_location.get("x", 0)
            player_y = player_location.get("y", 0)

            distance = ((player_x - coords["x"]) **
                        2 + (player_y - coords["y"]) ** 2) ** 0.5

            if distance > radius:
                return False

        return True

    async def _discover_quest(self, player_id: str, quest: Dict) -> Dict:
        """Mark quest as discovered for player."""
        try:
            # Create progress record
            progress = {
                "player_id": player_id,
                "quest_id": quest["_id"],
                "quest_type": "hidden",
                "status": "available",
                "discovered_at": datetime.utcnow(),
                "objectives_progress": []
            }

            await self.quest_progress.insert_one(progress)

            # Update quest status
            await self.quests.update_one(
                {"_id": quest["_id"]},
                {
                    "$set": {"status": "available"},
                    "$inc": {"discovery_count": 1}
                }
            )

            return {
                "quest_id": str(quest["_id"]),
                "title": quest.get("title"),
                "description": quest.get("description"),
                "discovered_at": progress["discovered_at"]
            }

        except Exception as e:
            logger.error(f"Error discovering quest: {e}")
            raise

    async def get_discovered_hidden_quests(self, player_id: str) -> List[Dict]:
        """Get all hidden quests discovered by player."""
        try:
            discovered = await self.quest_progress.find({
                "player_id": player_id,
                "quest_type": "hidden"
            }).to_list(None)

            quests = []
            for progress in discovered:
                quest = await self.quests.find_one({"_id": progress["quest_id"]})
                if quest:
                    quest["discovered_at"] = progress["discovered_at"]
                    quest["status"] = progress["status"]
                    quests.append(quest)

            return quests

        except Exception as e:
            logger.error(f"Error getting discovered hidden quests: {e}")
            return []

    async def get_hidden_quest_hints(self, player_id: str) -> List[Dict]:
        """Get cryptic hints for undiscovered hidden quests."""
        try:
            # Get undiscovered hidden quests
            discovered_ids = await self._get_discovered_quest_ids(player_id)

            hidden_quests = await self.quests.find({
                "quest_type": "hidden",
                "_id": {"$nin": discovered_ids}
            }).limit(3).to_list(None)

            hints = []
            for quest in hidden_quests:
                hint = {
                    "hint": quest.get("hint", "A mysterious quest awaits..."),
                    "difficulty": quest.get("difficulty", "unknown"),
                    "category": quest.get("category", "mystery")
                }
                hints.append(hint)

            return hints

        except Exception as e:
            logger.error(f"Error getting hints: {e}")
            return []
