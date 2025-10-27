"""Quest WebSocket events"""

from typing import Dict, Any


class QuestEventHandler:
    """Handles quest-related WebSocket events"""

    def __init__(self, manager):
        self.manager = manager

    async def handle_quest_accepted(self, player_id: str, quest_data: Dict[str, Any]):
        """Broadcast quest accepted event"""
        await self.manager.broadcast_to_player(
            player_id,
            {
                "type": "quest_accepted",
                "data": {
                    "quest_id": quest_data.get("_id"),
                    "title": quest_data.get("title"),
                    "quest_type": quest_data.get("quest_type"),
                }
            }
        )

    async def handle_quest_progress(self, player_id: str, quest_id: str, objective_id: str, progress: int):
        """Broadcast quest progress update"""
        await self.manager.broadcast_to_player(
            player_id,
            {
                "type": "quest_progress",
                "data": {
                    "quest_id": quest_id,
                    "objective_id": objective_id,
                    "progress": progress,
                }
            }
        )

    async def handle_quest_completed(self, player_id: str, quest_data: Dict[str, Any], rewards: Dict[str, Any]):
        """Broadcast quest completion"""
        await self.manager.broadcast_to_player(
            player_id,
            {
                "type": "quest_completed",
                "data": {
                    "quest_id": quest_data.get("_id"),
                    "title": quest_data.get("title"),
                    "rewards": rewards,
                }
            }
        )

    async def handle_objective_completed(self, player_id: str, quest_id: str, objective: Dict[str, Any]):
        """Broadcast objective completion"""
        await self.manager.broadcast_to_player(
            player_id,
            {
                "type": "objective_completed",
                "data": {
                    "quest_id": quest_id,
                    "objective_id": objective.get("objective_id"),
                    "description": objective.get("description"),
                }
            }
        )

    async def handle_new_quest_available(self, player_id: str, quest_type: str):
        """Notify player of new quest availability"""
        await self.manager.broadcast_to_player(
            player_id,
            {
                "type": "new_quest_available",
                "data": {
                    "quest_type": quest_type,
                    "message": f"New {quest_type} quest available!",
                }
            }
        )
