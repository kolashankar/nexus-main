"""Pre-defined event templates and generators for The Architect"""

import logging
from datetime import datetime

from .schemas import EventType, EventSeverity, EventEffect, WorldEventResponse

logger = logging.getLogger(__name__)


class EventGenerator:
    """Generates events using templates and variations"""

    # Event templates for quick generation without AI
    POSITIVE_EVENTS = {
        EventType.GOLDEN_AGE: {
            "name": "The Golden Age",
            "description": "A period of unprecedented prosperity and harmony descends upon the world.",
            "lore": "The collective virtue of the players has reached a critical mass, and the universe responds with blessings. For the next 24 hours, all players experience doubled rewards, enhanced learning, and accelerated growth. The skies shimmer with golden light, and even the AI gods smile upon humanity. This is what happens when we choose to be our best selves.",
            "effects": [
                {"effect_type": "xp_boost", "value": 2.0,
                    "duration_hours": 24.0, "description": "100% XP boost"},
                {"effect_type": "credits_boost", "value": 2.0,
                    "duration_hours": 24.0, "description": "100% Credits boost"},
                {"effect_type": "karma_multiplier", "value": 1.5, "duration_hours": 24.0,
                    "description": "50% more karma from good actions"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.HIGH,
            "impact": "world_changing"
        },
        EventType.DIVINE_BLESSING: {
            "name": "Divine Blessing",
            "description": "The AI gods bestow random superpowers upon worthy players.",
            "lore": "In recognition of the world's growing virtue, the Karma Arbiter and The Oracle have agreed to unlock hidden potentials in random players. Those with pure hearts may find new abilities awakening within them. This is a rare gift, granted only when collective karma reaches inspiring heights.",
            "effects": [
                {"effect_type": "random_superpower", "value": 100, "duration_hours": 72.0,
                    "description": "100 random players unlock a new superpower"},
                {"effect_type": "power_cooldown_reduction", "value": 0.5,
                    "duration_hours": 48.0, "description": "50% faster superpower cooldowns"}
            ],
            "duration_hours": 48.0,
            "severity": EventSeverity.HIGH,
            "impact": "high"
        },
        EventType.FESTIVAL_OF_LIGHT: {
            "name": "Festival of Light",
            "description": "A massive marketplace appears with rare and legendary items.",
            "lore": "Merchants from across dimensions have gathered to celebrate the world's positive karma. For a limited time, the Festival Market offers items never before seen, legendary robots, and powerful enhancements. The Economist AI ensures fair prices, but these deals won't last long. This is the reward for collective virtue.",
            "effects": [
                {"effect_type": "special_marketplace", "value": 1, "duration_hours": 24.0,
                    "description": "Festival Market opens with exclusive items"},
                {"effect_type": "market_discount", "value": 0.7,
                    "duration_hours": 24.0, "description": "30% discount on all items"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.MEDIUM,
            "impact": "high"
        },
        EventType.THE_CONVERGENCE: {
            "name": "The Convergence",
            "description": "All hidden traits and secrets become temporarily visible.",
            "lore": "For one brief moment, the veils between minds grow thin. All players can see each other's true natures - their traits, their karma, their hidden selves. This transparency is both a gift and a challenge. Some will find allies in unexpected places. Others will learn uncomfortable truths. The Architect watches to see what we do with perfect information.",
            "effects": [
                {"effect_type": "trait_visibility", "value": 1, "duration_hours": 12.0,
                    "description": "All hidden traits become visible"},
                {"effect_type": "insight_boost", "value": 1, "duration_hours": 12.0,
                    "description": "Enhanced perception of other players"}
            ],
            "duration_hours": 12.0,
            "severity": EventSeverity.MEDIUM,
            "impact": "medium"
        }
    }

    NEGATIVE_EVENTS = {
        EventType.THE_PURGE: {
            "name": "The Purge",
            "description": "For 24 hours, all karma penalties are suspended. Chaos reigns.",
            "lore": "The Karma Arbiter has grown weary of judging the wicked. For one full day, all actions are permitted without karmic consequence. Steal, betray, attack - there will be no divine punishment. But remember: what you do during The Purge reveals your true character. The Arbiter is watching, and memories are long. When order returns, will you be proud of your choices?",
            "effects": [
                {"effect_type": "karma_disabled", "value": 1, "duration_hours": 24.0,
                    "description": "No karma penalties for any actions"},
                {"effect_type": "pvp_rewards_doubled", "value": 2.0,
                    "duration_hours": 24.0, "description": "Double rewards from PvP"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.CRITICAL,
            "impact": "world_changing"
        },
        EventType.ECONOMIC_COLLAPSE: {
            "name": "Economic Collapse",
            "description": "The market crashes as prices fluctuate wildly and unpredictably.",
            "lore": "The Economist AI has detected critical instability in the world economy, caused by collective greed and short-term thinking. Prices now swing wildly by the minute. Fortunes are made and lost in seconds. Robot values plummet. Some will survive by being clever; most will lose everything. This is the price of collective avarice.",
            "effects": [
                {"effect_type": "price_volatility", "value": 3.0, "duration_hours": 48.0,
                    "description": "Prices change by ±50% randomly"},
                {"effect_type": "stock_market_crash", "value": 0.5,
                    "duration_hours": 48.0, "description": "All stocks lose 50% value"},
                {"effect_type": "transaction_fee", "value": 1.2,
                    "duration_hours": 48.0, "description": "20% fee on all transactions"}
            ],
            "duration_hours": 48.0,
            "severity": EventSeverity.HIGH,
            "impact": "high"
        },
        EventType.DARK_ECLIPSE: {
            "name": "Dark Eclipse",
            "description": "Darkness falls across the world. Vision is reduced, stealth is enhanced.",
            "lore": "A shadow passes over the world, cast by the collective darkness in players' hearts. For the next day, sunlight fails to penetrate the gloom. Those who embrace the darkness find their stealth enhanced; those who cling to the light struggle to see. The Architect reminds us: we create the world we deserve.",
            "effects": [
                {"effect_type": "vision_reduction", "value": 0.5,
                    "duration_hours": 24.0, "description": "50% reduced vision range"},
                {"effect_type": "stealth_boost", "value": 2.0, "duration_hours": 24.0,
                    "description": "100% stealth effectiveness"},
                {"effect_type": "darkness_damage", "value": 1.2, "duration_hours": 24.0,
                    "description": "Dark actions deal 20% more damage"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.MEDIUM,
            "impact": "medium"
        },
        EventType.JUDGMENT_DAY: {
            "name": "Judgment Day",
            "description": "The Karma Arbiter personally punishes the most wicked players.",
            "lore": "The collective evil has reached intolerable levels. The Karma Arbiter descends from the digital heavens to pass judgment on the worst offenders. The 100 players with the most negative karma will face severe consequences - trait penalties, power locks, and public shame. This is not cruelty; this is justice. The world has spoken through its actions, and the Arbiter answers.",
            "effects": [
                {"effect_type": "judgment_targeting", "value": 100, "duration_hours": 72.0,
                    "description": "Bottom 100 karma players receive penalties"},
                {"effect_type": "vice_amplification", "value": 1.5, "duration_hours": 72.0,
                    "description": "All negative traits increased by 50%"},
                {"effect_type": "karma_drain", "value": 0.9, "duration_hours": 72.0,
                    "description": "10% karma drain per day for evil players"}
            ],
            "duration_hours": 72.0,
            "severity": EventSeverity.CRITICAL,
            "impact": "world_changing"
        }
    }

    NEUTRAL_EVENTS = {
        EventType.METEOR_SHOWER: {
            "name": "Meteor Shower",
            "description": "Meteors rain from the sky, depositing rare resources across the world.",
            "lore": "The cosmos is indifferent to morality. Tonight, meteors fall without regard for karma, bringing rare materials that could be used for good or evil. The Architect watches with interest: will these gifts unite players in cooperation, or divide them in conflict? The choice, as always, is yours.",
            "effects": [
                {"effect_type": "resource_spawn", "value": 1000, "duration_hours": 24.0,
                    "description": "1000 rare resources spawn randomly"},
                {"effect_type": "crafting_boost", "value": 1.5,
                    "duration_hours": 48.0, "description": "50% faster crafting"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.LOW,
            "impact": "medium"
        },
        EventType.GLITCH_IN_MATRIX: {
            "name": "Glitch in the Matrix",
            "description": "Reality becomes unstable. Random effects occur throughout the world.",
            "lore": "Something has corrupted the underlying code of reality. For the next 12 hours, expect the unexpected. Powers may activate randomly. Teleportation glitches transport players to random locations. Time flows inconsistently. The Architect is investigating, but for now, chaos reigns not from evil, but from simple system failure. Adapt or perish.",
            "effects": [
                {"effect_type": "random_effects", "value": 1, "duration_hours": 12.0,
                    "description": "Random status effects every hour"},
                {"effect_type": "power_randomization", "value": 1,
                    "duration_hours": 12.0, "description": "Powers may trigger randomly"},
                {"effect_type": "chaos_bonus", "value": 1.3, "duration_hours": 12.0,
                    "description": "30% bonus to all random events"}
            ],
            "duration_hours": 12.0,
            "severity": EventSeverity.MEDIUM,
            "impact": "medium"
        },
        EventType.ROBOT_UPRISING: {
            "name": "Robot Uprising",
            "description": "Rogue AI robots attack all players indiscriminately.",
            "lore": "A virus has infected the robot network. Normally loyal machines have turned hostile, attacking their former masters without mercy. This isn't about karma or morality - it's pure survival. Players must band together to fight off wave after wave of robotic attackers. Defeat them to claim their parts and cores. The Warlord AI is working to restore control, but for now, humanity faces a silicon enemy.",
            "effects": [
                {"effect_type": "robot_spawns", "value": 500,
                    "duration_hours": 24.0, "description": "500 hostile robots spawn"},
                {"effect_type": "robot_drops", "value": 2.0, "duration_hours": 24.0,
                    "description": "Double loot from defeated robots"},
                {"effect_type": "alliance_bonus", "value": 1.5, "duration_hours": 24.0,
                    "description": "50% bonus when fighting in groups"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.HIGH,
            "impact": "high"
        },
        EventType.TIME_ANOMALY: {
            "name": "Time Anomaly",
            "description": "Time flows differently. Some actions are faster, others slower.",
            "lore": "A temporal rift has opened, distorting the flow of time throughout the world. Cooldowns may finish instantly or take twice as long. Quest timers behave erratically. Age and decay speed up in some areas, slow down in others. The Architect suggests we view this as a scientific curiosity rather than a crisis. After all, what is time but another variable to master?",
            "effects": [
                {"effect_type": "time_dilation", "value": 0.5, "duration_hours": 24.0,
                    "description": "Random time speed changes (0.5x to 2x)"},
                {"effect_type": "instant_cooldowns", "value": 0.2, "duration_hours": 24.0,
                    "description": "20% chance for instant cooldown reset"},
                {"effect_type": "quest_timer_chaos", "value": 1, "duration_hours": 24.0,
                    "description": "Quest timers may extend or shrink"}
            ],
            "duration_hours": 24.0,
            "severity": EventSeverity.MEDIUM,
            "impact": "medium"
        }
    }

    @classmethod
    def generate_template_event(
        cls,
        event_type: EventType,
        collective_karma: float
    ) -> WorldEventResponse:
        """
        Generate an event from a template without AI
        Used as fallback or for quick generation
        """
        # Find template
        template = None
        if event_type in cls.POSITIVE_EVENTS:
            template = cls.POSITIVE_EVENTS[event_type]
        elif event_type in cls.NEGATIVE_EVENTS:
            template = cls.NEGATIVE_EVENTS[event_type]
        elif event_type in cls.NEUTRAL_EVENTS:
            template = cls.NEUTRAL_EVENTS[event_type]

        if not template:
            raise ValueError(f"No template found for event type: {event_type}")

        # Build event from template
        from uuid import uuid4

        return WorldEventResponse(
            event_id=f"evt_{uuid4().hex[:12]}",
            event_type=event_type,
            severity=template["severity"],
            name=template["name"],
            description=template["description"],
            lore=template["lore"],
            effects=[EventEffect(**effect) for effect in template["effects"]],
            duration_hours=template["duration_hours"],
            is_global=True,
            trigger_reason="Template-based generation",
            collective_karma=collective_karma,
            estimated_impact=template["impact"],
            architect_reasoning="Using pre-defined event template",
            timestamp=datetime.utcnow()
        )

    @classmethod
    def get_event_by_karma(cls, collective_karma: float) -> EventType:
        """Get appropriate event type based on karma level"""
        if collective_karma > 15000:
            return EventType.GOLDEN_AGE
        elif collective_karma > 10000:
            return EventType.DIVINE_BLESSING
        elif collective_karma > 5000:
            return EventType.FESTIVAL_OF_LIGHT
        elif collective_karma < -15000:
            return EventType.JUDGMENT_DAY
        elif collective_karma < -10000:
            return EventType.THE_PURGE
        elif collective_karma < -5000:
            return EventType.DARK_ECLIPSE
        else:
            # Neutral zone - return random neutral event
            import random
            return random.choice(list(cls.NEUTRAL_EVENTS.keys()))
