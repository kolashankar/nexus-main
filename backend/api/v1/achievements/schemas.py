from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from backend.models.achievements import AchievementCategory, AchievementRarity
from datetime import datetime

class AchievementResponse(BaseModel):
    achievement_id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    points: int
    unlocked: bool = False
    unlocked_at: Optional[datetime] = None
    progress: Optional[float] = None

class UnlockAchievementRequest(BaseModel):
    achievement_id: str = Field(...,
                                description="ID of the achievement to unlock")

class UpdateProgressRequest(BaseModel):
    achievement_id: str = Field(..., description="ID of the achievement")
    progress_amount: int = Field(..., ge=1,
                                 description="Amount of progress to add")

class AchievementSummaryResponse(BaseModel):
    total_achievements: int
    unlocked: int
    completion_percentage: float
    total_points: int
    by_rarity: Dict[str, int]
    recent_unlocks: List[str]
