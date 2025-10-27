from typing import List, Dict, Optional
from datetime import datetime, timedelta
import uuid
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId


class HiddenQuestService:
    """Service for managing hidden quests."""

    def __init__(self, db: AsyncIOMotorClient = None):
        self.db = db
        self.hidden_quest_locations = self._initialize_locations()

    def _initialize_locations(self) -> Dict:
        """Initialize hidden quest spawn locations."""
        return {
            "abandoned_warehouse": {
                "x": 450, "y": 780,
                "required_trait": "perception",
                "min_value": 70
            },
            "underground_tunnel": {
                "x": 230, "y": 560,
                "required_trait": "stealth",
                "min_value": 75
            },
            "rooftop_garden": {
                "x": 890, "y": 340,
                "required_trait": "curiosity",
                "min_value": 65
            },
            "secret_library": {
                "x": 120, "y": 920,
                "required_trait": "intelligence",
                "min_value": 80
            }
        }

    async def attempt_discovery(
        self,
        player_id: str,
        location: Dict
    ) -> Dict:
        """Attempt to discover a hidden quest."""
        if not self.db:
            return {"success": False, "error": "Database not initialized"}
        
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return {"success": False, "error": "Player not found"}

        player_x = location.get("x", 0)
        player_y = location.get("y", 0)

        # Check if player is near a hidden quest location
        for location_name, loc_data in self.hidden_quest_locations.items():
            distance = (
                (player_x - loc_data["x"]) ** 2 + (player_y - loc_data["y"]) ** 2) ** 0.5

            if distance < 50:  # Within 50 units
                # Check if player has required trait
                required_trait = loc_data["required_trait"]
                min_value = loc_data["min_value"]
                player_trait_value = player.get(
                    "traits", {}).get(required_trait, 0)

                if player_trait_value >= min_value:
                    # Discovery success!
                    quest = await self._generate_hidden_quest(player_id, location_name)
                    return {
                        "success": True,
                        "discovered": True,
                        "quest": quest,
                        "message": f"You discovered a hidden quest at {location_name}!"
                    }
                else:
                    return {
                        "success": True,
                        "discovered": False,
                        "message": f"You sense something here, but need more {required_trait}..."
                    }

        return {
            "success": True,
            "discovered": False,
            "message": "Nothing of interest here."
        }

    async def _generate_hidden_quest(
        self,
        player_id: str,
        location_name: str
    ) -> Dict:
        """Generate a hidden quest."""
        quest_id = str(uuid.uuid4())

        quest = {
            "_id": quest_id,
            "player_id": player_id,
            "quest_type": "hidden",
            "title": f"Secret of the {location_name.replace('_', ' ').title()}",
            "description": "A mysterious quest you've uncovered...",
            "lore": "Few know of this place and its secrets.",
            "objectives": [
                {
                    "description": "Investigate the area",
                    "type": "visit",
                    "target": location_name,
                    "current": 0,
                    "required": 1,
                    "completed": False
                },
                {
                    "description": "Solve the mystery",
                    "type": "interact",
                    "target": "mystery_object",
                    "current": 0,
                    "required": 1,
                    "completed": False
                }
            ],
            "rewards": {
                "credits": 25000,
                "xp": 2500,
                "karma": 100,
                "items": ["legendary_artifact"],
                "trait_boosts": {}
            },
            "requirements": {},
            "difficulty": "legendary",
            "status": "available",
            "generated_by": "hidden_system",
            "generated_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7)
        }

        if self.db:
            await self.db.quests.insert_one(quest)
        return quest

    async def get_hints(self, player_id: str) -> List[str]:
        """Get cryptic hints about hidden quests."""
        if not self.db:
            return []
        
        player = await self.db.players.find_one({"_id": player_id})
        if not player:
            return []

        hints = [
            "Whispers speak of an abandoned place, where rust meets concrete...",
            "Those who move unseen may find passages below the city...",
            "High above, where few dare to climb, secrets bloom in unexpected places...",
            "Knowledge seekers find treasures in forgotten halls of learning..."
        ]

        # Only show relevant hints based on player traits
        relevant_hints = []
        player_traits = player.get("traits", {})

        if player_traits.get("perception", 0) >= 60:
            relevant_hints.append(hints[0])
        if player_traits.get("stealth", 0) >= 65:
            relevant_hints.append(hints[1])
        if player_traits.get("curiosity", 0) >= 55:
            relevant_hints.append(hints[2])
        if player_traits.get("intelligence", 0) >= 70:
            relevant_hints.append(hints[3])

        return relevant_hints if relevant_hints else ["Develop your abilities to uncover secrets..."]

    async def check_discovery(
        self,
        player_id: str,
        location: str,
        action: str,
        player: Dict
    ) -> Dict:
        """Check if player discovers a hidden quest."""
        return await self.attempt_discovery(player_id, {"location": location, "action": action})

    async def get_player_hidden_quests(self, player_id: str) -> List[Dict]:
        """Get all discovered hidden quests for a player."""
        if not self.db:
            return []
        
        try:
            quests = []
            async for quest in self.db.quests.find({
                "player_id": player_id,
                "quest_type": "hidden",
                "status": {"$in": ["active", "completed"]}
            }):
                quests.append(quest)
            return quests
        except Exception:
            return []
