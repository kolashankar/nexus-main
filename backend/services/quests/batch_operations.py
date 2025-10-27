"""Quest batch operations service"""

from typing import List, Dict, Any
from datetime import datetime


class QuestBatchOperations:
    """Handles batch operations on quests"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests

    async def batch_accept_quests(
        self,
        quest_ids: List[str],
        player_id: str,
    ) -> Dict[str, Any]:
        """Accept multiple quests at once"""
        result = await self.quests.update_many(
            {
                "_id": {"$in": quest_ids},
                "status": "available",
                "$or": [
                    {"player_id": player_id},
                    {"quest_type": {"$in": ["world", "guild"]}}
                ]
            },
            {
                "$set": {
                    "status": "active",
                    "started_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
            }
        )

        return {
            "accepted": result.modified_count,
            "requested": len(quest_ids),
        }

    async def batch_abandon_quests(
        self,
        quest_ids: List[str],
        player_id: str,
    ) -> Dict[str, Any]:
        """Abandon multiple quests"""
        result = await self.quests.update_many(
            {
                "_id": {"$in": quest_ids},
                "player_id": player_id,
                "status": "active",
            },
            {
                "$set": {
                    "status": "failed",
                    "updated_at": datetime.utcnow(),
                }
            }
        )

        return {
            "abandoned": result.modified_count,
            "requested": len(quest_ids),
        }

    async def batch_delete_quests(
        self,
        quest_ids: List[str],
        player_id: str = None,
    ) -> int:
        """Delete multiple quests (admin only)"""
        query = {"_id": {"$in": quest_ids}}
        if player_id:
            query["player_id"] = player_id

        result = await self.quests.delete_many(query)
        return result.deleted_count
