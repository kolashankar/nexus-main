"""Collective Consequences Service - Track and apply consequences of collective player behavior."""

from typing import Dict, List, Any
from datetime import datetime, timedelta
from backend.core.database import db
from backend.services.world.events import WorldEventsService


class CollectiveConsequencesService:
    """Service for managing consequences based on collective player behavior."""

    def __init__(self):
        self.db = db
        self.events_service = WorldEventsService()

    async def analyze_collective_behavior(self) -> Dict[str, Any]:
        """Analyze collective player behavior and determine consequences."""
        # Get world state
        world_state = await self.db.world_state.find_one()
        if not world_state:
            return {}

        # Analyze different aspects
        karma_analysis = await self._analyze_collective_karma()
        economic_analysis = await self._analyze_economic_behavior()
        social_analysis = await self._analyze_social_behavior()
        combat_analysis = await self._analyze_combat_behavior()

        # Determine consequences
        consequences = {
            "karma_based": await self._determine_karma_consequences(karma_analysis),
            "economic_based": await self._determine_economic_consequences(economic_analysis),
            "social_based": await self._determine_social_consequences(social_analysis),
            "combat_based": await self._determine_combat_consequences(combat_analysis)
        }

        # Apply consequences
        applied = await self._apply_consequences(consequences)

        return {
            "analysis": {
                "karma": karma_analysis,
                "economic": economic_analysis,
                "social": social_analysis,
                "combat": combat_analysis
            },
            "consequences": consequences,
            "applied": applied
        }

    async def _analyze_collective_karma(self) -> Dict[str, Any]:
        """Analyze collective karma trends."""
        # Get karma changes in last 24 hours
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

        pipeline = [
            {
                "$match": {
                    "timestamp": {"$gte": twenty_four_hours_ago}
                }
            },
            {
                "$group": {
                    "_id": None,
                    "total_karma_change": {"$sum": "$karma_change"},
                    "positive_actions": {
                        "$sum": {"$cond": [{"$gt": ["$karma_change", 0]}, 1, 0]}
                    },
                    "negative_actions": {
                        "$sum": {"$cond": [{"$lt": ["$karma_change", 0]}, 1, 0]}
                    },
                    "avg_karma_change": {"$avg": "$karma_change"}
                }
            }
        ]

        result = await self.db.actions.aggregate(pipeline).to_list(length=1)

        if not result:
            return {
                "trend": "neutral",
                "total_change": 0,
                "positive_ratio": 0.5
            }

        data = result[0]
        total_actions = data["positive_actions"] + data["negative_actions"]
        positive_ratio = data["positive_actions"] / \
            total_actions if total_actions > 0 else 0.5

        # Determine trend
        if positive_ratio > 0.7:
            trend = "very_positive"
        elif positive_ratio > 0.55:
            trend = "positive"
        elif positive_ratio < 0.3:
            trend = "very_negative"
        elif positive_ratio < 0.45:
            trend = "negative"
        else:
            trend = "neutral"

        return {
            "trend": trend,
            "total_change": data["total_karma_change"],
            "positive_ratio": positive_ratio,
            "avg_change": data["avg_karma_change"]
        }

    async def _analyze_economic_behavior(self) -> Dict[str, Any]:
        """Analyze collective economic behavior."""
        # Get average wealth
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "avg_wealth": {"$avg": "$currencies.credits"},
                    "median_wealth": {"$median": {"input": "$currencies.credits"}},
                    "total_wealth": {"$sum": "$currencies.credits"}
                }
            }
        ]

        result = await self.db.players.aggregate(pipeline).to_list(length=1)

        if not result:
            return {"trend": "stable", "avg_wealth": 0}

        data = result[0]

        return {
            "trend": "stable",  # Would need historical data for real trend
            "avg_wealth": data["avg_wealth"],
            "total_wealth": data["total_wealth"]
        }

    async def _analyze_social_behavior(self) -> Dict[str, Any]:
        """Analyze social interactions."""
        # Count guilds and alliances
        total_guilds = await self.db.guilds.count_documents({})
        active_wars = await self.db.guilds.count_documents({
            "active_wars": {"$exists": True, "$ne": []}
        })

        return {
            "total_guilds": total_guilds,
            "active_wars": active_wars,
            "cooperation_level": "moderate" if total_guilds > active_wars else "low"
        }

    async def _analyze_combat_behavior(self) -> Dict[str, Any]:
        """Analyze combat activity."""
        twenty_four_hours_ago = datetime.utcnow() - timedelta(hours=24)

        total_combats = await self.db.combat_sessions.count_documents({
            "created_at": {"$gte": twenty_four_hours_ago}
        })

        return {
            "combat_frequency": "high" if total_combats > 100 else "moderate" if total_combats > 20 else "low",
            "total_combats_24h": total_combats
        }

    async def _determine_karma_consequences(self, analysis: Dict[str, Any]) -> List[str]:
        """Determine karma-based consequences."""
        consequences = []

        trend = analysis["trend"]

        if trend == "very_positive":
            consequences.append("trigger_golden_age")
        elif trend == "positive":
            consequences.append("trigger_divine_blessing")
        elif trend == "very_negative":
            consequences.append("trigger_purge")
        elif trend == "negative":
            consequences.append("trigger_dark_eclipse")

        return consequences

    async def _determine_economic_consequences(self, analysis: Dict[str, Any]) -> List[str]:
        """Determine economic-based consequences."""
        consequences = []

        # Simple example - would be more complex in real implementation
        avg_wealth = analysis.get("avg_wealth", 0)

        if avg_wealth > 100000:
            consequences.append("economic_inflation")
        elif avg_wealth < 1000:
            consequences.append("economic_depression")

        return consequences

    async def _determine_social_consequences(self, analysis: Dict[str, Any]) -> List[str]:
        """Determine social-based consequences."""
        consequences = []

        active_wars = analysis.get("active_wars", 0)

        if active_wars > 5:
            consequences.append("world_conflict")
        elif active_wars == 0:
            consequences.append("peace_era")

        return consequences

    async def _determine_combat_consequences(self, analysis: Dict[str, Any]) -> List[str]:
        """Determine combat-based consequences."""
        consequences = []

        frequency = analysis.get("combat_frequency", "moderate")

        if frequency == "high":
            consequences.append("combat_fatigue")

        return consequences

    async def _apply_consequences(self, consequences: Dict[str, List[str]]) -> Dict[str, Any]:
        """Apply the determined consequences."""
        applied = {}

        # Apply karma-based consequences
        for consequence in consequences["karma_based"]:
            if consequence.startswith("trigger_"):
                event_type = consequence.replace("trigger_", "")
                try:
                    await self.events_service.trigger_event(event_type, {
                        "reason": "Collective karma consequence"
                    })
                    applied[consequence] = "success"
                except Exception as e:
                    applied[consequence] = f"failed: {str(e)}"

        # Apply other consequences (simplified for now)
        for category, consequence_list in consequences.items():
            if category != "karma_based":
                for consequence in consequence_list:
                    applied[consequence] = "logged"

        return applied

    async def get_consequence_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get history of collective consequences."""
        # This would retrieve from a consequences log collection
        # For now, return empty list
        return []
