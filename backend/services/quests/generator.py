"""Quest generator service - Creates quests using AI (Oracle)"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import uuid
import random

from ...models.quests.quest import QuestType
from ...models.quests.objective import ObjectiveType
from ..ai.oracle.oracle import Oracle


class QuestGenerator:
    """Generates quests using AI and templates"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players
        self.oracle = Oracle()

    async def generate_personal_quest(
        self,
        player_id: str,
        player: Dict[str, Any],
        quest_type: str = "personal",
    ) -> Dict[str, Any]:
        """Generate personalized quest using Oracle AI"""
        # Use Oracle to generate quest
        generated_quest = await self.oracle.generate_quest_for_player(player, quest_type)
        
        # Convert to dict
        quest_data = generated_quest.model_dump() if hasattr(generated_quest, 'model_dump') else generated_quest

        # Add metadata
        quest_data["_id"] = str(uuid.uuid4())
        quest_data["player_id"] = player_id
        quest_data["quest_type"] = quest_type
        quest_data["status"] = "available"
        quest_data["generated_by"] = "oracle"
        quest_data["generated_at"] = datetime.utcnow()
        quest_data["created_at"] = datetime.utcnow()
        quest_data["updated_at"] = datetime.utcnow()

        # Set expiry (personal quests expire in 7 days)
        quest_data["expires_at"] = datetime.utcnow() + timedelta(days=7)

        # Insert quest
        await self.quests.insert_one(quest_data)

        return quest_data

    async def generate_daily_quests(
        self,
        player_id: str,
        player: Dict[str, Any],
        count: int = 3,
    ) -> List[Dict[str, Any]]:
        """Generate daily quests"""
        quests = []

        for i in range(count):
            # Use simpler template-based generation for daily quests
            quest = self._generate_simple_quest(
                player_id=player_id,
                player=player,
                quest_type=QuestType.DAILY,
                difficulty="easy",
            )

            # Set expiry (daily quests expire at end of day)
            tomorrow = datetime.utcnow().replace(hour=0, minute=0, second=0,
                                       microsecond=0) + timedelta(days=1)
            quest["expires_at"] = tomorrow

            await self.quests.insert_one(quest)
            quests.append(quest)

        return quests

    async def generate_weekly_quests(
        self,
        player_id: str,
        player: Dict[str, Any],
        count: int = 5,
    ) -> List[Dict[str, Any]]:
        """Generate weekly quests"""
        quests = []

        for i in range(count):
            # Weekly quests are harder
            quest = self._generate_simple_quest(
                player_id=player_id,
                player=player,
                quest_type=QuestType.WEEKLY,
                difficulty="medium",
            )

            # Set expiry (weekly quests expire in 7 days)
            quest["expires_at"] = datetime.utcnow() + timedelta(days=7)

            await self.quests.insert_one(quest)
            quests.append(quest)

        return quests

    def _generate_simple_quest(
        self,
        player_id: str,
        player: Dict[str, Any],
        quest_type: QuestType,
        difficulty: str = "medium",
    ) -> Dict[str, Any]:
        """Generate simple quest from templates"""
        quest_id = str(uuid.uuid4())
        player_level = player.get("level", 1)

        # Choose objective types based on player's strong traits
        traits = player.get("traits", {})
        possible_objectives = []

        if traits.get("hacking", 0) > 50:
            possible_objectives.append(ObjectiveType.HACK)
        if traits.get("kindness", 0) > 50:
            possible_objectives.append(ObjectiveType.HELP)
        if traits.get("trading", 0) > 50:
            possible_objectives.append(ObjectiveType.TRADE)

        # Default objectives
        if not possible_objectives:
            possible_objectives = [
                ObjectiveType.EARN_KARMA, ObjectiveType.WIN_COMBAT]

        # Select random objective
        obj_type = random.choice(possible_objectives)

        # Generate objective based on type
        objective = self._create_objective(obj_type, difficulty, player_level)

        # Generate quest title and description
        titles = {
            ObjectiveType.HACK: "System Breach",
            ObjectiveType.HELP: "Good Samaritan",
            ObjectiveType.TRADE: "Merchant's Deal",
            ObjectiveType.EARN_KARMA: "Path to Enlightenment",
            ObjectiveType.WIN_COMBAT: "Warrior's Challenge",
        }

        descriptions = {
            ObjectiveType.HACK: "Demonstrate your hacking prowess.",
            ObjectiveType.HELP: "Help others and earn good karma.",
            ObjectiveType.TRADE: "Trade with other players.",
            ObjectiveType.EARN_KARMA: "Earn karma through your actions.",
            ObjectiveType.WIN_COMBAT: "Prove yourself in combat.",
        }

        # Calculate rewards based on difficulty
        rewards = self._calculate_rewards(difficulty, player_level, obj_type)

        return {
            "_id": quest_id,
            "quest_type": quest_type.value,
            "title": titles.get(obj_type, "Quest"),
            "description": descriptions.get(obj_type, "Complete this quest."),
            "lore": None,
            "player_id": player_id,
            "guild_id": None,
            "generated_by": "system",
            "generated_at": datetime.utcnow(),
            "seed": None,
            "status": "available",
            "objectives": [objective],
            "rewards": rewards,
            "requirements": {
                "min_level": 1,
                "min_karma": None,
                "max_karma": None,
                "required_traits": {},
                "required_items": [],
                "required_quests": [],
            },
            "story_data": None,
            "expires_at": None,  # Will be set by caller
            "started_at": None,
            "completed_at": None,
            "completion_time": None,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

    def _create_objective(
        self,
        obj_type: ObjectiveType,
        difficulty: str,
        player_level: int,
    ) -> Dict[str, Any]:
        """Create objective based on type and difficulty"""
        # Calculate required amount based on difficulty
        amounts = {
            "easy": {ObjectiveType.HACK: 3, ObjectiveType.HELP: 2, ObjectiveType.TRADE: 2, ObjectiveType.EARN_KARMA: 50, ObjectiveType.WIN_COMBAT: 2},
            "medium": {ObjectiveType.HACK: 5, ObjectiveType.HELP: 5, ObjectiveType.TRADE: 5, ObjectiveType.EARN_KARMA: 100, ObjectiveType.WIN_COMBAT: 5},
            "hard": {ObjectiveType.HACK: 10, ObjectiveType.HELP: 10, ObjectiveType.TRADE: 10, ObjectiveType.EARN_KARMA: 200, ObjectiveType.WIN_COMBAT: 10},
        }

        required = amounts.get(difficulty, amounts["medium"]).get(obj_type, 5)

        descriptions = {
            ObjectiveType.HACK: f"Successfully hack {required} systems",
            ObjectiveType.HELP: f"Help {required} players",
            ObjectiveType.TRADE: f"Complete {required} trades",
            ObjectiveType.EARN_KARMA: f"Earn {required} karma points",
            ObjectiveType.WIN_COMBAT: f"Win {required} combats",
        }

        return {
            "objective_id": str(uuid.uuid4()),
            "description": descriptions.get(obj_type, f"Complete {required} tasks"),
            "type": obj_type.value,
            "target": obj_type.value,
            "current": 0,
            "required": required,
            "completed": False,
        }

    def _calculate_rewards(
        self,
        difficulty: str,
        player_level: int,
        obj_type: ObjectiveType,
    ) -> Dict[str, Any]:
        """Calculate quest rewards"""
        # Base rewards by difficulty
        base = {
            "easy": {"credits": 100, "xp": 50, "karma": 10},
            "medium": {"credits": 300, "xp": 150, "karma": 25},
            "hard": {"credits": 600, "xp": 400, "karma": 50},
        }

        rewards = base.get(difficulty, base["medium"])

        # Scale by player level
        level_multiplier = 1 + (player_level * 0.1)
        rewards["credits"] = int(rewards["credits"] * level_multiplier)
        rewards["xp"] = int(rewards["xp"] * level_multiplier)

        return {
            "credits": rewards["credits"],
            "xp": rewards["xp"],
            "karma": rewards["karma"],
            "karma_tokens": 0,
            "items": [],
            "trait_boosts": {},
            "special": None,
        }
