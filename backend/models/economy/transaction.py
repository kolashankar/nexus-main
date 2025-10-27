"""Transaction models."""

from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid


class Transaction(BaseModel):
    """Transaction model."""
    transaction_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # transfer, purchase, reward, trade
    from_player: Optional[str] = None
    to_player: Optional[str] = None
    currency_type: str = "credits"
    amount: int
    status: str = "pending"  # pending, completed, failed, cancelled
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "txn-123",
                "type": "transfer",
                "from_player": "player1",
                "to_player": "player2",
                "currency_type": "credits",
                "amount": 1000,
                "status": "completed"
            }
        }


class CurrencyBalance(BaseModel):
    """Currency balance model."""
    player_id: str
    credits: int = 0
    karma_tokens: int = 0
    dark_matter: int = 0
    prestige_points: int = 0
    guild_coins: int = 0
    legacy_shards: int = 0
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    def get_total_wealth(self) -> int:
        """Calculate total wealth score."""
        return (
            self.credits +
            (self.karma_tokens * 10) +
            (self.dark_matter * 10) +
            (self.prestige_points * 50) +
            (self.guild_coins * 5) +
            (self.legacy_shards * 100)
        )

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player-123",
                "credits": 10000,
                "karma_tokens": 50,
                "dark_matter": 20,
                "prestige_points": 5,
                "guild_coins": 100,
                "legacy_shards": 2
            }
        }
