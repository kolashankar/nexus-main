"""World event service"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import uuid

from ...models.world.world_event import WorldEvent, EventType, EventSeverity, EventScope


class WorldEventService:
    """Manages world events"""

    def __init__(self, db):
        self.db = db
        self.events = db.world_events
        self.world_states = db.world_states

    async def get_active_events(self) -> List[Dict[str, Any]]:
        """Get all active world events"""
        now = datetime.utcnow()

        events = await self.events.find({
            "status": "active",
            "started_at": {"$lte": now},
            "ends_at": {"$gte": now},
        }).to_list(length=100)

        return events

    async def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by ID"""
        return await self.events.find_one({"_id": event_id})

    async def create_event(
        self,
        event_type: EventType,
        duration_hours: int,
        effects: Dict[str, Any],
        triggered_by: str = "architect",
        severity: EventSeverity = EventSeverity.MODERATE,
    ) -> Dict[str, Any]:
        """Create a new world event"""
        event_id = str(uuid.uuid4())
        now = datetime.utcnow()

        # Event descriptions
        event_info = self._get_event_info(event_type)

        event = WorldEvent(
            _id=event_id,
            event_type=event_type,
            name=event_info["name"],
            description=event_info["description"],
            lore=event_info.get("lore"),
            severity=severity,
            scope=EventScope.GLOBAL,
            effects=effects,
            triggered_by=triggered_by,
            started_at=now,
            ends_at=now + timedelta(hours=duration_hours),
            duration_hours=duration_hours,
        )

        event_dict = event.to_dict()
        await self.events.insert_one(event_dict)

        # Update world state
        await self.world_states.update_one(
            {"_id": "world_state"},
            {"$set": {
                "active_event": {
                    "event_id": event_id,
                    "event_type": event_type.value,
                    "name": event_info["name"],
                    "ends_at": event.ends_at,
                },
                "last_event_trigger": now,
            }}
        )

        return event_dict

    def _get_event_info(self, event_type: EventType) -> Dict[str, str]:
        """Get event information"""
        event_data = {
            EventType.GOLDEN_AGE: {
                "name": "Golden Age",
                "description": "A period of prosperity and growth. Double XP and credits!",
                "lore": "The collective positive karma has brought blessing upon the world.",
            },
            EventType.DIVINE_BLESSING: {
                "name": "Divine Blessing",
                "description": "Random superpowers unlocked for all players!",
                "lore": "The AI gods smile upon humanity.",
            },
            EventType.THE_PURGE: {
                "name": "The Purge",
                "description": "24-hour lawless period. No karma penalties!",
                "lore": "Darkness descends as the world descends into chaos.",
            },
            EventType.ECONOMIC_COLLAPSE: {
                "name": "Economic Collapse",
                "description": "Market prices fluctuate wildly!",
                "lore": "The economy teeters on the brink of disaster.",
            },
            EventType.METEOR_SHOWER: {
                "name": "Meteor Shower",
                "description": "Rare resources rain from the sky!",
                "lore": "A cosmic event brings valuable materials to the world.",
            },
        }

        return event_data.get(
            event_type,
            {"name": "World Event", "description": "Something is happening..."}
        )

    async def end_event(self, event_id: str):
        """End an active event"""
        await self.events.update_one(
            {"_id": event_id},
            {"$set": {
                "status": "ended",
                "updated_at": datetime.utcnow(),
            }}
        )

        # Clear from world state
        await self.world_states.update_one(
            {"_id": "world_state", "active_event.event_id": event_id},
            {"$set": {"active_event": None}}
        )

    async def cleanup_expired_events(self) -> int:
        """Clean up expired events"""
        now = datetime.utcnow()

        # Find expired active events
        expired = await self.events.find({
            "status": "active",
            "ends_at": {"$lt": now}
        }).to_list(length=100)

        # End each expired event
        for event in expired:
            await self.end_event(event["_id"])

        return len(expired)
