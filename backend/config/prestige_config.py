"""Prestige System Configuration.

Defines 10 prestige levels with bonuses and requirements.
"""

from typing import Dict, List, Any

PRESTIGE_LEVELS: List[Dict[str, Any]] = [
    {
        "level": 1,
        "name": "Ascended I",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 1000,
            "achievements_required": 20
        },
        "reset_effects": {
            "keep_percentage": 0.10,  # Keep 10% of all traits
            "reset_currencies": ["credits"],
            "keep_currencies": ["karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": False,
            "reset_level": True
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.10,  # +10% XP gain
            "karma_multiplier": 1.10,  # +10% karma gain
            "credits_multiplier": 1.10,  # +10% credits gain
            "trait_growth": 1.05  # +5% faster trait growth
        },
        "prestige_points_awarded": 100,
        "unlocks": [
            "prestige_shop_access",
            "prestige_title"
        ]
    },
    {
        "level": 2,
        "name": "Ascended II",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 2000,
            "achievements_required": 40
        },
        "reset_effects": {
            "keep_percentage": 0.15,
            "reset_currencies": ["credits"],
            "keep_currencies": ["karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": False,
            "reset_level": True
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.20,
            "karma_multiplier": 1.20,
            "credits_multiplier": 1.20,
            "trait_growth": 1.10
        },
        "prestige_points_awarded": 200,
        "unlocks": [
            "prestige_cosmetic_tier_1",
            "fast_travel"
        ]
    },
    {
        "level": 3,
        "name": "Transcended I",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 3000,
            "achievements_required": 60
        },
        "reset_effects": {
            "keep_percentage": 0.20,
            "reset_currencies": ["credits"],
            "keep_currencies": ["karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,  # Start keeping powers
            "reset_level": True
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.30,
            "karma_multiplier": 1.30,
            "credits_multiplier": 1.30,
            "trait_growth": 1.15,
            "superpower_cooldown_reduction": 0.10  # -10% cooldowns
        },
        "prestige_points_awarded": 300,
        "unlocks": [
            "prestige_cosmetic_tier_2",
            "double_daily_quests"
        ]
    },
    {
        "level": 4,
        "name": "Transcended II",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 4000,
            "achievements_required": 80
        },
        "reset_effects": {
            "keep_percentage": 0.25,
            "reset_currencies": [],  # Don't reset credits
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": True
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.40,
            "karma_multiplier": 1.40,
            "credits_multiplier": 1.40,
            "trait_growth": 1.20,
            "superpower_cooldown_reduction": 0.15
        },
        "prestige_points_awarded": 400,
        "unlocks": [
            "prestige_cosmetic_tier_3",
            "skill_tree_respec"
        ]
    },
    {
        "level": 5,
        "name": "Enlightened I",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 5000,
            "achievements_required": 100
        },
        "reset_effects": {
            "keep_percentage": 0.30,
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False  # Don't reset level anymore
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.50,
            "karma_multiplier": 1.50,
            "credits_multiplier": 1.50,
            "trait_growth": 1.25,
            "superpower_cooldown_reduction": 0.20,
            "robot_efficiency": 1.20
        },
        "prestige_points_awarded": 500,
        "unlocks": [
            "prestige_exclusive_power",
            "mentor_bonus"
        ]
    },
    {
        "level": 6,
        "name": "Enlightened II",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 6000,
            "achievements_required": 120
        },
        "reset_effects": {
            "keep_percentage": 0.35,
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.60,
            "karma_multiplier": 1.60,
            "credits_multiplier": 1.60,
            "trait_growth": 1.30,
            "superpower_cooldown_reduction": 0.25,
            "robot_efficiency": 1.25,
            "guild_bonus": 1.15
        },
        "prestige_points_awarded": 600,
        "unlocks": [
            "prestige_cosmetic_tier_4",
            "instant_quest_completion"
        ]
    },
    {
        "level": 7,
        "name": "Eternal I",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 7000,
            "achievements_required": 140
        },
        "reset_effects": {
            "keep_percentage": 0.40,
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.70,
            "karma_multiplier": 1.70,
            "credits_multiplier": 1.70,
            "trait_growth": 1.35,
            "superpower_cooldown_reduction": 0.30,
            "robot_efficiency": 1.30,
            "guild_bonus": 1.20,
            "pvp_damage": 1.15
        },
        "prestige_points_awarded": 700,
        "unlocks": [
            "prestige_exclusive_quest_line",
            "legacy_trait_transfer"
        ]
    },
    {
        "level": 8,
        "name": "Eternal II",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 8000,
            "achievements_required": 160
        },
        "reset_effects": {
            "keep_percentage": 0.45,
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.80,
            "karma_multiplier": 1.80,
            "credits_multiplier": 1.80,
            "trait_growth": 1.40,
            "superpower_cooldown_reduction": 0.35,
            "robot_efficiency": 1.35,
            "guild_bonus": 1.25,
            "pvp_damage": 1.20
        },
        "prestige_points_awarded": 800,
        "unlocks": [
            "prestige_cosmetic_tier_5",
            "auto_skill_tree_unlock"
        ]
    },
    {
        "level": 9,
        "name": "Divine I",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 9000,
            "achievements_required": 180
        },
        "reset_effects": {
            "keep_percentage": 0.50,
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False
        },
        "permanent_bonuses": {
            "xp_multiplier": 1.90,
            "karma_multiplier": 1.90,
            "credits_multiplier": 1.90,
            "trait_growth": 1.45,
            "superpower_cooldown_reduction": 0.40,
            "robot_efficiency": 1.40,
            "guild_bonus": 1.30,
            "pvp_damage": 1.25,
            "quest_rewards": 1.50
        },
        "prestige_points_awarded": 900,
        "unlocks": [
            "divine_intervention",
            "reality_manipulation"
        ]
    },
    {
        "level": 10,
        "name": "Divine II - Transcendent",
        "requirements": {
            "min_player_level": 100,
            "karma_threshold": 10000,
            "achievements_required": 200
        },
        "reset_effects": {
            "keep_percentage": 0.60,  # Keep 60% of traits
            "reset_currencies": [],
            "keep_currencies": ["credits", "karma_tokens", "dark_matter", "legacy_shards"],
            "keep_achievements": True,
            "keep_superpowers": True,
            "reset_level": False
        },
        "permanent_bonuses": {
            "xp_multiplier": 2.00,  # Double XP
            "karma_multiplier": 2.00,  # Double Karma
            "credits_multiplier": 2.00,  # Double Credits
            "trait_growth": 1.50,  # +50% trait growth
            "superpower_cooldown_reduction": 0.50,  # Half cooldowns
            "robot_efficiency": 1.50,
            "guild_bonus": 1.50,
            "pvp_damage": 1.50,
            "quest_rewards": 2.00,
            "legendary_drop_rate": 0.50
        },
        "prestige_points_awarded": 1000,
        "unlocks": [
            "prestige_ultimate_cosmetic",
            "god_mode_access",
            "infinite_respec",
            "max_prestige_title"
        ]
    }
]

