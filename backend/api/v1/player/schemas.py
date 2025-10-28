from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class AppearanceUpdate(BaseModel):
    """Character appearance update."""
    model: Optional[str] = None
    skin_tone: Optional[str] = None
    hair_color: Optional[str] = None
    hair_style: Optional[str] = None

class PlayerUpdateRequest(BaseModel):
    """Request to update player profile."""
    economic_class: Optional[str] = None
    moral_class: Optional[str] = None
    character_model: Optional[str] = None
    skin_tone: Optional[str] = None
    hair_color: Optional[str] = None
    appearance: Optional[AppearanceUpdate] = None

class PlayerProfileResponse(BaseModel):
    """Complete player profile response."""
    id: str
    username: str
    email: str
    level: int
    xp: int
    prestige_level: int
    economic_class: str
    moral_class: str
    currencies: Dict
    karma_points: int
    traits: Dict[str, float]
    meta_traits: Dict[str, float]
    visibility: Dict
    stats: Dict
    online: bool
    last_login: Optional[datetime] = None
    appearance: Optional[Dict] = None
    character_model: Optional[str] = None
    skin_tone: Optional[str] = None
    hair_color: Optional[str] = None

class PlayerStatsResponse(BaseModel):
    """Player statistics response."""
    id: str
    username: str
    level: int
    xp: int
    stats: Dict
    total_karma: int
    rank: Optional[int] = None

class VisibilityUpdateRequest(BaseModel):
    """Update visibility/privacy settings."""
    privacy_tier: Optional[str] = Field(
        None, pattern="^(public|selective|private|ghost|phantom)$")
    cash: Optional[bool] = None
    economic_class: Optional[bool] = None
    moral_class: Optional[bool] = None
    traits_public: Optional[List[str]] = None
    superpowers: Optional[bool] = None
    karma_score: Optional[bool] = None
    guild: Optional[bool] = None
    location: Optional[bool] = None