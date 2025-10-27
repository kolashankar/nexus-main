"""Superpower Definitions for all 25 Powers across 5 Tiers.

Each superpower has unlock conditions based on traits.
"""

from typing import Dict, List, Any
from enum import Enum

class SuperpowerTier(Enum):
    TIER_1 = 1  # Basic
    TIER_2 = 2  # Intermediate
    TIER_3 = 3  # Advanced
    TIER_4 = 4  # Master
    TIER_5 = 5  # Legendary

ALL_SUPERPOWERS: List[Dict[str, Any]] = [
    # TIER 1 - Basic Powers (Unlock Early)
    {
        "id": "mind_reading",
        "name": "Mind Reading",
        "description": "Know others' intentions and surface thoughts",
        "tier": SuperpowerTier.TIER_1.value,
        "unlock_conditions": {
            "empathy": 80,
            "perception": 70
        },
        "cooldown": 30,
        "duration": 10,
        "effects": {
            "reveal_intentions": True,
            "see_hidden_quests": True,
            "bonus_negotiation": 0.2
        },
        "cost": {"karma_tokens": 50}
    },
    {
        "id": "enhanced_reflexes",
        "name": "Enhanced Reflexes",
        "description": "Faster reactions and movement speed",
        "tier": SuperpowerTier.TIER_1.value,
        "unlock_conditions": {
            "speed": 75,
            "dexterity": 70
        },
        "cooldown": 45,
        "duration": 15,
        "effects": {
            "speed_multiplier": 1.5,
            "dodge_chance": 0.3,
            "attack_speed": 0.25
        },
        "cost": {"karma_tokens": 50}
    },
    {
        "id": "persuasion_aura",
        "name": "Persuasion Aura",
        "description": "Influence emotions and decisions of nearby players",
        "tier": SuperpowerTier.TIER_1.value,
        "unlock_conditions": {
            "charisma": 80,
            "negotiation": 75
        },
        "cooldown": 60,
        "duration": 20,
        "effects": {
            "persuasion_bonus": 0.4,
            "trade_discount": 0.15,
            "influence_radius": 20
        },
        "cost": {"karma_tokens": 50}
    },
    {
        "id": "danger_sense",
        "name": "Danger Sense",
        "description": "Detect threats and ambushes before they happen",
        "tier": SuperpowerTier.TIER_1.value,
        "unlock_conditions": {
            "perception": 80,
            "survival_instinct": 70
        },
        "cooldown": 90,
        "duration": 30,
        "effects": {
            "detect_ambush": True,
            "threat_indicator": True,
            "evasion_bonus": 0.25
        },
        "cost": {"karma_tokens": 50}
    },
    {
        "id": "quick_heal",
        "name": "Quick Heal",
        "description": "Rapidly recover health over short period",
        "tier": SuperpowerTier.TIER_1.value,
        "unlock_conditions": {
            "medicine": 75,
            "resilience": 70
        },
        "cooldown": 120,
        "duration": 10,
        "effects": {
            "heal_amount": 50,
            "heal_over_time": 5,
            "remove_minor_debuffs": True
        },
        "cost": {"karma_tokens": 50}
    },

    # TIER 2 - Intermediate Powers
    {
        "id": "telekinesis",
        "name": "Telekinesis",
        "description": "Move objects with mind, unlock doors, disable traps",
        "tier": SuperpowerTier.TIER_2.value,
        "unlock_conditions": {
            "meditation": 80,
            "intelligence": 75
        },
        "cooldown": 60,
        "duration": 15,
        "effects": {
            "move_objects": True,
            "unlock_doors": True,
            "disable_traps": True,
            "throw_damage": 30
        },
        "cost": {"karma_tokens": 100}
    },
    {
        "id": "invisibility",
        "name": "Invisibility",
        "description": "Become completely unseen for short duration",
        "tier": SuperpowerTier.TIER_2.value,
        "unlock_conditions": {
            "stealth": 90,
            "patience": 70
        },
        "cooldown": 180,
        "duration": 20,
        "effects": {
            "invisible": True,
            "mute_sounds": True,
            "break_on_attack": True
        },
        "cost": {"karma_tokens": 100}
    },
    {
        "id": "energy_shield",
        "name": "Energy Shield",
        "description": "Create protective barrier absorbing damage",
        "tier": SuperpowerTier.TIER_2.value,
        "unlock_conditions": {
            "resilience": 85,
            "endurance": 80
        },
        "cooldown": 120,
        "duration": 15,
        "effects": {
            "shield_hp": 100,
            "damage_reflection": 0.2,
            "status_immunity": True
        },
        "cost": {"karma_tokens": 100}
    },
    {
        "id": "psychic_vision",
        "name": "Psychic Vision",
        "description": "See past events and hidden information",
        "tier": SuperpowerTier.TIER_2.value,
        "unlock_conditions": {
            "meditation": 90,
            "perception": 85
        },
        "cooldown": 300,
        "duration": 30,
        "effects": {
            "see_history": True,
            "reveal_secrets": True,
            "find_hidden_items": True
        },
        "cost": {"karma_tokens": 100}
    },
    {
        "id": "tech_control",
        "name": "Tech Control",
        "description": "Control electronic devices and robots remotely",
        "tier": SuperpowerTier.TIER_2.value,
        "unlock_conditions": {
            "hacking": 85,
            "technical_knowledge": 80
        },
        "cooldown": 90,
        "duration": 25,
        "effects": {
            "hack_devices": True,
            "control_robots": True,
            "disable_security": True
        },
        "cost": {"karma_tokens": 100}
    },

    # TIER 3 - Advanced Powers
    {
        "id": "time_slow",
        "name": "Time Slow",
        "description": "Slow perceived time for tactical advantage",
        "tier": SuperpowerTier.TIER_3.value,
        "unlock_conditions": {
            "focus": 85,
            "wisdom": 75
        },
        "cooldown": 180,
        "duration": 10,
        "effects": {
            "time_dilation": 0.5,
            "action_points_bonus": 2,
            "perfect_accuracy": True
        },
        "cost": {"karma_tokens": 200}
    },
    {
        "id": "healing_touch",
        "name": "Healing Touch",
        "description": "Instantly heal others and remove all debuffs",
        "tier": SuperpowerTier.TIER_3.value,
        "unlock_conditions": {
            "kindness": 85,
            "medicine": 80
        },
        "cooldown": 120,
        "duration": 0,
        "effects": {
            "heal_amount": 100,
            "remove_all_debuffs": True,
            "grant_regen": 10
        },
        "cost": {"karma_tokens": 200}
    },
    {
        "id": "probability_manipulation",
        "name": "Probability Manipulation",
        "description": "Alter outcomes slightly in your favor",
        "tier": SuperpowerTier.TIER_3.value,
        "unlock_conditions": {
            "vision": 90,
            "strategy": 85
        },
        "cooldown": 300,
        "duration": 60,
        "effects": {
            "luck_bonus": 0.3,
            "crit_chance": 0.25,
            "loot_quality": 0.4
        },
        "cost": {"karma_tokens": 200}
    },
    {
        "id": "empathic_link",
        "name": "Empathic Link",
        "description": "Share emotions and buffs with ally",
        "tier": SuperpowerTier.TIER_3.value,
        "unlock_conditions": {
            "empathy": 90,
            "loveability": 80
        },
        "cooldown": 180,
        "duration": 120,
        "effects": {
            "share_buffs": True,
            "share_healing": 0.5,
            "damage_split": 0.3
        },
        "cost": {"karma_tokens": 200}
    },
    {
        "id": "shadow_walk",
        "name": "Shadow Walk",
        "description": "Teleport short distances through shadows",
        "tier": SuperpowerTier.TIER_3.value,
        "unlock_conditions": {
            "stealth": 85,
            "speed": 80
        },
        "cooldown": 45,
        "duration": 0,
        "effects": {
            "teleport_range": 30,
            "leave_no_trace": True,
            "surprise_bonus": 0.5
        },
        "cost": {"karma_tokens": 200}
    },

    # TIER 4 - Master Powers
    {
        "id": "charm_mastery",
        "name": "Charm Mastery",
        "description": "Control emotions and force compliance",
        "tier": SuperpowerTier.TIER_4.value,
        "unlock_conditions": {
            "charisma": 90,
            "negotiation": 85,
            "manipulation": 70
        },
        "cooldown": 240,
        "duration": 60,
        "effects": {
            "charm_npcs": True,
            "force_trade": True,
            "instant_alliance": True
        },
        "cost": {"karma_tokens": 300, "dark_matter": 50}
    },
    {
        "id": "combat_supremacy",
        "name": "Combat Supremacy",
        "description": "Massively enhanced fighting abilities",
        "tier": SuperpowerTier.TIER_4.value,
        "unlock_conditions": {
            "physical_strength": 80,
            "dexterity": 80,
            "courage": 75
        },
        "cooldown": 300,
        "duration": 30,
        "effects": {
            "damage_multiplier": 2.0,
            "armor_penetration": 0.5,
            "unstoppable": True
        },
        "cost": {"karma_tokens": 300}
    },
    {
        "id": "memory_vault",
        "name": "Memory Vault",
        "description": "Perfect recall of all seen information",
        "tier": SuperpowerTier.TIER_4.value,
        "unlock_conditions": {
            "memory": 95,
            "focus": 90
        },
        "cooldown": 600,
        "duration": 300,
        "effects": {
            "perfect_recall": True,
            "copy_skills": True,
            "learn_faster": 0.5
        },
        "cost": {"karma_tokens": 300}
    },
    {
        "id": "future_glimpse",
        "name": "Future Glimpse",
        "description": "See potential outcomes before they happen",
        "tier": SuperpowerTier.TIER_4.value,
        "unlock_conditions": {
            "meditation": 95,
            "vision": 90,
            "wisdom": 85
        },
        "cooldown": 900,
        "duration": 30,
        "effects": {
            "see_outcomes": 3,
            "avoid_death": True,
            "perfect_strategy": True
        },
        "cost": {"karma_tokens": 300}
    },
    {
        "id": "reality_bend",
        "name": "Reality Bend",
        "description": "Minor reality manipulation for brief moments",
        "tier": SuperpowerTier.TIER_4.value,
        "unlock_conditions": {
            "enlightenment": 90,
            "karmic_balance": 85
        },
        "cooldown": 1800,
        "duration": 10,
        "effects": {
            "rewrite_event": True,
            "create_item": True,
            "alter_terrain": True
        },
        "cost": {"karma_tokens": 300, "prestige_points": 100}
    },

    # TIER 5 - Legendary Powers (Very Rare)
    {
        "id": "karmic_transfer",
        "name": "Karmic Transfer",
        "description": "Give or take karma from other players",
        "tier": SuperpowerTier.TIER_5.value,
        "unlock_conditions": {
            "divine_favor": 95,
            "wisdom": 90
        },
        "cooldown": 1800,
        "duration": 0,
        "effects": {
            "transfer_amount": 100,
            "steal_karma": True,
            "gift_karma": True
        },
        "cost": {"karma_tokens": 500, "prestige_points": 200}
    },
    {
        "id": "soul_bond",
        "name": "Soul Bond",
        "description": "Permanent connection with another player",
        "tier": SuperpowerTier.TIER_5.value,
        "unlock_conditions": {
            "loveability": 95,
            "loyalty": 90
        },
        "cooldown": 0,  # Once per character
        "duration": -1,  # Permanent
        "effects": {
            "share_all_buffs": True,
            "resurrect_partner": True,
            "telepathy": True
        },
        "cost": {"karma_tokens": 1000}
    },
    {
        "id": "temporal_echo",
        "name": "Temporal Echo",
        "description": "Rewind personal time by 10 seconds",
        "tier": SuperpowerTier.TIER_5.value,
        "unlock_conditions": {
            "focus": 95,
            "wisdom": 90,
            "meditation": 90
        },
        "cooldown": 3600,  # 1 hour
        "duration": 0,
        "effects": {
            "rewind_time": 10,
            "keep_knowledge": True,
            "undo_death": True
        },
        "cost": {"karma_tokens": 500, "prestige_points": 300}
    },
    {
        "id": "omniscience",
        "name": "Omniscience",
        "description": "Brief complete awareness of everything",
        "tier": SuperpowerTier.TIER_5.value,
        "unlock_conditions": {
            "intelligence": 90,
            "wisdom": 90,
            "perception": 90,
            "meditation": 90
        },
        "cooldown": 7200,  # 2 hours
        "duration": 5,
        "effects": {
            "see_all_players": True,
            "see_all_events": True,
            "see_all_secrets": True
        },
        "cost": {"karma_tokens": 1000, "prestige_points": 500}
    },
    {
        "id": "ascension",
        "name": "Ascension",
        "description": "Temporary god-like state with immense power",
        "tier": SuperpowerTier.TIER_5.value,
        "unlock_conditions": {
            "all_virtues": 95,  # All 20 virtues > 95
            "karma_points": 5000
        },
        "cooldown": 86400,  # 24 hours
        "duration": 60,
        "effects": {
            "invulnerable": True,
            "unlimited_power": True,
            "reality_control": True,
            "grant_blessings": True
        },
        "cost": {"karma_tokens": 2000, "prestige_points": 1000}
    }
]

