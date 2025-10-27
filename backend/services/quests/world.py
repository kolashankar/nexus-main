from typing import List, Dict
from datetime import datetime
from ...models.quests.quest import Quest


class WorldQuestService:
    """Service for managing world quests."""

    async def get_world_quests(self) -> List[Dict]:
        """Get active world quests (available to all players)."""
        quests = await Quest.find({
            "quest_type": "world",
            "status": "available",
            "$or": [
                {"expires_at": None},
                {"expires_at": {"$gt": datetime.utcnow()}}
            ]
        }).to_list()

        return quests

    async def participate(self, player_id: str, quest_id: str) -> Dict:
        """Register player for world quest participation."""
        quest = await Quest.find_one({"_id": quest_id})

        if not quest:
            return {"success": False, "error": "Quest not found"}

        # Add player to participants
        participants = quest.get("participants", [])
        if player_id not in participants:
            participants.append(player_id)
            await Quest.update_one(
                {"_id": quest_id},
                {"$set": {"participants": participants}}
            )

        return {"success": True, "quest_id": quest_id}
