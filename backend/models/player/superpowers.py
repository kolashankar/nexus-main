from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PowerTier(str, Enum):
    TIER_1 = "tier_1"  # Basic
    TIER_2 = "tier_2"  # Intermediate
    TIER_3 = "tier_3"  # Advanced
    TIER_4 = "tier_4"  # Master
    TIER_5 = "tier_5"  # Legendary

class SuperpowerDefinition(BaseModel):
    """Definition of a superpower"""
    power_id: str
    name: str
    description: str
    tier: PowerTier
    requirements: Dict[str, float] = Field(
        default_factory=dict)  # {"trait_name": min_value}
    cooldown_seconds: int = 300  # 5 minutes default
    energy_cost: int = 50
    effects: Dict[str, Any] = Field(default_factory=dict)

class UnlockedSuperpower(BaseModel):
    """Player's unlocked superpower"""
    power_id: str
    unlocked_at: datetime
    usage_count: int = 0
    last_used_at: Optional[datetime] = None
    cooldown_until: Optional[datetime] = None
    level: int = Field(1, ge=1, le=10)
    mastery: float = Field(0.0, ge=0.0, le=100.0)

    def is_on_cooldown(self) -> bool:
        """Check if power is on cooldown"""
        if self.cooldown_until is None:
            return False
        return datetime.utcnow() < self.cooldown_until

    def use_power(self, cooldown_seconds: int):
        """Use the power and set cooldown"""
        self.usage_count += 1
        self.last_used_at = datetime.utcnow()
        from datetime import timedelta
        self.cooldown_until = datetime.utcnow() + timedelta(seconds=cooldown_seconds)
        self.mastery = min(100.0, self.mastery + 0.5)

class PlayerSuperpowers(BaseModel):
    """All superpowers for a player"""
    player_id: str
    unlocked_powers: List[UnlockedSuperpower] = Field(default_factory=list)
    equipped_powers: List[str] = Field(default_factory=list, max_items=5)
    total_powers_unlocked: int = 0

    def unlock_power(self, power_id: str) -> bool:
        """Unlock a new superpower"""
        if any(p.power_id == power_id for p in self.unlocked_powers):
            return False

        new_power = UnlockedSuperpower(
            power_id=power_id,
            unlocked_at=datetime.utcnow()
        )
        self.unlocked_powers.append(new_power)
        self.total_powers_unlocked += 1
        return True

    def equip_power(self, power_id: str) -> bool:
        """Equip a power for use"""
        if len(self.equipped_powers) >= 5:
            return False
        if power_id in self.equipped_powers:
            return False
        if not any(p.power_id == power_id for p in self.unlocked_powers):
            return False

        self.equipped_powers.append(power_id)
        return True
