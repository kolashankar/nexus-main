from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LegacyResponse(BaseModel):
    legacy_level: int
    legacy_points: int
    lifetime_legacy_points: int
    seasons_played: int
    titles_earned: int
    active_title: Optional[str] = None
    heirlooms: int
    unlocked_perks: int

class LegacyPerkResponse(BaseModel):
    perk_id: str
    name: str
    description: str
    bonus_type: str
    bonus_value: float
    cost: int
    unlocked: bool

class UnlockPerkRequest(BaseModel):
    perk_id: str = Field(..., description="ID of the perk to unlock")

class ActivatePerkRequest(BaseModel):
    perk_id: str = Field(..., description="ID of the perk to activate")

class EarnPointsRequest(BaseModel):
    amount: int = Field(..., ge=1,
                        description="Amount of legacy points to earn")
    source: str = Field(..., description="Source of the legacy points")

class LegacyTitleResponse(BaseModel):
    title_id: str
    name: str
    description: str
    earned_at: datetime
    season_earned: int
    permanent: bool

class HeirloomResponse(BaseModel):
    item_id: str
    name: str
    description: str
    power_level: int
    transferable: bool
    season_acquired: int

class NewCharacterBonusesResponse(BaseModel):
    xp_multiplier: float
    karma_multiplier: float
    trait_multiplier: float
    starting_credits: int
    starting_skill_points: int
