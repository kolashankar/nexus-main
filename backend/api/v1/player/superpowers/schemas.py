from pydantic import BaseModel, Field
from typing import Dict, Optional
from backend.models.player.superpowers import PowerTier

class SuperpowerResponse(BaseModel):
    power_id: str
    name: str
    description: str
    tier: PowerTier
    unlocked: bool
    level: int = 1
    usage_count: int = 0
    mastery: float = 0.0
    on_cooldown: bool = False

class UnlockPowerRequest(BaseModel):
    power_id: str = Field(..., description="ID of the power to unlock")

class EquipPowerRequest(BaseModel):
    power_id: str = Field(..., description="ID of the power to equip")

class UsePowerRequest(BaseModel):
    power_id: str = Field(..., description="ID of the power to use")
    target_id: Optional[str] = Field(
        None, description="Target player ID (if applicable)")

class PowerDefinitionResponse(BaseModel):
    power_id: str
    name: str
    description: str
    tier: PowerTier
    requirements: Dict[str, float]
    cooldown_seconds: int
    energy_cost: int
    eligible: bool = False
