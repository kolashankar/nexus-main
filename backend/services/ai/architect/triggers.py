"""Event Trigger System for The Architect"""

import logging
import json
from typing import List

from .prompts import ARCHITECT_SYSTEM_PROMPT, TRIGGER_EVALUATION_PROMPT
from .schemas import (
    WorldState,
    TriggerEvaluation,
    EventTriggerCondition,
    EventType,
    EventSeverity
)
from ..client import get_ai_client

logger = logging.getLogger(__name__)


class EventTrigger:
    """Defines when events should trigger"""

    # Karma thresholds for automatic triggering
    KARMA_THRESHOLDS = {
        "apocalyptic": -10000,
        "severe_negative": -5000,
        "moderate_negative": -1000,
        "neutral": 0,
        "moderate_positive": 5000,
        "high_positive": 10000,
        "golden_age": 15000
    }

    # Minimum time between global events (hours)
    MIN_GLOBAL_EVENT_INTERVAL = 6

    # Recommended event frequency based on online players
    EVENT_FREQUENCY = {
        "very_low": 24,  # < 10 players online
        "low": 12,       # 10-50 players
        "medium": 8,     # 50-100 players
        "high": 6,       # 100-500 players
        "very_high": 4   # 500+ players
    }

    @classmethod
    def evaluate_conditions(cls, world_state: WorldState) -> List[EventTriggerCondition]:
        """
        Evaluate all trigger conditions for the current world state
        
        Returns list of conditions with their current status
        """
        conditions = []

        # Condition 1: Karma threshold reached
        karma_condition = cls._evaluate_karma_threshold(
            world_state.collective_karma)
        conditions.append(karma_condition)

        # Condition 2: Time since last event
        if world_state.time_since_last_event is not None:
            time_condition = cls._evaluate_time_since_last(
                world_state.time_since_last_event,
                world_state.online_players
            )
            conditions.append(time_condition)

        # Condition 3: Action ratio (positive vs negative)
        if world_state.total_actions_24h > 0:
            ratio_condition = cls._evaluate_action_ratio(
                world_state.positive_actions_24h,
                world_state.negative_actions_24h,
                world_state.total_actions_24h
            )
            conditions.append(ratio_condition)

        # Condition 4: World instability (wars + contested territories)
        instability_condition = cls._evaluate_world_instability(
            world_state.guild_wars_active,
            world_state.territories_contested
        )
        conditions.append(instability_condition)

        return conditions

    @classmethod
    def _evaluate_karma_threshold(cls, collective_karma: float) -> EventTriggerCondition:
        """Check if karma has crossed a significant threshold"""
        # Find which threshold was crossed
        threshold_crossed = None

        for name, threshold in sorted(cls.KARMA_THRESHOLDS.items(), key=lambda x: abs(x[1]), reverse=True):
            if collective_karma >= threshold:
                threshold_crossed = threshold
                break

        # Significant if karma is at extreme ends
        met = abs(collective_karma) > 5000

        return EventTriggerCondition(
            condition_type="karma_threshold",
            threshold=threshold_crossed or 0,
            comparison="crossed",
            met=met,
            current_value=collective_karma
        )

    @classmethod
    def _evaluate_time_since_last(
        cls,
        hours_since_last: float,
        online_players: int
    ) -> EventTriggerCondition:
        """Check if enough time has passed since last event"""
        # Determine frequency based on player count
        if online_players < 10:
            min_interval = cls.EVENT_FREQUENCY["very_low"]
        elif online_players < 50:
            min_interval = cls.EVENT_FREQUENCY["low"]
        elif online_players < 100:
            min_interval = cls.EVENT_FREQUENCY["medium"]
        elif online_players < 500:
            min_interval = cls.EVENT_FREQUENCY["high"]
        else:
            min_interval = cls.EVENT_FREQUENCY["very_high"]

        met = hours_since_last >= min_interval

        return EventTriggerCondition(
            condition_type="time_since_last_event",
            threshold=min_interval,
            comparison="greater_than",
            met=met,
            current_value=hours_since_last
        )

    @classmethod
    def _evaluate_action_ratio(
        cls,
        positive_actions: int,
        negative_actions: int,
        total_actions: int
    ) -> EventTriggerCondition:
        """Check if action ratio is extreme (very good or very bad)"""
        positive_ratio = positive_actions / total_actions if total_actions > 0 else 0.5

        # Trigger if ratio is extreme (>80% or <20%)
        met = positive_ratio > 0.8 or positive_ratio < 0.2

        return EventTriggerCondition(
            condition_type="positive_action_ratio",
            threshold=0.8 if positive_ratio > 0.5 else 0.2,
            comparison="extreme",
            met=met,
            current_value=positive_ratio
        )

    @classmethod
    def _evaluate_world_instability(
        cls,
        guild_wars: int,
        contested_territories: int
    ) -> EventTriggerCondition:
        """Check if world is highly unstable"""
        instability_score = guild_wars * 2 + contested_territories

        # Trigger if instability is high
        met = instability_score >= 5

        return EventTriggerCondition(
            condition_type="world_instability",
            threshold=5,
            comparison="greater_than",
            met=met,
            current_value=float(instability_score)
        )


