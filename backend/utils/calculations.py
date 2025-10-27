"""Game calculations and formulas"""
from typing import Dict
import math

def calculate_level_from_xp(xp: int) -> int:
    """Calculate player level from XP"""
    return int(math.sqrt(xp / 100)) + 1

def calculate_xp_for_level(level: int) -> int:
    """Calculate XP required for a level"""
    return ((level - 1) ** 2) * 100

def calculate_combat_power(traits: Dict[str, float]) -> float:
    """Calculate overall combat power from traits"""
    combat_traits = [
        'physical_strength', 'speed', 'dexterity',
        'endurance', 'strategy', 'perception'
    ]
    total = sum(traits.get(t, 0) for t in combat_traits)
    return total / len(combat_traits)

def calculate_success_probability(
    actor_skill: float,
    target_resistance: float,
    base_chance: float = 50.0
) -> float:
    """Calculate success probability for actions"""
    diff = actor_skill - target_resistance
    probability = base_chance + diff
    return max(5.0, min(95.0, probability))

def calculate_trait_decay(trait_value: float, decay_rate: float = 0.01) -> float:
    """Calculate trait decay over time"""
    return max(0, trait_value - decay_rate)
