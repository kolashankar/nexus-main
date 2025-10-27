"""Progression API Schemas."""

from pydantic import BaseModel, Field
from typing import Dict

class XPGainRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount of XP to gain")

class XPGainResponse(BaseModel):
    success: bool
    new_xp: int
    new_level: int
    level_up: bool
    levels_gained: int

class ProgressionDataResponse(BaseModel):
    level: int
    xp: int
    xp_progress: int
    xp_for_next: int
    prestige_level: int
    skill_tree_progress: Dict[str, float]
    superpowers_unlocked: int
    achievements_unlocked: int
    total_achievements: int

class ProgressionSummaryResponse(BaseModel):
    level: int
    prestige_level: int
    total_skill_nodes: int
    total_superpowers: int
    total_achievements: int
    completion_percentage: float
