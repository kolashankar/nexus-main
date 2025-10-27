"""Battle Pass model."""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class RewardType(str, Enum):
    """Types of battle pass rewards."""
    CREDITS = "credits"
    XP = "xp"
    KARMA_TOKENS = "karma_tokens"
    COSMETIC = "cosmetic"
    EMOTE = "emote"
    TITLE = "title"
    ROBOT = "robot"
    SUPERPOWER_CHARGE = "superpower_charge"
    TRAIT_BOOST = "trait_boost"
    EXCLUSIVE_ITEM = "exclusive_item"


class BattlePassTier(BaseModel):
    """Individual tier in the battle pass."""
    tier: int = Field(..., ge=1, le=100)
    xp_required: int = Field(...,
                             description="Cumulative XP required to reach this tier")
    free_rewards: List[Dict[str, Any]] = Field(default_factory=list)
    premium_rewards: List[Dict[str, Any]] = Field(default_factory=list)
    is_locked: bool = True

    class Config:
        from_attributes = True


class BattlePass(BaseModel):
    """Battle Pass model."""
    pass_id: str = Field(..., description="Unique battle pass ID")
    season: int = Field(..., description="Season number")
    name: str = Field(..., description="Battle pass name")
    description: str = Field(default="")

    # Timing
    start_date: datetime
    end_date: datetime
    is_active: bool = True

    # Tiers
    total_tiers: int = Field(default=100, description="Total number of tiers")
    free_tiers: int = Field(default=50, description="Number of free tiers")
    premium_tiers: int = Field(
        default=100, description="Number of premium tiers")

    # Tiers data
    tiers: List[BattlePassTier] = Field(default_factory=list)

    # Pricing
    premium_price: int = Field(
        default=1000, description="Cost in credits to unlock premium")

    # Statistics
    total_players: int = Field(default=0)
    premium_players: int = Field(default=0)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class PlayerBattlePass(BaseModel):
    """Player's battle pass progress."""
    player_id: str
    pass_id: str
    season: int

    # Status
    has_premium: bool = Field(default=False)
    current_tier: int = Field(default=0, ge=0, le=100)
    current_xp: int = Field(default=0, ge=0)

    # Rewards
    claimed_free_rewards: List[int] = Field(
        default_factory=list,
        description="List of tier numbers where free rewards have been claimed"
    )
    claimed_premium_rewards: List[int] = Field(
        default_factory=list,
        description="List of tier numbers where premium rewards have been claimed"
    )

    # Progress tracking
    total_xp_earned: int = Field(default=0)
    last_xp_gain: Optional[datetime] = None

    # Purchase info
    premium_purchased_at: Optional[datetime] = None
    premium_price_paid: Optional[int] = None

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class BattlePassReward(BaseModel):
    """Battle pass reward definition."""
    reward_type: RewardType
    reward_id: str = Field(...,
                           description="ID of the specific reward (cosmetic ID, etc.)")
    amount: int = Field(default=1, description="Quantity of the reward")
    name: str
    description: str = ""
    icon_url: Optional[str] = None
    rarity: Optional[str] = Field(
        default="common", description="common, rare, epic, legendary")
    is_premium_only: bool = Field(default=False)

    class Config:
        from_attributes = True
