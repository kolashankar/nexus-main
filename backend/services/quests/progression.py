"""Quest progression tracking service."""

from typing import Dict, List
from motor.motor_asyncio import AsyncIOMotorClient
import logging

logger = logging.getLogger(__name__)

class QuestProgressionTracker:
    """Tracks and manages quest progression."""

    def __init__(self, db: AsyncIOMotorClient):
        self.db = db
        self.quest_progress = db.quest_progress
        self.quests = db.quests
        self.actions = db.actions

    async def track_action(self, player_id: str, action_type: str, action_data: Dict) -> List[Dict]:
        """Track player action and update relevant quest objectives."""
        try:
            # Get active quests for player
            active_quests = await self.quest_progress.find({
                "player_id": player_id,
                "status": "active"
            }).to_list(None)

            updated_quests = []

            for progress in active_quests:
                # Get quest details
                quest = await self.quests.find_one({"_id": progress["quest_id"]})
                if not quest:
                    continue

                # Check each objective
                objectives = quest.get("objectives", [])
                for i, objective in enumerate(objectives):
                    if self._matches_objective(objective, action_type, action_data):
                        # Update progress
                        current = progress["objectives_progress"][i]["current"]
                        new_progress = current + 1

                        await self.quest_progress.update_one(
                            {"_id": progress["_id"]},
                            {
                                "$set": {
                                    f"objectives_progress.{i}.current": new_progress,
                                    f"objectives_progress.{i}.completed": (
                                        new_progress >= objective.get(
                                            "required", 1)
                                    )
                                }
                            }
                        )

                        updated_quests.append({
                            "quest_id": str(quest["_id"]),
                            "quest_title": quest.get("title"),
                            "objective_id": i,
                            "objective_description": objective.get("description"),
                            "progress": new_progress,
                            "required": objective.get("required", 1)
                        })

            return updated_quests

        except Exception as e:
            logger.error(f"Error tracking action: {e}")
            return []

    def _matches_objective(self, objective: Dict, action_type: str, action_data: Dict) -> bool:
        """Check if action matches objective criteria."""
        obj_type = objective.get("type")

        # Match by action type
        type_mapping = {
            "hack": ["hack", "cyber_attack"],
            "steal": ["steal", "theft"],
            "help": ["help", "assist"],
            "donate": ["donate", "give"],
            "trade": ["trade", "exchange"],
            "combat": ["attack", "fight", "battle"],
            "talk": ["talk", "dialogue", "interact"]
        }

        if obj_type in type_mapping:
            if action_type not in type_mapping[obj_type]:
                return False

        # Match target if specified
        if "target" in objective:
            target = objective["target"]
            if target != action_data.get("target_type"):
                return False

        return True

    async def get_player_quest_stats(self, player_id: str) -> Dict:
        """Get player's quest statistics."""
        try:
            # Aggregate quest stats
            pipeline = [
                {"$match": {"player_id": player_id}},
                {
                    "$group": {
                        "_id": "$status",
                        "count": {"$sum": 1}
                    }
                }
            ]

            results = await self.quest_progress.aggregate(pipeline).to_list(None)

            stats = {
                "total": 0,
                "active": 0,
                "completed": 0,
                "failed": 0,
                "abandoned": 0
            }

            for result in results:
                status = result["_id"]
                count = result["count"]
                stats[status] = count
                stats["total"] += count

            return stats

        except Exception as e:
            logger.error(f"Error getting quest stats: {e}")
            return {}

    async def get_quest_completion_rate(self, player_id: str) -> float:
        """Calculate quest completion rate for player."""
        try:
            stats = await self.get_player_quest_stats(player_id)

            total_started = stats.get(
                "completed", 0) + stats.get("failed", 0) + stats.get("abandoned", 0)
            completed = stats.get("completed", 0)

            if total_started == 0:
                return 0.0

            return (completed / total_started) * 100

        except Exception as e:
            logger.error(f"Error calculating completion rate: {e}")
            return 0.0
