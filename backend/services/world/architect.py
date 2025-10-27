"""The Architect service - AI that manages world events"""

from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import random

from ...models.world.world_event import EventType, EventSeverity
from .event_service import WorldEventService


class ArchitectService:
    """The Architect - AI that triggers world events based on collective karma"""

    def __init__(self, db):
        self.db = db
        self.world_states = db.world_states
        self.event_service = WorldEventService(db)

    async def evaluate_world_state(self) -> Optional[Dict[str, Any]]:
        """Evaluate world state and potentially trigger event"""
        # Get world state
        state = await self.world_states.find_one({"_id": "world_state"})
        if not state:
            return None

        # Check if there's already an active event
        if state.get("active_event"):
            return None

        # Get global karma
        collective_karma = state.get(
            "global_karma", {}).get("collective_karma", 0)
        karma_trend = state.get("global_karma", {}).get(
            "karma_trend", "stable")

        # Decide if event should trigger
        should_trigger, event_type = self._should_trigger_event(
            collective_karma,
            karma_trend,
            state
        )

        if should_trigger and event_type:
            # Trigger event
            event = await self._trigger_event(event_type, collective_karma)
            return event

        return None

    def _should_trigger_event(
        self,
        collective_karma: int,
        karma_trend: str,
        state: Dict[str, Any],
    ) -> tuple[bool, Optional[EventType]]:
        """Determine if an event should trigger"""
        # Check last event time
        last_event = state.get("last_event_trigger")
        if last_event:
            if isinstance(last_event, str):
                last_event = datetime.fromisoformat(
                    last_event.replace("Z", "+00:00"))

            # Don't trigger events too frequently (min 6 hours)
            if datetime.utcnow() - last_event < timedelta(hours=6):
                return False, None

        # Very high positive karma
        if collective_karma > 10000:
            return True, random.choice([
                EventType.GOLDEN_AGE,
                EventType.DIVINE_BLESSING,
                EventType.FESTIVAL_OF_LIGHT,
            ])

        # Very low negative karma
        if collective_karma < -10000:
            return True, random.choice([
                EventType.THE_PURGE,
                EventType.JUDGMENT_DAY,
                EventType.DARK_ECLIPSE,
            ])

        # Random neutral events (10% chance)
        if random.random() < 0.1:
            return True, random.choice([
                EventType.METEOR_SHOWER,
                EventType.GLITCH_IN_MATRIX,
                EventType.TIME_ANOMALY,
            ])

        return False, None

    async def _trigger_event(
        self,
        event_type: EventType,
        collective_karma: int,
    ) -> Dict[str, Any]:
        """Trigger a world event"""
        # Determine duration
        duration = self._get_event_duration(event_type)

        # Determine effects
        effects = self._get_event_effects(event_type)

        # Determine severity
        severity = self._get_event_severity(event_type, collective_karma)

        # Create event
        event = await self.event_service.create_event(
            event_type=event_type,
            duration_hours=duration,
            effects=effects,
            triggered_by="architect",
            severity=severity,
        )

        return event

    def _get_event_duration(self, event_type: EventType) -> int:
        """Get event duration in hours"""
        durations = {
            EventType.GOLDEN_AGE: 24,
            EventType.DIVINE_BLESSING: 12,
            EventType.THE_PURGE: 24,
            EventType.ECONOMIC_COLLAPSE: 48,
            EventType.METEOR_SHOWER: 6,
            EventType.GLITCH_IN_MATRIX: 2,
        }
        return durations.get(event_type, 12)

    def _get_event_effects(self, event_type: EventType) -> Dict[str, Any]:
        """Get event effects"""
        effects_map = {
            EventType.GOLDEN_AGE: {
                "xp_multiplier": 2.0,
                "credits_multiplier": 2.0,
            },
            EventType.DIVINE_BLESSING: {
                "random_power_unlock": True,
            },
            EventType.THE_PURGE: {
                "karma_penalties_disabled": True,
                "pvp_enabled_everywhere": True,
            },
            EventType.ECONOMIC_COLLAPSE: {
                "price_volatility": 0.5,
            },
            EventType.METEOR_SHOWER: {
                "resource_spawn_rate": 5.0,
            },
        }
        return effects_map.get(event_type, {})

    def _get_event_severity(self, event_type: EventType, karma: int) -> EventSeverity:
        """Determine event severity"""
        if abs(karma) > 50000:
            return EventSeverity.CATASTROPHIC
        elif abs(karma) > 30000:
            return EventSeverity.CRITICAL
        elif abs(karma) > 15000:
            return EventSeverity.MAJOR
        else:
            return EventSeverity.MODERATE
