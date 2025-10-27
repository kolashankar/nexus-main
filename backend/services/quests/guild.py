from typing import List, Dict
from datetime import datetime, timedelta
import uuid
from ...models.quests.quest import Quest
from ...models.player.player import Player


class GuildQuestService:
    """Service for managing guild quests."""

    async def get_guild_quests(self, guild_id: str) -> List[Dict]:
        """Get quests for a guild."""
        quests = await Quest.find({
            "guild_id": guild_id,
            "quest_type": "guild",
            "status": {"$in": ["available", "active"]}
        }).to_list()

        return quests

    async def create_guild_quest(
        self,
        player_id: str,
        guild_id: str,
        quest_data: Dict
    ) -> Dict:
        """Create a new guild quest."""
        # Check player permissions
        player = await Player.find_one({"_id": player_id})
        if not player or player.get("guild_id") != guild_id:
            return {"success": False, "error": "Not a member of this guild"}

        guild_rank = player.get("guild_rank")
        if guild_rank not in ["leader", "officer"]:
            return {"success": False, "error": "Insufficient permissions"}

        # Create quest
        quest_id = str(uuid.uuid4())

        quest = {
            "_id": quest_id,
            "guild_id": guild_id,
            "quest_type": "guild",
            "title": quest_data.get("title"),
            "description": quest_data.get("description"),
            "objectives": quest_data.get("objectives", []),
            "rewards": quest_data.get("rewards", {}),
            "required_members": quest_data.get("required_members", 5),
            "participants": [],
            "contributions": {},
            "status": "available",
            "generated_by": "guild_leader",
            "generated_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=7)
        }

        await Quest.insert_one(quest)

        return {"success": True, "quest_id": quest_id, "quest": quest}

    async def contribute(
        self,
        player_id: str,
        quest_id: str,
        contribution: Dict
    ) -> Dict:
        """Record player contribution to guild quest."""
        quest = await Quest.find_one({"_id": quest_id})

        if not quest:
            return {"success": False, "error": "Quest not found"}

        # Add player to participants if not already
        participants = quest.get("participants", [])
        if player_id not in participants:
            participants.append(player_id)

        # Record contribution
        contributions = quest.get("contributions", {})
        if player_id not in contributions:
            contributions[player_id] = []
        contributions[player_id].append(contribution)

        # Update quest
        await Quest.update_one(
            {"_id": quest_id},
            {
                "$set": {
                    "participants": participants,
                    "contributions": contributions
                }
            }
        )

        return {"success": True, "contribution_recorded": contribution}
