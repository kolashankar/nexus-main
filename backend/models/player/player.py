from pydantic import BaseModel, Field, EmailStr
from typing import Dict, List, Optional
from datetime import datetime
from backend.models.base import BaseDBModel
from backend.models.player.traits import TraitsModel as Traits, MetaTraitsModel as MetaTraits  # pylint: disable=duplicate-code

# Currencies Model
class Currencies(BaseModel):
    """6 Currency Types"""
    credits: int = Field(default=1000, ge=0)
    karma_tokens: int = Field(default=0, ge=0)
    dark_matter: int = Field(default=0, ge=0)
    prestige_points: int = Field(default=0, ge=0)
    guild_coins: int = Field(default=0, ge=0)
    legacy_shards: int = Field(default=0, ge=0)

# Visibility Settings
class Visibility(BaseModel):
    """Privacy/Visibility Settings"""
    privacy_tier: str = Field(default="public")
    cash: bool = Field(default=False)
    economic_class: bool = Field(default=False)
    moral_class: bool = Field(default=False)
    traits_public: List[str] = Field(default_factory=list)
    superpowers: bool = Field(default=False)
    karma_score: bool = Field(default=False)
    guild: bool = Field(default=True)
    location: bool = Field(default=True)

# Player Stats
class PlayerStats(BaseModel):
    """Player Statistics"""
    total_actions: int = Field(default=0)
    total_stolen: int = Field(default=0)
    total_donated: int = Field(default=0)
    pvp_wins: int = Field(default=0)
    pvp_losses: int = Field(default=0)
    quests_completed: int = Field(default=0)
    guilds_joined: int = Field(default=0)
    robots_owned: int = Field(default=0)
    marriages: int = Field(default=0)

# Main Player Model
class Player(BaseDBModel):
    """Complete Player Model"""
    # Basic Info
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password_hash: str

    # Profile
    level: int = Field(default=1, ge=1, le=100)
    xp: int = Field(default=0, ge=0)
    prestige_level: int = Field(default=0, ge=0, le=10)

    # Classes
    economic_class: str = Field(default="middle")
    moral_class: str = Field(default="average")

    # Currencies
    currencies: Currencies = Field(default_factory=Currencies)
    karma_points: int = Field(default=0)

    # Traits
    traits: Traits = Field(default_factory=Traits)
    meta_traits: MetaTraits = Field(default_factory=MetaTraits)

    # Visibility
    visibility: Visibility = Field(default_factory=Visibility)

    # Stats
    stats: PlayerStats = Field(default_factory=PlayerStats)

    # Active State
    online: bool = Field(default=False)
    last_action: Optional[datetime] = None
    last_login: Optional[datetime] = None

# Create/Update Schemas
class PlayerCreate(BaseModel):
    """Schema for creating a new player"""
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    economic_class: Optional[str] = "middle"
    moral_class: Optional[str] = "average"

class PlayerUpdate(BaseModel):
    """Schema for updating player info"""
    economic_class: Optional[str] = None
    moral_class: Optional[str] = None

class PlayerResponse(BaseModel):
    """Public player response (respects visibility)"""
    id: str
    username: str
    level: int
    economic_class: Optional[str] = None
    moral_class: Optional[str] = None
    karma_points: Optional[int] = None
    traits: Optional[Dict[str, float]] = None
    meta_traits: Optional[Dict[str, float]] = None
    online: bool

    @classmethod
    def from_player(cls, player: Player, requester_id: Optional[str] = None):
        """Create response based on visibility settings"""
        # If requester is self, show everything
        if requester_id and requester_id == player.id:
            return cls(
                id=player.id,
                username=player.username,
                level=player.level,
                economic_class=player.economic_class,
                moral_class=player.moral_class,
                karma_points=player.karma_points,
                traits=player.traits.model_dump(),
                meta_traits=player.meta_traits.model_dump(),
                online=player.online
            )

        # Otherwise respect visibility
        response_data = {
            "id": player.id,
            "username": player.username,
            "level": player.level,
            "online": player.online
        }

        if player.visibility.economic_class:
            response_data["economic_class"] = player.economic_class

        if player.visibility.moral_class:
            response_data["moral_class"] = player.moral_class

        if player.visibility.karma_score:
            response_data["karma_points"] = player.karma_points

        # Show only public traits
        if player.visibility.traits_public:
            visible_traits = {k: v for k, v in player.traits.model_dump().items()
                            if k in player.visibility.traits_public}
            response_data["traits"] = visible_traits

        return cls(**response_data)
