from pydantic import BaseModel
from typing import List, Dict

class PrestigeResponse(BaseModel):
    current_prestige_level: int
    total_prestiges: int
    prestige_points: int
    can_prestige: bool
    permanent_bonuses: Dict[str, float]

class PrestigeEligibilityResponse(BaseModel):
    eligible: bool
    message: str
    current_level: int
    current_karma: int
    current_achievements: int
    requirements: Dict[str, int]

class PrestigeRewardResponse(BaseModel):
    prestige_level: int
    prestige_points: int
    exclusive_powers: List[str]
    permanent_bonuses: Dict[str, float]
    cosmetic_rewards: List[str]

class PrestigePerformResponse(BaseModel):
    success: bool
    message: str
    prestige_level: int
    rewards: Dict
    new_traits: Dict[str, float]
    permanent_bonuses: Dict[str, float]
