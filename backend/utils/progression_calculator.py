"""Progression Calculation Utilities.

Helpers for calculating XP, levels, trait growth, etc.
"""

import math
from typing import Dict, Tuple

def calculate_xp_for_level(level: int) -> int:
    """Calculate total XP required to reach a level.
    
    Uses exponential curve: XP = 100 * (level ^ 2.5)
    """
    if level <= 1:
        return 0
    return int(100 * math.pow(level, 2.5))

def calculate_level_from_xp(xp: int) -> Tuple[int, int, int]:
    """Calculate level and progress from total XP.
    
    Returns:
        (level, xp_for_current_level, xp_for_next_level)
    """
    level = 1
    while calculate_xp_for_level(level + 1) <= xp:
        level += 1

    xp_current = calculate_xp_for_level(level)
    xp_next = calculate_xp_for_level(level + 1)

    return level, xp - xp_current, xp_next - xp_current

def calculate_trait_growth(
    current_value: float,
    action_impact: float,
    trait_growth_multiplier: float = 1.0
) -> float:
    """Calculate new trait value after an action.
    
    Args:
        current_value: Current trait value (0-100)
        action_impact: Impact of action (-10 to +10)
        trait_growth_multiplier: Multiplier from prestige bonuses
    
    Returns:
        New trait value (clamped to 0-100)
    """
    # Diminishing returns as trait approaches limits
    if action_impact > 0:
        # Harder to grow as you approach 100
        resistance = current_value / 100.0
        adjusted_impact = action_impact * (1.0 - resistance * 0.5)
    else:
        # Harder to decay as you approach 0
        resistance = (100 - current_value) / 100.0
        adjusted_impact = action_impact * (1.0 - resistance * 0.5)

    # Apply growth multiplier
    adjusted_impact *= trait_growth_multiplier

    # Calculate new value
    new_value = current_value + adjusted_impact

    # Clamp to 0-100
    return max(0.0, min(100.0, new_value))

def calculate_superpower_unlock_progress(
    player_traits: Dict[str, float],
    required_traits: Dict[str, float]
) -> float:
    """Calculate progress toward unlocking a superpower.
    
    Returns:
        Progress percentage (0.0 to 1.0)
    """
    if not required_traits:
        return 1.0

    total_progress = 0.0
    for trait, required_value in required_traits.items():
        current_value = player_traits.get(trait, 0.0)
        trait_progress = min(1.0, current_value / required_value)
        total_progress += trait_progress

    return total_progress / len(required_traits)

def calculate_skill_tree_cost(node_id: int, nodes_unlocked: int) -> Dict[str, int]:
    """Calculate cost to unlock a skill tree node.
    
    Args:
        node_id: ID of node to unlock (1-20)
        nodes_unlocked: Number of nodes already unlocked
    
    Returns:
        Cost dictionary (e.g., {"credits": 1000, "karma_tokens": 50})
    """
    base_cost = 500
    cost_multiplier = 1.5

    # Cost increases with node ID and nodes already unlocked
    credits_cost = int(base_cost * math.pow(cost_multiplier, node_id - 1))
    karma_tokens_cost = int(credits_cost * 0.1)

    return {
        "credits": credits_cost,
        "karma_tokens": karma_tokens_cost
    }

def calculate_achievement_points(achievements_unlocked: int, total_achievements: int) -> int:
    """Calculate achievement points based on completion.
    
    Returns:
        Total achievement points
    """
    return achievements_unlocked * 10 + (achievements_unlocked // 10) * 50

def calculate_prestige_bonus_total(prestige_level: int, bonus_type: str) -> float:
    """Calculate total bonus from prestige level.
    
    Args:
        prestige_level: Current prestige level (0-10)
        bonus_type: Type of bonus (xp_multiplier, karma_multiplier, etc.)
    
    Returns:
        Total multiplier (e.g., 1.5 for +50% bonus)
    """
    # Base bonuses per prestige level
    bonuses_per_level = {
        "xp_multiplier": 0.10,
        "karma_multiplier": 0.10,
        "credits_multiplier": 0.10,
        "trait_growth": 0.05
    }

    base_bonus = bonuses_per_level.get(bonus_type, 0.05)
    total_bonus = 1.0 + (base_bonus * prestige_level)

    return total_bonus

def calculate_legacy_shard_earnings(actions_completed: int, karma_gained: int) -> int:
    """Calculate legacy shards earned in a season.
    
    Args:
        actions_completed: Total actions performed
        karma_gained: Total karma gained (absolute value)
    
    Returns:
        Legacy shards earned
    """
    # 1 shard per 100 actions
    action_shards = actions_completed // 100

    # 1 shard per 50 karma (positive or negative)
    karma_shards = abs(karma_gained) // 50

    return action_shards + karma_shards

def calculate_daily_quest_rewards(player_level: int, prestige_level: int) -> Dict[str, int]:
    """Calculate rewards for completing a daily quest.
    
    Args:
        player_level: Current player level
        prestige_level: Current prestige level
    
    Returns:
        Reward dictionary
    """
    base_xp = 500
    base_credits = 1000
    base_karma_tokens = 50

    # Scale with level
    xp = int(base_xp * (1 + player_level * 0.1))
    credits = int(base_credits * (1 + player_level * 0.1))
    karma_tokens = int(base_karma_tokens * (1 + player_level * 0.05))

    # Apply prestige bonus
    prestige_multiplier = calculate_prestige_bonus_total(
        prestige_level, "xp_multiplier")

    return {
        "xp": int(xp * prestige_multiplier),
        "credits": int(credits * prestige_multiplier),
        "karma_tokens": karma_tokens
    }
