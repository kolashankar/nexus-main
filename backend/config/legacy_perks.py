"""Legacy System - Cross-Season Progression.

Legacy perks provide permanent account-wide bonuses.
"""

from typing import Dict, List, Any

LEGACY_PERKS: List[Dict[str, Any]] = [
    {
        "id": "legacy_xp_boost",
        "name": "Legacy XP Boost",
        "description": "Permanent +5% XP gain on all characters",
        "cost": {"legacy_shards": 1000},
        "max_level": 10,
        "bonus_per_level": {"xp_multiplier": 0.05},
        "cumulative": True
    },
    {
        "id": "legacy_karma_boost",
        "name": "Legacy Karma Boost",
        "description": "Permanent +5% karma gain on all characters",
        "cost": {"legacy_shards": 1000},
        "max_level": 10,
        "bonus_per_level": {"karma_multiplier": 0.05},
        "cumulative": True
    },
    {
        "id": "legacy_starting_traits",
        "name": "Legacy Starting Traits",
        "description": "New characters start with +10% in all traits",
        "cost": {"legacy_shards": 2000},
        "max_level": 5,
        "bonus_per_level": {"starting_trait_bonus": 0.10},
        "cumulative": True
    },
    {
        "id": "legacy_prestige_access",
        "name": "Early Prestige Access",
        "description": "Unlock prestige at level 90 instead of 100",
        "cost": {"legacy_shards": 5000},
        "max_level": 1,
        "bonus_per_level": {"prestige_level_requirement": -10},
        "cumulative": False
    },
    {
        "id": "legacy_power_unlock",
        "name": "Legacy Power Unlock",
        "description": "Unlock one Tier 1 superpower at character creation",
        "cost": {"legacy_shards": 3000},
        "max_level": 1,
        "bonus_per_level": {"starting_power": 1},
        "cumulative": False
    },
    {
        "id": "legacy_currency_start",
        "name": "Legacy Starting Wealth",
        "description": "New characters start with 10,000 credits",
        "cost": {"legacy_shards": 1500},
        "max_level": 10,
        "bonus_per_level": {"starting_credits": 10000},
        "cumulative": True
    },
    {
        "id": "legacy_mentor_bonus",
        "name": "Legacy Mentor Rewards",
        "description": "+20% rewards from mentoring apprentices",
        "cost": {"legacy_shards": 2500},
        "max_level": 5,
        "bonus_per_level": {"mentor_reward_bonus": 0.20},
        "cumulative": True
    },
    {
        "id": "legacy_guild_benefits",
        "name": "Legacy Guild Benefits",
        "description": "+15% to all guild contributions and rewards",
        "cost": {"legacy_shards": 3000},
        "max_level": 5,
        "bonus_per_level": {"guild_bonus": 0.15},
        "cumulative": True
    }
]

def get_legacy_perk_by_id(perk_id: str) -> Dict[str, Any]:
    """Get legacy perk definition by ID."""
    for perk in LEGACY_PERKS:
        if perk["id"] == perk_id:
            return perk
    return None

def calculate_legacy_bonus(perks_owned: Dict[str, int]) -> Dict[str, float]:
    """Calculate total legacy bonuses from owned perks."""
    total_bonuses = {}

    for perk_id, level in perks_owned.items():
        perk = get_legacy_perk_by_id(perk_id)
        if not perk:
            continue

        bonus_per_level = perk["bonus_per_level"]
        for bonus_key, bonus_value in bonus_per_level.items():
            if perk["cumulative"]:
                total_bonuses[bonus_key] = total_bonuses.get(
                    bonus_key, 0) + (bonus_value * level)
            else:
                total_bonuses[bonus_key] = bonus_value

    return total_bonuses

def can_purchase_legacy_perk(player_data: Dict[str, Any], perk_id: str, current_level: int) -> tuple[bool, str]:
    """Check if player can purchase/upgrade a legacy perk."""
    perk = get_legacy_perk_by_id(perk_id)
    if not perk:
        return False, "Perk not found"

    if current_level >= perk["max_level"]:
        return False, "Perk already at max level"

    cost = perk["cost"]
    for currency, amount in cost.items():
        if player_data.get(currency, 0) < amount:
            return False, f"Not enough {currency} (need {amount})"

    return True, "Can purchase"
