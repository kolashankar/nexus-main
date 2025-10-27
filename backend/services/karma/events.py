from typing import Dict, Any, List
from datetime import datetime
from backend.core.database import get_database
import uuid

class KarmaEventManager:
    """Manages karma-related events"""

    def __init__(self):
        self.db = get_database()

    async def create_karma_event(
        self,
        event_type: str,
        player_id: str,
        karma_change: int,
        description: str,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create a new karma event"""
        event = {
            "_id": str(uuid.uuid4()),
            "event_type": event_type,
            "player_id": player_id,
            "karma_change": karma_change,
            "description": description,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow()
        }

        await self.db.karma_events.insert_one(event)
        return event

    async def get_player_karma_history(
        self,
        player_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get player's karma event history"""
        events = await self.db.karma_events.find(
            {"player_id": player_id}
        ).sort("timestamp", -1).limit(limit).to_list(length=limit)

        return events

    async def get_recent_karma_events(
        self,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get recent karma events across all players"""
        events = await self.db.karma_events.find(
        ).sort("timestamp", -1).limit(limit).to_list(length=limit)

        return events
