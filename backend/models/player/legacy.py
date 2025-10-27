from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class LegacyTitle(BaseModel):
    """Cross-season legacy title"""
    title_id: str
    name: str
    description: str
    earned_at: datetime
    season_earned: int
    permanent: bool = True

class HeirloomItem(BaseModel):
    """Item that can be passed to new characters"""
    item_id: str
    name: str
    description: str
    power_level: int
    transferable: bool = True
    season_acquired: int

class LegacyPerk(BaseModel):
    """Permanent account-wide perk"""
    perk_id: str
    name: str
    description: str
    bonus_type: str  # "xp_boost", "karma_multiplier", "trait_gain_bonus"
    bonus_value: float
    cost: int  # Legacy points required
    unlocked: bool = False

class PlayerLegacy(BaseModel):
    """Cross-season legacy system"""
    account_id: str
    legacy_points: int = 0
    lifetime_legacy_points: int = 0
    legacy_level: int = 1

    # Titles
    earned_titles: List[LegacyTitle] = Field(default_factory=list)
    active_title: Optional[str] = None

    # Heirlooms
    heirloom_items: List[HeirloomItem] = Field(default_factory=list)

    # Perks
    unlocked_perks: List[LegacyPerk] = Field(default_factory=list)
    active_perks: List[str] = Field(default_factory=list)

    # Statistics
    seasons_played: int = 0
    total_characters_created: int = 0
    highest_karma_achieved: int = 0
    total_achievements: int = 0

    # Mentorship
    mentorship_level: int = 0
    apprentices_taught: int = 0
    mentorship_rewards_earned: int = 0

    def earn_legacy_points(self, amount: int, source: str):
        """Earn legacy points from various sources"""
        self.legacy_points += amount
        self.lifetime_legacy_points += amount

        # Level up legacy level
        points_for_next_level = self.legacy_level * 1000
        if self.lifetime_legacy_points >= points_for_next_level:
            self.legacy_level += 1

    def spend_legacy_points(self, amount: int) -> bool:
        """Spend legacy points on perks"""
        if self.legacy_points >= amount:
            self.legacy_points -= amount
            return True
        return False

    def add_title(self, title: LegacyTitle):
        """Add a new legacy title"""
        if not any(t.title_id == title.title_id for t in self.earned_titles):
            self.earned_titles.append(title)
