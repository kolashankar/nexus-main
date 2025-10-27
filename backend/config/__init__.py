"""Configuration package for game data."""

from .skill_tree_nodes import get_all_skill_trees
from .superpower_definitions import ALL_SUPERPOWERS, get_superpower_by_id
from .achievement_definitions import ALL_ACHIEVEMENTS, get_achievement_by_id
from .prestige_config import PRESTIGE_LEVELS, get_prestige_level
from .legacy_perks import LEGACY_PERKS, get_legacy_perk_by_id

__all__ = [
    "get_all_skill_trees",
    "ALL_SUPERPOWERS",
    "get_superpower_by_id",
    "ALL_ACHIEVEMENTS",
    "get_achievement_by_id",
    "PRESTIGE_LEVELS",
    "get_prestige_level",
    "LEGACY_PERKS",
    "get_legacy_perk_by_id",
]
