"""The Architect - World Events AI"""

import logging
import json
from typing import Dict, Any, Optional

from ..base import BaseAIService
from .prompts import (
    ARCHITECT_SYSTEM_PROMPT,
    EVENT_GENERATION_PROMPT,
    REGIONAL_EVENT_PROMPT
)
from .schemas import (
    WorldEventResponse,
    WorldState,
    EventType,
    EventSeverity,
    EventEffect
)
from ..client import get_ai_client
from ..cache_manager import AICacheManager

logger = logging.getLogger(__name__)


class Architect(BaseAIService):
    """The Architect - Overseer of World Events"""

    def __init__(self):
        super().__init__("Architect", model="gpt-4o")
        self.cache_manager = AICacheManager()
        self.client = get_ai_client()
        logger.info("The Architect initialized - World events system online")

    async def generate_global_event(
        self,
        world_state: WorldState,
        force_event_type: Optional[EventType] = None,
        context: Optional[str] = None
    ) -> WorldEventResponse:
        """
        Generate a global world event based on collective karma
        
        Args:
            world_state: Current state of the world
            force_event_type: Force a specific event type (for admin triggers)
            context: Additional context for event generation
        
        Returns:
            WorldEventResponse with full event details
        """
        logger.info(
            f"Generating global event: "
            f"collective_karma={world_state.collective_karma}, "
            f"avg_karma={world_state.average_karma}, "
            f"trend={world_state.karma_trend}"
        )

        # Check cache for similar world states
        cache_key = self._generate_cache_key(world_state)
        cached_event = await self.cache_manager.get(cache_key)

        if cached_event and not force_event_type:
            logger.info("Using cached event for similar world state")
            return WorldEventResponse(**cached_event, cached=True)

        # Prepare world state summary
        world_state_summary = self._format_world_state(world_state)

        # Build context
        full_context = f"""
Triggered by: {context or 'Automatic karma threshold'}
Forced event type: {force_event_type.value if force_event_type else 'None - AI decides'}

World Karma Summary:
- Collective Karma: {world_state.collective_karma:,.0f}
- Average Karma: {world_state.average_karma:.2f}
- Trend: {world_state.karma_trend}
- Total Players: {world_state.total_players:,}
- Online Now: {world_state.online_players:,}

Recent Activity (24h):
- Total Actions: {world_state.total_actions_24h:,}
- Positive Actions: {world_state.positive_actions_24h:,} ({self._percentage(world_state.positive_actions_24h, world_state.total_actions_24h)}%)
- Negative Actions: {world_state.negative_actions_24h:,} ({self._percentage(world_state.negative_actions_24h, world_state.total_actions_24h)}%)

World Conflicts:
- Active Guild Wars: {world_state.guild_wars_active}
- Contested Territories: {world_state.territories_contested}

Market: {world_state.market_health}
Last Event: {world_state.last_global_event or 'None'} ({world_state.time_since_last_event or 0:.1f}h ago)
        """

        # Generate event using AI
        try:
            prompt = EVENT_GENERATION_PROMPT.format(
                world_state=world_state_summary,
                context=full_context
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ARCHITECT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,  # High creativity for dramatic events
                max_tokens=2000
            )

            event_data = json.loads(response.choices[0].message.content)

            # Build event response
            event = WorldEventResponse(
                event_id=self._generate_event_id(),
                event_type=EventType(event_data["event_type"]),
                severity=EventSeverity(event_data["severity"]),
                name=event_data["name"],
                description=event_data["description"],
                lore=event_data["lore"],
                effects=[
                    EventEffect(**effect) for effect in event_data["effects"]
                ],
                duration_hours=event_data["duration_hours"],
                is_global=event_data.get("is_global", True),
                affected_territories=event_data.get(
                    "affected_territories", []),
                requires_participation=event_data.get(
                    "requires_participation", False),
                participation_mechanics=event_data.get(
                    "participation_mechanics"),
                participation_rewards=event_data.get("participation_rewards"),
                trigger_reason=event_data["trigger_reason"],
                collective_karma=world_state.collective_karma,
                estimated_impact=event_data["estimated_impact"],
                architect_reasoning=event_data["architect_reasoning"],
                alternative_events_considered=event_data.get(
                    "alternative_events_considered", [])
            )

            # Cache the event
            if not force_event_type:
                await self.cache_manager.set(
                    cache_key,
                    event.dict(),
                    ttl=3600  # Cache for 1 hour
                )

            logger.info(
                f"Generated event: {event.name} ({event.event_type.value}) - "
                f"Severity: {event.severity.value}, Impact: {event.estimated_impact}"
            )

            return event

        except Exception as e:
            logger.error(f"Error generating event: {e}")
            # Return fallback event
            return self._fallback_event(world_state, force_event_type)

    async def generate_regional_event(
        self,
        territory_state: Dict[str, Any],
        context: Optional[str] = None
    ) -> WorldEventResponse:
        """Generate a territory-specific regional event"""
        logger.info(
            f"Generating regional event for territory {territory_state['territory_id']}")

        try:
            prompt = REGIONAL_EVENT_PROMPT.format(
                territory_state=json.dumps(territory_state, indent=2),
                context=context or "Regional event triggered by local conditions"
            )

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": ARCHITECT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=1500
            )

            event_data = json.loads(response.choices[0].message.content)

            event = WorldEventResponse(
                event_id=self._generate_event_id(),
                event_type=EventType(event_data["event_type"]),
                severity=EventSeverity(event_data["severity"]),
                name=event_data["name"],
                description=event_data["description"],
                lore=event_data["lore"],
                effects=[
                    EventEffect(**effect) for effect in event_data["effects"]
                ],
                duration_hours=event_data["duration_hours"],
                is_global=False,
                affected_territories=[territory_state["territory_id"]],
                requires_participation=event_data.get(
                    "requires_participation", False),
                participation_mechanics=event_data.get(
                    "participation_mechanics"),
                participation_rewards=event_data.get("participation_rewards"),
                trigger_reason=event_data["trigger_reason"],
                collective_karma=territory_state.get("local_karma", 0),
                estimated_impact="medium",
                architect_reasoning=event_data["architect_reasoning"],
                alternative_events_considered=event_data.get(
                    "alternative_events_considered", [])
            )

            logger.info(
                f"Generated regional event: {event.name} for territory {territory_state['territory_id']}")
            return event

        except Exception as e:
            logger.error(f"Error generating regional event: {e}")
            return self._fallback_regional_event(territory_state)

    def _format_world_state(self, world_state: WorldState) -> str:
        """Format world state for AI consumption"""
        return f"""
Collective Karma: {world_state.collective_karma:,.0f}
Average Karma: {world_state.average_karma:.2f}
Trend: {world_state.karma_trend}
Players: {world_state.total_players:,} (Online: {world_state.online_players:,})
Actions (24h): {world_state.total_actions_24h:,}
Market: {world_state.market_health}
        """

    def _generate_cache_key(self, world_state: WorldState) -> str:
        """Generate cache key for similar world states"""
        # Round karma to nearest 1000 for caching similar states
        karma_bucket = int(world_state.collective_karma / 1000) * 1000
        return f"architect:event:{karma_bucket}:{world_state.karma_trend}"

    def _generate_event_id(self) -> str:
        """Generate unique event ID"""
        from uuid import uuid4
        return f"evt_{uuid4().hex[:12]}"

    def _percentage(self, part: int, total: int) -> float:
        """Calculate percentage"""
        if total == 0:
            return 0.0
        return round((part / total) * 100, 1)

    def _fallback_event(self, world_state: WorldState, force_type: Optional[EventType]) -> WorldEventResponse:
        """Generate a fallback event if AI fails"""
        logger.warning("Using fallback event generation")

        # Determine event type based on karma
        if force_type:
            event_type = force_type
        elif world_state.collective_karma > 5000:
            event_type = EventType.GOLDEN_AGE
        elif world_state.collective_karma < -5000:
            event_type = EventType.JUDGMENT_DAY
        else:
            event_type = EventType.METEOR_SHOWER

        return WorldEventResponse(
            event_id=self._generate_event_id(),
            event_type=event_type,
            severity=EventSeverity.MEDIUM,
            name="The Architect's Whisper",
            description="The world shifts as cosmic forces align.",
            lore="In times of uncertainty, the Architect ensures balance is maintained. This event serves as a reminder that all actions have consequences, and the world watches.",
            effects=[
                EventEffect(
                    effect_type="xp_boost",
                    value=1.2,
                    affected_players="all",
                    duration_hours=12.0,
                    description="20% XP boost for all players"
                )
            ],
            duration_hours=12.0,
            is_global=True,
            trigger_reason="Fallback event - AI generation failed",
            collective_karma=world_state.collective_karma,
            estimated_impact="medium",
            architect_reasoning="Fallback event triggered to maintain game experience"
        )

    def _fallback_regional_event(self, territory_state: Dict[str, Any]) -> WorldEventResponse:
        """Fallback regional event"""
        return WorldEventResponse(
            event_id=self._generate_event_id(),
            event_type=EventType.RESOURCE_DISCOVERY,
            severity=EventSeverity.LOW,
            name="Resource Deposit Found",
            description="Local scouts discover a small resource cache.",
            lore="While exploring the territory, local scouts stumbled upon a modest cache of resources. Nothing world-changing, but every bit helps.",
            effects=[
                EventEffect(
                    effect_type="resource_spawn",
                    value=100,
                    affected_players="territory",
                    duration_hours=24.0,
                    description="100 bonus resources spawn in territory"
                )
            ],
            duration_hours=24.0,
            is_global=False,
            affected_territories=[territory_state["territory_id"]],
            trigger_reason="Regional event",
            collective_karma=0,
            estimated_impact="low",
            architect_reasoning="Fallback regional event"
        )

    async def process(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process event generation (base class requirement)"""
        world_state = WorldState(**request.get("world_state", {}))

        if request.get("event_scope") == "regional":
            event = await self.generate_regional_event(
                territory_state=request.get("territory_state", {}),
                context=request.get("context")
            )
        else:
            event = await self.generate_global_event(
                world_state=world_state,
                force_event_type=request.get("force_event_type"),
                context=request.get("context")
            )

        return event.dict()