class TriggerEvaluator:
    """Uses AI to intelligently evaluate when to trigger events"""

    def __init__(self):
        self.client = get_ai_client()
        logger.info("TriggerEvaluator initialized")

    async def should_trigger_event(
        self,
        world_state: WorldState,
        conditions: List[EventTriggerCondition]
    ) -> TriggerEvaluation:
        """
        Use AI to decide if an event should trigger now
        
        Considers all conditions plus narrative timing and player engagement
        """
        logger.info("Evaluating event trigger with AI")

        # Count how many conditions are met
        conditions_met_count = sum(1 for c in conditions if c.met)

        # Quick bypass: If no conditions met and recent event, don't trigger
        if conditions_met_count == 0 and world_state.time_since_last_event and world_state.time_since_last_event < 3:
            logger.info("No conditions met and recent event - skipping")
            return TriggerEvaluation(
                should_trigger=False,
                confidence=0.9,
                conditions_met=conditions,
                reasoning="No trigger conditions met and event triggered recently",
                urgency="low"
            )

        # Prepare conditions summary
        conditions_summary = self._format_conditions(conditions)
        trends_summary = self._analyze_trends(world_state)

        try:
            prompt = TRIGGER_EVALUATION_PROMPT.format(
                world_state=self._format_world_state(world_state),
                time_since_last=world_state.time_since_last_event or 0,
                trends=trends_summary
            )

            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": ARCHITECT_SYSTEM_PROMPT},
                    {"role": "user", "content": f"{prompt}\n\nConditions Status:\n{conditions_summary}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.6,  # Balanced creativity
                max_tokens=800
            )

            result = json.loads(response.choices[0].message.content)

            evaluation = TriggerEvaluation(
                should_trigger=result["should_trigger"],
                confidence=result["confidence"],
                event_type_suggestion=EventType(result["event_type_suggestion"]) if result.get(
                    "event_type_suggestion") else None,
                severity_suggestion=EventSeverity(
                    result.get("severity_suggestion", "medium")),
                conditions_met=conditions,
                reasoning=result["reasoning"],
                urgency=result.get("urgency", "normal")
            )

            logger.info(
                f"Trigger evaluation: {evaluation.should_trigger} "
                f"(confidence: {evaluation.confidence:.2f}, urgency: {evaluation.urgency})"
            )

            return evaluation

        except Exception as e:
            logger.error(f"Error in AI trigger evaluation: {e}")
            # Fallback to rule-based evaluation
            return self._fallback_evaluation(conditions, world_state)

    def _format_conditions(self, conditions: List[EventTriggerCondition]) -> str:
        """Format conditions for AI"""
        lines = []
        for i, cond in enumerate(conditions, 1):
            status = "✓ MET" if cond.met else "✗ NOT MET"
            lines.append(
                f"{i}. {cond.condition_type}: {status} "
                f"(current: {cond.current_value}, threshold: {cond.threshold})"
            )
        return "\n".join(lines)

    def _format_world_state(self, world_state: WorldState) -> str:
        """Format world state for AI"""
        return f"""
Collective Karma: {world_state.collective_karma:,.0f} (Trend: {world_state.karma_trend})
Players: {world_state.total_players:,} total, {world_state.online_players:,} online
Actions (24h): {world_state.total_actions_24h:,} total
  - Positive: {world_state.positive_actions_24h:,}
  - Negative: {world_state.negative_actions_24h:,}
Conflicts: {world_state.guild_wars_active} wars, {world_state.territories_contested} contested territories
Market Health: {world_state.market_health}
Last Event: {world_state.last_global_event or 'None'}
        """

    def _analyze_trends(self, world_state: WorldState) -> str:
        """Analyze trends for AI context"""
        trends = []

        # Karma trend analysis
        if world_state.karma_trend == "rising":
            trends.append(
                "Collective karma is improving - players are being more virtuous")
        elif world_state.karma_trend == "falling":
            trends.append(
                "Collective karma is declining - more negative actions occurring")
        else:
            trends.append("Karma is stable - balanced between good and evil")

        # Action analysis
        if world_state.total_actions_24h > 0:
            positive_ratio = world_state.positive_actions_24h / world_state.total_actions_24h
            if positive_ratio > 0.7:
                trends.append(
                    "Player base is predominantly helpful and positive")
            elif positive_ratio < 0.3:
                trends.append(
                    "Player base is predominantly selfish and negative")
            else:
                trends.append("Player actions are mixed between good and evil")

        # Conflict analysis
        if world_state.guild_wars_active > 0:
            trends.append(
                f"Active conflicts: {world_state.guild_wars_active} guild wars in progress")

        return "\n".join(trends)

    def _fallback_evaluation(self, conditions: List[EventTriggerCondition], world_state: WorldState) -> TriggerEvaluation:
        """Rule-based fallback if AI fails"""
        logger.warning("Using fallback rule-based trigger evaluation")

        conditions_met_count = sum(1 for c in conditions if c.met)

        # Simple rule: trigger if 2+ conditions met
        should_trigger = conditions_met_count >= 2

        # Suggest event type based on karma
        event_type = None
        if should_trigger:
            if world_state.collective_karma > 10000:
                event_type = EventType.GOLDEN_AGE
            elif world_state.collective_karma < -10000:
                event_type = EventType.JUDGMENT_DAY
            else:
                event_type = EventType.METEOR_SHOWER

        return TriggerEvaluation(
            should_trigger=should_trigger,
            confidence=0.7,
            event_type_suggestion=event_type,
            severity_suggestion=EventSeverity.MEDIUM,
            conditions_met=conditions,
            reasoning=f"Fallback evaluation: {conditions_met_count}/4 conditions met",
            urgency="normal"
        )