def get_superpower_by_id(power_id: str) -> Dict[str, Any]:
    """Get superpower definition by ID."""
    for power in ALL_SUPERPOWERS:
        if power["id"] == power_id:
            return power
    return None

def get_superpowers_by_tier(tier: int) -> List[Dict[str, Any]]:
    """Get all superpowers in a specific tier."""
    return [p for p in ALL_SUPERPOWERS if p["tier"] == tier]

def check_unlock_conditions(player_traits: Dict[str, float], power_id: str) -> bool:
    """Check if player meets unlock conditions for a power."""
    power = get_superpower_by_id(power_id)
    if not power:
        return False

    conditions = power["unlock_conditions"]

    # Check all_virtues special condition
    if "all_virtues" in conditions:
        virtues = [
            "empathy", "integrity", "discipline", "creativity", "resilience",
            "curiosity", "kindness", "courage", "patience", "adaptability",
            "wisdom", "humility", "vision", "honesty", "loyalty",
            "generosity", "self_awareness", "gratitude", "optimism", "loveability"
        ]
        min_value = conditions["all_virtues"]
        if not all(player_traits.get(v, 0) >= min_value for v in virtues):
            return False

    # Check individual trait conditions
    for trait, min_value in conditions.items():
        if trait == "all_virtues":
            continue
        if player_traits.get(trait, 0) < min_value:
            return False

    return True
