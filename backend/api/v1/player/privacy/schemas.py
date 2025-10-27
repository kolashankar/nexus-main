from pydantic import BaseModel
from typing import Optional, List

class VisibilitySettingsUpdate(BaseModel):
    cash: Optional[bool] = None
    economic_class: Optional[bool] = None
    moral_class: Optional[bool] = None
    traits_public: Optional[List[str]] = None
    superpowers: Optional[bool] = None
    karma_score: Optional[bool] = None
    guild: Optional[bool] = None
    location: Optional[bool] = None

class PrivacyTierUpdate(BaseModel):
    tier: str  # public, selective, private, ghost, phantom

class PrivacySettingsResponse(BaseModel):
    privacy_tier: str
    cash: bool
    economic_class: bool
    moral_class: bool
    traits_public: List[str]
    superpowers: bool
    karma_score: bool
    guild: bool
    location: bool
