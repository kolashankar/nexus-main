"""World Event Manager"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorDatabase

from ...models.world.karma_event import KarmaEventModel, EventStatus, EventParticipation
from ..ai.architect.architect import Architect
from ..ai.architect.triggers import EventTrigger, TriggerEvaluator
from ..ai.architect.schemas import WorldState
from .state_manager import WorldStateManager
from .collective_karma import CollectiveKarmaTracker

logger = logging.getLogger(__name__)


class EventManager:
    """
    Manages world events - creation, activation, and lifecycle
    Works with The Architect AI to trigger events
    """

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.karma_events
        self.architect = Architect()
        self.trigger_evaluator = TriggerEvaluator()
        self.world_state_manager = WorldStateManager(db)
        self.karma_tracker = CollectiveKarmaTracker(db)
        logger.info("EventManager initialized")

    async def check_and_trigger_event(self, force: bool = False) -> Optional[KarmaEventModel]:
        """
        Check if an event should be triggered and create it
        Called periodically by background task
        
        Args:
            force: Force event generation even if conditions not met
        
        Returns:
            Created event if triggered, None otherwise
        """
        logger.info("Checking event trigger conditions")

        # Check if there's already an active event
        active_event = await self.get_active_global_event()
        if active_event and not force:
            logger.info(f"Event already active: {active_event.name}")
            return None

        # Get world state
        world_state_model = await self.world_state_manager.get_world_state()

        # Convert to Architect's WorldState schema
        time_since_last = await self.world_state_manager.get_time_since_last_event()

        world_state = WorldState(
            collective_karma=world_state_model.collective_karma,
            average_karma=world_state_model.average_karma,
            karma_trend=world_state_model.karma_trend,
            total_players=world_state_model.total_players,
            online_players=world_state_model.online_players,
            total_actions_24h=world_state_model.total_actions_24h,
            positive_actions_24h=world_state_model.positive_actions_24h,
            negative_actions_24h=world_state_model.negative_actions_24h,
            guild_wars_active=world_state_model.guild_wars_active,
            territories_contested=world_state_model.territories_contested,
            market_health=world_state_model.market_health,
            last_global_event=world_state_model.last_global_event_type,
            time_since_last_event=time_since_last
        )

        # Evaluate trigger conditions
        conditions = EventTrigger.evaluate_conditions(world_state)
        evaluation = await self.trigger_evaluator.should_trigger_event(world_state, conditions)

        if not evaluation.should_trigger and not force:
            logger.info(f"Event trigger not needed: {evaluation.reasoning}")
            return None

        logger.info(
            f"Event trigger confirmed! "
            f"Reason: {evaluation.reasoning}, "
            f"Confidence: {evaluation.confidence:.2f}"
        )

        # Generate event using The Architect
        event_response = await self.architect.generate_global_event(
            world_state=world_state,
            force_event_type=evaluation.event_type_suggestion,
            context=evaluation.reasoning
        )

        # Create and save event
        event = await self.create_event(event_response.dict(), world_state_model.dict())

        # Activate event immediately
        await self.activate_event(event.event_id)

        logger.info(
            f"Event created and activated: {event.name} ({event.event_type})")

        return event

    async def create_event(
        self,
        event_data: Dict[str, Any],
        world_state_snapshot: Dict[str, Any]
    ) -> KarmaEventModel:
        """
        Create a new event from Architect response
        
        Args:
            event_data: Event data from Architect
            world_state_snapshot: Snapshot of world state at creation
        
        Returns:
            Created KarmaEventModel
        """
        event = KarmaEventModel(
            **event_data,
            status=EventStatus.SCHEDULED,
            world_state_snapshot=world_state_snapshot,
            triggered_by="architect",
            karma_at_trigger=world_state_snapshot.get("collective_karma", 0.0),
            created_at=datetime.utcnow()
        )

        # Save to database
        event_dict = event.dict()
        await self.collection.insert_one(event_dict)

        logger.info(f"Event created in database: {event.event_id}")

        return event

    async def activate_event(self, event_id: str) -> KarmaEventModel:
        """
        Activate an event (make it live)
        
        Args:
            event_id: Event ID to activate
        
        Returns:
            Activated event
        """
        event = await self.get_event_by_id(event_id)

        if not event:
            raise ValueError(f"Event not found: {event_id}")

        if event.status == EventStatus.ACTIVE:
            logger.warning(f"Event already active: {event_id}")
            return event

        # Update event
        now = datetime.utcnow()
        ends_at = now + timedelta(hours=event.duration_hours)

        await self.collection.update_one(
            {"event_id": event_id},
            {"$set": {
                "status": EventStatus.ACTIVE.value,
                "started_at": now,
                "ends_at": ends_at
            }}
        )

        # Update world state
        await self.world_state_manager.set_active_event({
            "event_id": event_id,
            "event_type": event.event_type,
            "name": event.name,
            "ends_at": ends_at.isoformat()
        })

        logger.info(f"Event activated: {event.name} - ends at {ends_at}")

        # Broadcast event to all players (via WebSocket)
        # This would be handled by WebSocket manager

        return await self.get_event_by_id(event_id)

    async def end_event(self, event_id: str, actual_impact: Optional[str] = None) -> None:
        """
        End an active event
        
        Args:
            event_id: Event to end
            actual_impact: Actual impact assessment (optional)
        """
        now = datetime.utcnow()

        update = {
            "status": EventStatus.ENDED.value,
            "ended_at": now
        }

        if actual_impact:
            update["actual_impact"] = actual_impact

        await self.collection.update_one(
            {"event_id": event_id},
            {"$set": update}
        )

        # Update world state
        await self.world_state_manager.end_active_event()

        logger.info(f"Event ended: {event_id}")

    async def get_event_by_id(self, event_id: str) -> Optional[KarmaEventModel]:
        """
        Get event by ID
        
        Args:
            event_id: Event ID
        
        Returns:
            Event or None if not found
        """
        event_doc = await self.collection.find_one({"event_id": event_id})

        if not event_doc:
            return None

        event_doc.pop("_id", None)
        return KarmaEventModel(**event_doc)

    async def get_active_global_event(self) -> Optional[KarmaEventModel]:
        """
        Get currently active global event
        
        Returns:
            Active event or None
        """
        event_doc = await self.collection.find_one({
            "status": EventStatus.ACTIVE.value,
            "is_global": True
        })

        if not event_doc:
            return None

        event_doc.pop("_id", None)
        return KarmaEventModel(**event_doc)

    async def get_active_regional_events(self, territory_id: int) -> List[KarmaEventModel]:
        """
        Get active events for a territory
        
        Args:
            territory_id: Territory ID
        
        Returns:
            List of active regional events
        """
        cursor = self.collection.find({
            "status": EventStatus.ACTIVE.value,
            "is_global": False,
            "affected_territories": territory_id
        })

        events = []
        async for doc in cursor:
            doc.pop("_id", None)
            events.append(KarmaEventModel(**doc))

        return events

    async def get_recent_events(self, limit: int = 10) -> List[KarmaEventModel]:
        """
        Get recent events (active + ended)
        
        Args:
            limit: Maximum number of events to return
        
        Returns:
            List of recent events
        """
        cursor = self.collection.find().sort("created_at", -1).limit(limit)

        events = []
        async for doc in cursor:
            doc.pop("_id", None)
            events.append(KarmaEventModel(**doc))

        return events

    async def record_participation(
        self,
        event_id: str,
        player_id: str,
        username: str
    ) -> bool:
        """
        Record player participation in event
        
        Args:
            event_id: Event ID
            player_id: Player ID
            username: Player username
        
        Returns:
            True if recorded, False if already participated
        """
        event = await self.get_event_by_id(event_id)

        if not event or not event.requires_participation:
            return False

        # Check if already participated
        existing = any(p.player_id == player_id for p in event.participants)

        if existing:
            # Update participation count
            await self.collection.update_one(
                {"event_id": event_id, "participants.player_id": player_id},
                {
                    "$inc": {"participants.$.participation_count": 1},
                    "$set": {"participants.$.last_participated": datetime.utcnow()}
                }
            )
            return True

        # Add new participant
        participation = EventParticipation(
            player_id=player_id,
            username=username,
            participation_count=1
        )

        await self.collection.update_one(
            {"event_id": event_id},
            {
                "$push": {"participants": participation.dict()},
                "$inc": {"total_participants": 1}
            }
        )

        logger.info(f"Player {username} participated in event {event_id}")
        return True

    async def cleanup_expired_events(self) -> int:
        """
        End events that have passed their end time
        Called by background task
        
        Returns:
            Number of events ended
        """
        now = datetime.utcnow()

        # Find expired active events
        cursor = self.collection.find({
            "status": EventStatus.ACTIVE.value,
            "ends_at": {"$lte": now}
        })

        count = 0
        async for event_doc in cursor:
            await self.end_event(event_doc["event_id"])
            count += 1

        if count > 0:
            logger.info(f"Cleaned up {count} expired events")

        return count
