"""Quest tracking service - Tracks player actions for quest objectives"""

from typing import Dict, Any, List
from datetime import datetime


class QuestTrackingService:
    """Tracks player actions and updates quest progress automatically"""

    def __init__(self, db):
        self.db = db
        self.quests = db.quests
        self.players = db.players

    async def track_action(
        self,
        player_id: str,
        action_type: str,
        action_data: Dict[str, Any],
    ) -> List[str]:
        """Track an action and update relevant quest objectives"""
        # Get all active quests
        active_quests = await self.quests.find({
            "player_id": player_id,
            "status": "active",
        }).to_list(length=100)

        updated_quest_ids = []

        for quest in active_quests:
            updated = False
            objectives = quest.get("objectives", [])

            for obj in objectives:
                if obj.get("completed"):
                    continue

                # Check if action matches objective
                if self._matches_objective(action_type, obj["type"], action_data, obj):
                    obj["current"] = min(
                        obj["current"] + 1,
                        obj["required"]
                    )

                    if obj["current"] >= obj["required"]:
                        obj["completed"] = True

                    updated = True

            if updated:
                await self.quests.update_one(
                    {"_id": quest["_id"]},
                    {
                        "$set": {
                            "objectives": objectives,
                            "updated_at": datetime.utcnow(),
                        }
                    }
                )
                updated_quest_ids.append(quest["_id"])

        return updated_quest_ids

    def _matches_objective(
        self,
        action_type: str,
        objective_type: str,
        action_data: Dict[str, Any],
        objective: Dict[str, Any],
    ) -> bool:
        """Check if action matches objective type"""
        action_map = {
            "hack": "hack",
            "help": "help",
            "steal": "steal",
            "donate": "donate",
            "trade": "trade",
            "combat_win": "win_combat",
            "duel_win": "win_duel",
        }

        return action_map.get(action_type) == objective_type

    async def check_completable_quests(
        self,
        player_id: str,
    ) -> List[Dict[str, Any]]:
        """Check which quests are ready to be completed"""
        active_quests = await self.quests.find({
            "player_id": player_id,
            "status": "active",
        }).to_list(length=100)

        completable = []
        for quest in active_quests:
            all_done = all(
                obj.get("completed", False)
                for obj in quest.get("objectives", [])
            )
            if all_done:
                completable.append(quest)

        return completable
