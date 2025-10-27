"""Regional Events Service - Territory-specific events."""

from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from backend.core.database import db
import uuid
import random


class RegionalEventsService:
    """Service for managing regional events in territories."""

    def __init__(self):
        self.db = db
        self.event_types = {
            "resource_surge": {
                "name": "Resource Surge",
                "description": "Increased resource generation in this territory",
                "duration": 2 * 60 * 60,  # 2 hours
                "effects": {"resource_multiplier": 2.0}
            },
            "hostile_takeover": {
                "name": "Hostile Takeover Attempt",
                "description": "Territory under attack, defend to maintain control",
                "duration": 1 * 60 * 60,
                "effects": {"defense_required": True}
            },
            "market_boom": {
                "name": "Local Market Boom",
                "description": "Better prices in this territory's marketplace",
                "duration": 3 * 60 * 60,
                "effects": {"price_bonus": 0.2}
            },
            "npc_raid": {
                "name": "NPC Raid",
                "description": "AI-controlled enemies are attacking",
                "duration": 30 * 60,
                "effects": {"combat_challenge": True}
            },
            "festival": {
                "name": "Local Festival",
                "description": "Celebration brings bonuses to all activities",
                "duration": 4 * 60 * 60,
                "effects": {"xp_bonus": 0.5, "karma_bonus": 0.3}
            },
            "disaster": {
                "name": "Natural Disaster",
                "description": "Territory affected by environmental hazard",
                "duration": 2 * 60 * 60,
                "effects": {"activity_penalty": 0.3}
            }
        }

    async def trigger_regional_event(
        self,
        territory_id: int,
        event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Trigger a regional event for a specific territory."""
        if event_type is None:
            # Random event
            event_type = random.choice(list(self.event_types.keys()))

        if event_type not in self.event_types:
            raise ValueError(f"Unknown event type: {event_type}")

        config = self.event_types[event_type]
        now = datetime.utcnow()
        event_id = str(uuid.uuid4())

        # Get territory info
        world_state = await self.db.world_state.find_one()
        territory = next(
            (t for t in world_state.get("territories", [])
             if t.get("territory_id") == territory_id),
            None
        )

        if not territory:
            raise ValueError(f"Territory {territory_id} not found")

        event = {
            "event_id": event_id,
            "territory_id": territory_id,
            "territory_name": territory.get("name", f"Territory {territory_id}"),
            "event_type": event_type,
            "name": config["name"],
            "description": config["description"],
            "started_at": now,
            "ends_at": now + timedelta(seconds=config["duration"]),
            "effects": config["effects"],
            "is_active": True,
            "participants": [],
            "created_at": now
        }

        # Insert event
        await self.db.regional_events.insert_one(event)

        # Notify players in the territory
        await self._notify_territory_players(territory_id, event)

        return event

    async def get_territory_events(
        self,
        territory_id: int,
        active_only: bool = True
    ) -> List[Dict[str, Any]]:
        """Get all events for a territory."""
        query = {"territory_id": territory_id}
        if active_only:
            query["is_active"] = True
            query["ends_at"] = {"$gt": datetime.utcnow()}

        events = await self.db.regional_events.find(query).to_list(length=50)
        return events

    async def participate_in_event(
        self,
        event_id: str,
        player_id: str,
        action: str
    ) -> Dict[str, Any]:
        """Record player participation in a regional event."""
        event = await self.db.regional_events.find_one({"event_id": event_id})

        if not event:
            raise ValueError("Event not found")

        if not event["is_active"]:
            raise ValueError("Event is not active")

        # Record participation
        participation = {
            "player_id": player_id,
            "action": action,
            "timestamp": datetime.utcnow()
        }

        await self.db.regional_events.update_one(
            {"event_id": event_id},
            {"$push": {"participants": participation}}
        )

        # Apply event-specific logic
        rewards = await self._process_event_participation(
            event=event,
            player_id=player_id,
            action=action
        )

        return rewards

    async def _process_event_participation(
        self,
        event: Dict[str, Any],
        player_id: str,
        action: str
    ) -> Dict[str, Any]:
        """Process player participation and grant rewards."""
        rewards = {"xp": 0, "credits": 0, "karma": 0}

        event_type = event["event_type"]

        if event_type == "resource_surge":
            # Bonus resources
            rewards["credits"] = random.randint(100, 500)
        elif event_type == "hostile_takeover" and action == "defend":
            # Defend rewards
            rewards["xp"] = random.randint(200, 500)
            rewards["karma"] = 10
        elif event_type == "npc_raid" and action == "combat":
            # Combat rewards
            rewards["xp"] = random.randint(150, 400)
            rewards["credits"] = random.randint(50, 200)
        elif event_type == "festival":
            # Festival participation
            rewards["xp"] = random.randint(50, 150)
            rewards["karma"] = 5

        # Grant rewards to player
        if rewards["xp"] > 0:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"xp": rewards["xp"]}}
            )

        if rewards["credits"] > 0:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"currencies.credits": rewards["credits"]}}
            )

        if rewards["karma"] > 0:
            await self.db.players.update_one(
                {"_id": player_id},
                {"$inc": {"karma_points": rewards["karma"]}}
            )

        return rewards

    async def _notify_territory_players(
        self,
        territory_id: int,
        event: Dict[str, Any]
    ):
        """Notify players in the territory about the event."""
        # Get players in this territory
        players_in_territory = await self.db.players.find({
            "location.territory_id": territory_id,
            "online": True
        }).to_list(length=1000)

        # In a real implementation, this would send WebSocket notifications
        # For now, just log
        print(
            f"Notifying {len(players_in_territory)} players about event: {event['name']}")

    async def end_expired_events(self) -> int:
        """End regional events that have expired."""
        now = datetime.utcnow()
        result = await self.db.regional_events.update_many(
            {"ends_at": {"$lt": now}, "is_active": True},
            {"$set": {"is_active": False}}
        )
        return result.modified_count

    async def trigger_random_events(self, num_events: int = 3):
        """Trigger random regional events across territories."""
        # Get all territories
        world_state = await self.db.world_state.find_one()
        if not world_state:
            return

        territories = world_state.get("territories", [])
        if not territories:
            return

        # Select random territories
        selected = random.sample(
            territories,
            min(num_events, len(territories))
        )

        events = []
        for territory in selected:
            try:
                event = await self.trigger_regional_event(
                    territory_id=territory["territory_id"]
                )
                events.append(event)
            except Exception as e:
                print(
                    f"Error triggering event for territory {territory['territory_id']}: {e}")

        return events
