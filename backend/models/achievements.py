from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class AchievementCategory(str, Enum):
    TRAIT_MASTERY = "trait_mastery"
    POWER_COLLECTOR = "power_collector"
    KARMA = "karma"
    SOCIAL = "social"
    ECONOMIC = "economic"
    COMBAT = "combat"
    STORY = "story"
    HIDDEN = "hidden"
    SEASONAL = "seasonal"
    LEGACY = "legacy"

class AchievementRarity(str, Enum):
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

class AchievementDefinition(BaseModel):
    """Definition of an achievement"""
    achievement_id: str
    name: str
    description: str
    category: AchievementCategory
    rarity: AchievementRarity
    icon: str
    points: int = 10
    requirements: Dict[str, Any] = Field(default_factory=dict)
    rewards: Dict[str, int] = Field(default_factory=dict)
    hidden: bool = False
    repeatable: bool = False

class AchievementProgress(BaseModel):
    """Progress tracking for an achievement"""
    achievement_id: str
    current_progress: int = 0
    required_progress: int = 1
    percentage: float = 0.0
    started_at: datetime = Field(default_factory=datetime.utcnow)
    milestones_reached: List[int] = Field(default_factory=list)

    def update_progress(self, amount: int):
        """Update progress towards achievement"""
        self.current_progress = min(
            self.required_progress, self.current_progress + amount)
        self.percentage = (self.current_progress / \
                           self.required_progress) * 100.0

class UnlockedAchievement(BaseModel):
    """Unlocked achievement"""
    achievement_id: str
    unlocked_at: datetime
    points_earned: int
    rarity: AchievementRarity
    notification_shown: bool = False
    completion_time: Optional[float] = None  # Time taken in seconds

class PlayerAchievements(BaseModel):
    """All achievements for a player"""
    player_id: str
    unlocked_achievements: List[UnlockedAchievement] = Field(
        default_factory=list)
    achievement_progress: Dict[str, AchievementProgress] = Field(
        default_factory=dict)
    total_points: int = 0
    completion_percentage: float = 0.0
    recent_unlocks: List[str] = Field(default_factory=list)

    def unlock_achievement(self, achievement_id: str, definition: AchievementDefinition) -> bool:
        """Unlock an achievement"""
        if any(a.achievement_id == achievement_id for a in self.unlocked_achievements):
            if not definition.repeatable:
                return False

        new_achievement = UnlockedAchievement(
            achievement_id=achievement_id,
            unlocked_at=datetime.utcnow(),
            points_earned=definition.points,
            rarity=definition.rarity
        )
        self.unlocked_achievements.append(new_achievement)
        self.total_points += definition.points
        self.recent_unlocks.insert(0, achievement_id)
        if len(self.recent_unlocks) > 10:
            self.recent_unlocks.pop()
        return True
