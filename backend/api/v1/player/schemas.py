from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime

class PlayerUpdateRequest(BaseModel):
    """Request to update player profile."""
    economic_class: Optional[str] = None
    moral_class: Optional[str] = None

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