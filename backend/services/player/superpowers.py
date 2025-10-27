from typing import Dict, List, Tuple
from backend.models.player.superpowers import (
    PlayerSuperpowers, SuperpowerDefinition, PowerTier
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# All 25 superpowers with their requirements
SUPERPOWER_DEFINITIONS = {
    # Tier 1 - Basic Powers
    "mind_reading": SuperpowerDefinition(
        power_id="mind_reading",
        name="Mind Reading",
        description="Know others' intentions",
        tier=PowerTier.TIER_1,
        requirements={"empathy": 80.0, "perception": 70.0},
        cooldown_seconds=180,
        energy_cost=30
    ),
    "enhanced_reflexes": SuperpowerDefinition(
        power_id="enhanced_reflexes",
        name="Enhanced Reflexes",
        description="Faster reactions",
        tier=PowerTier.TIER_1,
        requirements={"speed": 75.0, "dexterity": 70.0},
        cooldown_seconds=120,
        energy_cost=25
    ),
    "persuasion_aura": SuperpowerDefinition(
        power_id="persuasion_aura",
        name="Persuasion Aura",
        description="Influence emotions",
        tier=PowerTier.TIER_1,
        requirements={"charisma": 80.0, "negotiation": 75.0},
        cooldown_seconds=240,
        energy_cost=40
    ),
    "danger_sense": SuperpowerDefinition(
        power_id="danger_sense",
        name="Danger Sense",
        description="Detect threats",
        tier=PowerTier.TIER_1,
        requirements={"perception": 80.0, "survival_instinct": 70.0},
        cooldown_seconds=90,
        energy_cost=20
    ),
    "quick_heal": SuperpowerDefinition(
        power_id="quick_heal",
        name="Quick Heal",
        description="Fast recovery",
        tier=PowerTier.TIER_1,
        requirements={"medicine": 75.0, "resilience": 70.0},
        cooldown_seconds=300,
        energy_cost=50
    ),

    # Tier 2 - Intermediate Powers
    "telekinesis": SuperpowerDefinition(
        power_id="telekinesis",
        name="Telekinesis",
        description="Move objects with mind",
        tier=PowerTier.TIER_2,
        requirements={"meditation": 80.0, "intelligence": 75.0},
        cooldown_seconds=360,
        energy_cost=60
    ),
    "invisibility": SuperpowerDefinition(
        power_id="invisibility",
        name="Invisibility",
        description="Become unseen",
        tier=PowerTier.TIER_2,
        requirements={"stealth": 90.0, "patience": 70.0},
        cooldown_seconds=480,
        energy_cost=70
    ),
    "energy_shield": SuperpowerDefinition(
        power_id="energy_shield",
        name="Energy Shield",
        description="Protect from attacks",
        tier=PowerTier.TIER_2,
        requirements={"resilience": 85.0, "endurance": 80.0},
        cooldown_seconds=300,
        energy_cost=55
    ),
    "psychic_vision": SuperpowerDefinition(
        power_id="psychic_vision",
        name="Psychic Vision",
        description="See past events",
        tier=PowerTier.TIER_2,
        requirements={"meditation": 90.0, "perception": 85.0},
        cooldown_seconds=600,
        energy_cost=80
    ),
    "tech_control": SuperpowerDefinition(
        power_id="tech_control",
        name="Tech Control",
        description="Control electronics",
        tier=PowerTier.TIER_2,
        requirements={"hacking": 85.0, "technical_knowledge": 80.0},
        cooldown_seconds=240,
        energy_cost=45
    ),

    # Tier 3 - Advanced Powers
    "time_slow": SuperpowerDefinition(
        power_id="time_slow",
        name="Time Slow",
        description="Slow perceived time",
        tier=PowerTier.TIER_3,
        requirements={"focus": 85.0, "wisdom": 75.0},
        cooldown_seconds=720,
        energy_cost=100
    ),
    "healing_touch": SuperpowerDefinition(
        power_id="healing_touch",
        name="Healing Touch",
        description="Heal others",
        tier=PowerTier.TIER_3,
        requirements={"kindness": 85.0, "medicine": 80.0},
        cooldown_seconds=420,
        energy_cost=75
    ),
    "probability_manipulation": SuperpowerDefinition(
        power_id="probability_manipulation",
        name="Probability Manipulation",
        description="Alter outcomes slightly",
        tier=PowerTier.TIER_3,
        requirements={"vision": 90.0, "strategy": 85.0},
        cooldown_seconds=900,
        energy_cost=120
    ),
    "empathic_link": SuperpowerDefinition(
        power_id="empathic_link",
        name="Empathic Link",
        description="Share emotions",
        tier=PowerTier.TIER_3,
        requirements={"empathy": 90.0, "loveability": 80.0},
        cooldown_seconds=360,
        energy_cost=65
    ),
    "shadow_walk": SuperpowerDefinition(
        power_id="shadow_walk",
        name="Shadow Walk",
        description="Teleport short distances",
        tier=PowerTier.TIER_3,
        requirements={"stealth": 85.0, "speed": 80.0},
        cooldown_seconds=540,
        energy_cost=90
    ),

    # Tier 4 - Master Powers
    "charm_mastery": SuperpowerDefinition(
        power_id="charm_mastery",
        name="Charm Mastery",
        description="Control emotions",
        tier=PowerTier.TIER_4,
        requirements={"charisma": 90.0,
            "negotiation": 85.0, "manipulation": 70.0},
        cooldown_seconds=600,
        energy_cost=110
    ),
    "combat_supremacy": SuperpowerDefinition(
        power_id="combat_supremacy",
        name="Combat Supremacy",
        description="Enhanced fighting",
        tier=PowerTier.TIER_4,
        requirements={"physical_strength": 80.0,
            "dexterity": 80.0, "courage": 75.0},
        cooldown_seconds=480,
        energy_cost=95
    ),
    "memory_vault": SuperpowerDefinition(
        power_id="memory_vault",
        name="Memory Vault",
        description="Perfect recall",
        tier=PowerTier.TIER_4,
        requirements={"memory": 95.0, "focus": 90.0},
        cooldown_seconds=1200,
        energy_cost=150
    ),
    "future_glimpse": SuperpowerDefinition(
        power_id="future_glimpse",
        name="Future Glimpse",
        description="See potential outcomes",
        tier=PowerTier.TIER_4,
        requirements={"meditation": 95.0, "vision": 90.0, "wisdom": 85.0},
        cooldown_seconds=1800,
        energy_cost=200
    ),
    "reality_bend": SuperpowerDefinition(
        power_id="reality_bend",
        name="Reality Bend",
        description="Minor reality manipulation",
        tier=PowerTier.TIER_4,
        requirements={"enlightenment": 90.0, "karmic_balance": 85.0},
        cooldown_seconds=2400,
        energy_cost=250
    ),

    # Tier 5 - Legendary Powers
    "karmic_transfer": SuperpowerDefinition(
        power_id="karmic_transfer",
        name="Karmic Transfer",
        description="Give/take karma from others",
        tier=PowerTier.TIER_5,
        requirements={"divine_favor": 95.0, "wisdom": 90.0},
        cooldown_seconds=3600,
        energy_cost=300
    ),
    "soul_bond": SuperpowerDefinition(
        power_id="soul_bond",
        name="Soul Bond",
        description="Permanent connection with another",
        tier=PowerTier.TIER_5,
        requirements={"loveability": 95.0, "loyalty": 90.0},
        cooldown_seconds=0,  # One-time use
        energy_cost=500
    ),
    "temporal_echo": SuperpowerDefinition(
        power_id="temporal_echo",
        name="Temporal Echo",
        description="Rewind personal time 10 seconds",
        tier=PowerTier.TIER_5,
        requirements={"focus": 95.0, "wisdom": 95.0, "meditation": 90.0},
        cooldown_seconds=7200,
        energy_cost=400
    ),
    "omniscience": SuperpowerDefinition(
        power_id="omniscience",
        name="Omniscience",
        description="Brief complete awareness",
        tier=PowerTier.TIER_5,
        requirements={"intelligence": 90.0,
            "wisdom": 90.0, "perception": 90.0},
        cooldown_seconds=10800,
        energy_cost=500
    ),
    "ascension": SuperpowerDefinition(
        power_id="ascension",
        name="Ascension",
        description="Temporary god-like state",
        tier=PowerTier.TIER_5,
        requirements={
            "empathy": 95.0, "integrity": 95.0, "wisdom": 95.0,
            "kindness": 95.0, "courage": 95.0
        },
        cooldown_seconds=86400,  # 24 hours
        energy_cost=1000
    ),
}

class SuperpowerService:
    """Service for managing player superpowers"""

    @staticmethod
    def initialize_superpowers(player_id: str) -> PlayerSuperpowers:
        """Initialize superpowers for a new player"""
        return PlayerSuperpowers(player_id=player_id)

    @staticmethod
    def check_unlock_eligibility(
        player_traits: Dict[str, float],
        power_id: str
    ) -> Tuple[bool, str]:
        """Check if player meets requirements to unlock a power"""
        if power_id not in SUPERPOWER_DEFINITIONS:
            return False, "Invalid power ID"

        power_def = SUPERPOWER_DEFINITIONS[power_id]

        for trait, min_value in power_def.requirements.items():
            if trait not in player_traits or player_traits[trait] < min_value:
                return False, f"Requires {trait} >= {min_value}"

        return True, "Requirements met"

    @staticmethod
    def unlock_power(
        player_superpowers: PlayerSuperpowers,
        player_traits: Dict[str, float],
        power_id: str
    ) -> Tuple[bool, str]:
        """Unlock a superpower"""
        eligible, message = SuperpowerService.check_unlock_eligibility(
            player_traits, power_id)
        if not eligible:
            return False, message

        success = player_superpowers.unlock_power(power_id)
        if success:
            return True, "Superpower unlocked!"
        return False, "Power already unlocked"

    @staticmethod
    def use_power(
        player_superpowers: PlayerSuperpowers,
        power_id: str
    ) -> Tuple[bool, str, Dict]:
        """Use a superpower"""
        # Check if power is unlocked
        power = next(
            (p for p in player_superpowers.unlocked_powers if p.power_id == power_id), None)
        if not power:
            return False, "Power not unlocked", {}

        # Check if power is equipped
        if power_id not in player_superpowers.equipped_powers:
            return False, "Power not equipped", {}

        # Check cooldown
        if power.is_on_cooldown():
            remaining = (power.cooldown_until - \
                         datetime.utcnow()).total_seconds()
            return False, f"Power on cooldown ({int(remaining)}s remaining)", {}

        # Use the power
        power_def = SUPERPOWER_DEFINITIONS[power_id]
        power.use_power(power_def.cooldown_seconds)

        return True, "Power activated!", power_def.effects

    @staticmethod
    def get_available_powers(player_traits: Dict[str, float]) -> List[Dict]:
        """Get list of powers player can unlock"""
        available = []

        for power_id, power_def in SUPERPOWER_DEFINITIONS.items():
            eligible, message = SuperpowerService.check_unlock_eligibility(
                player_traits, power_id
            )
            available.append({
                "power_id": power_id,
                "name": power_def.name,
                "description": power_def.description,
                "tier": power_def.tier,
                "eligible": eligible,
                "requirements": power_def.requirements,
                "message": message
            })

        return available
