from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class PrestigeLevel(BaseModel):
    """Single prestige level"""
    level: int = Field(0, ge=0, le=10)
    reached_at: Optional[datetime] = None
    traits_kept_percentage: float = 0.10  # 10% of traits kept
    bonus_multipliers: Dict[str, float] = Field(default_factory=dict)

class PrestigeReward(BaseModel):
    """Reward for prestiging"""
    prestige_level: int
    prestige_points: int = 100
    exclusive_powers: List[str] = Field(default_factory=list)
    permanent_bonuses: Dict[str, float] = Field(default_factory=dict)
    cosmetic_rewards: List[str] = Field(default_factory=list)

class PlayerPrestige(BaseModel):
    """Prestige system for a player"""
    player_id: str
    current_prestige_level: int = 0
    total_prestiges: int = 0
    prestige_points: int = 0
    can_prestige: bool = False
    next_prestige_requirements: Dict[str, Any] = Field(default_factory=dict)
    prestige_history: List[datetime] = Field(default_factory=list)
    permanent_bonuses: Dict[str, float] = Field(default_factory=dict)

    def check_prestige_eligibility(self, player_level: int, karma: int) -> bool:
        """Check if player can prestige"""
        if self.current_prestige_level >= 10:
            return False
        if player_level < 100:
            return False
        if karma < 1000:
            return False
        self.can_prestige = True
        return True

    def perform_prestige(self) -> bool:
        """Perform prestige reset"""
        if not self.can_prestige:
            return False

        self.current_prestige_level += 1
        self.total_prestiges += 1
        self.prestige_points += 100
        self.prestige_history.append(datetime.utcnow())
        self.can_prestige = False
        return True