def get_prestige_level(level: int) -> Dict[str, Any]:
    """Get prestige level configuration."""
    for p_level in PRESTIGE_LEVELS:
        if p_level["level"] == level:
            return p_level
    return None

def can_prestige(player_data: Dict[str, Any], next_level: int) -> tuple[bool, str]:
    """Check if player can prestige to next level."""
    config = get_prestige_level(next_level)
    if not config:
        return False, "Invalid prestige level"

    requirements = config["requirements"]

    if player_data.get("level", 0) < requirements["min_player_level"]:
        return False, f"Need level {requirements['min_player_level']}"

    if abs(player_data.get("karma_points", 0)) < requirements["karma_threshold"]:
        return False, f"Need {requirements['karma_threshold']} karma"

    if player_data.get("achievements_unlocked", 0) < requirements["achievements_required"]:
        return False, f"Need {requirements['achievements_required']} achievements"

    return True, "Ready to prestige"

def calculate_kept_traits(traits: Dict[str, float], prestige_level: int) -> Dict[str, float]:
    """Calculate traits kept after prestige based on level."""
    config = get_prestige_level(prestige_level)
    if not config:
        return {}

    keep_percentage = config["reset_effects"]["keep_percentage"]
    return {trait: value * keep_percentage for trait, value in traits.items()}
