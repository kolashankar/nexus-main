"""World Events Service - Manages dynamic world events."""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from backend.core.database import db
from backend.services.ai.architect.architect import Architect
import random
import uuid


class WorldEventsService:
    """Service for managing world events triggered by collective karma."""

    def __init__(self):
        self.db = db
        self.architect = Architect()
        self.event_types = {
            # Positive Events (triggered by high positive karma)
            "golden_age": {
                "name": "Golden Age",
                "description": "24hr double XP/cash for all players",
                "duration": 24 * 60 * 60,  # 24 hours
                "effects": {"xp_multiplier": 2.0, "cash_multiplier": 2.0},
                "karma_threshold": 10000
            },
            "divine_blessing": {
                "name": "Divine Blessing",
                "description": "Random superpowers unlocked for players",
                "duration": 12 * 60 * 60,
                "effects": {"random_power_unlock": True},
                "karma_threshold": 8000
            },
            "festival_of_light": {
                "name": "Festival of Light",
                "description": "Massive marketplace with rare items",
                "duration": 48 * 60 * 60,
                "effects": {"rare_items_available": True, "discount": 0.3},
                "karma_threshold": 6000
            },
            "the_convergence": {
                "name": "The Convergence",
                "description": "All players can see hidden traits temporarily",
                "duration": 6 * 60 * 60,
                "effects": {"reveal_all_traits": True},
                "karma_threshold": 5000
            },
            # Negative Events (triggered by low collective karma)
            "the_purge": {
                "name": "The Purge",
                "description": "24hr lawless period, no karma penalties",
                "duration": 24 * 60 * 60,
                "effects": {"karma_penalties_disabled": True},
                "karma_threshold": -10000
            },
            "economic_collapse": {
                "name": "Economic Collapse",
                "description": "All prices fluctuate wildly",
                "duration": 12 * 60 * 60,
                "effects": {"price_volatility": 0.5},
                "karma_threshold": -8000
            },
            "dark_eclipse": {
                "name": "Dark Eclipse",
                "description": "Vision reduced, stealth boosted",
                "duration": 6 * 60 * 60,
                "effects": {"vision_range": 0.5, "stealth_bonus": 2.0},
                "karma_threshold": -6000
            },
            "judgment_day": {
                "name": "Judgment Day",
                "description": "AI Arbiter directly punishes worst players",
                "duration": 3 * 60 * 60,
                "effects": {"arbiter_judgment": True},
                "karma_threshold": -12000
            },
            # Neutral Events
            "meteor_shower": {
                "name": "Meteor Shower",
                "description": "Rare resources spawn across the world",
                "duration": 2 * 60 * 60,
                "effects": {"resource_spawn_rate": 3.0},
                "karma_threshold": None
            },
            "glitch_in_matrix": {
                "name": "Glitch in the Matrix",
                "description": "Random effects occur",
                "duration": 1 * 60 * 60,
                "effects": {"random_effects": True},
                "karma_threshold": None
            },
            "robot_uprising": {
                "name": "Robot Uprising",
                "description": "AI robots attack everyone",
                "duration": 4 * 60 * 60,
                "effects": {"hostile_robots": True},
                "karma_threshold": None
            },
            "time_anomaly": {
                "name": "Time Anomaly",
                "description": "Game time speeds up or slows down",
                "duration": 2 * 60 * 60,
                "effects": {"time_multiplier": random.choice([0.5, 2.0])},
                "karma_threshold": None
            }
        }

    async def get_world_state(self) -> Dict[str, Any]:
        """Get current world state."""
        world_state = await self.db.world_state.find_one()
        if not world_state:
            # Initialize world state
            world_state = await self._initialize_world_state()
        return world_state

    async def _initialize_world_state(self) -> Dict[str, Any]:
        """Initialize world state."""
        now = datetime.utcnow()
        initial_state = {
            "collective_karma": 0.0,
            "karma_trend": "stable",
            "active_event": None,
            "current_season": 1,
            "season_start": now,
            "season_end": now + timedelta(days=90),  # 3 months
            "total_players": 0,
            "online_players": 0,
            "total_karma_generated": 0.0,
            "territories": [],
            "last_updated": now
        }
        await self.db.world_state.insert_one(initial_state)
        return initial_state

    async def get_active_events(self, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all active world events."""
        query = {"is_active": True, "ends_at": {"$gt": datetime.utcnow()}}
        if event_type:
            query["event_type"] = event_type

        events = await self.db.world_events.find(query).to_list(length=100)
        return events

    async def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get specific event details."""
        event = await self.db.world_events.find_one({"event_id": event_id})
        return event

    async def trigger_event(
        self,
        event_type: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Trigger a world event."""
        if event_type not in self.event_types:
            raise ValueError(f"Unknown event type: {event_type}")

        event_config = self.event_types[event_type]
        now = datetime.utcnow()
        event_id = str(uuid.uuid4())

        event = {
            "event_id": event_id,
            "event_type": event_type,
            "name": event_config["name"],
            "description": event_config["description"],
            "started_at": now,
            "ends_at": now + timedelta(seconds=event_config["duration"]),
            "effects": event_config["effects"],
            "trigger_reason": parameters.get("reason") if parameters else "Manual trigger",
            "affected_territories": parameters.get("territories", []) if parameters else [],
            "participants": 0,
            "is_active": True,
            "responses": []
        }

        # Insert event
        await self.db.world_events.insert_one(event)

        # Update world state
        await self.db.world_state.update_one(
            {},
            {"$set": {"active_event": event}}
        )

        return event

    async def respond_to_event(
        self,
        event_id: str,
        player_id: str,
        response: str
    ) -> Dict[str, Any]:
        """Record player response to an event."""
        event = await self.get_event(event_id)
        if not event:
            raise ValueError("Event not found")

        if not event["is_active"]:
            raise ValueError("Event is not active")

        # Record response
        response_data = {
            "player_id": player_id,
            "response": response,
            "timestamp": datetime.utcnow()
        }

        await self.db.world_events.update_one(
            {"event_id": event_id},
            {
                "$push": {"responses": response_data},
                "$inc": {"participants": 1}
            }
        )

        return {"success": True, "message": "Response recorded"}

    async def get_regional_events(
        self,
        territory_id: int
    ) -> List[Dict[str, Any]]:
        """Get regional events for a specific territory."""
        events = await self.db.regional_events.find({
            "territory_id": territory_id,
            "is_active": True
        }).to_list(length=50)
        return events

    async def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get world event history."""
        events = await self.db.world_events.find().sort(
            "started_at", -1
        ).limit(limit).to_list(length=limit)
        return events

    async def check_and_trigger_karma_events(self, collective_karma: float):
        """Check if collective karma triggers any events."""
        for event_type, config in self.event_types.items():
            threshold = config.get("karma_threshold")
            if threshold is None:
                continue

            # Check if threshold is met
            if threshold > 0 and collective_karma >= threshold:
                # Trigger positive event
                await self.trigger_event(event_type, {
                    "reason": f"Collective karma reached {collective_karma}"
                })
            elif threshold < 0 and collective_karma <= threshold:
                # Trigger negative event
                await self.trigger_event(event_type, {
                    "reason": f"Collective karma fell to {collective_karma}"
                })

    async def end_expired_events(self):
        """End events that have expired."""
        now = datetime.utcnow()
        result = await self.db.world_events.update_many(
            {"ends_at": {"$lt": now}, "is_active": True},
            {"$set": {"is_active": False}}
        )
        return result.modified_count
