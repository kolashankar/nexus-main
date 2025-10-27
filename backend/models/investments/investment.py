from pydantic import BaseModel, Field
from datetime import datetime


class Investment(BaseModel):
    """Investment model."""
    id: str = Field(..., description="Investment ID")
    player_id: str = Field(..., description="Player ID")

    investment_type: str = Field(
        ...,
        description="Type (stocks, bonds, crypto, startup, venture)"
    )
    name: str = Field(..., description="Investment name")
    description: str = Field(..., description="Investment description")

    amount_invested: int = Field(..., ge=0, description="Amount invested")
    investment_date: datetime = Field(default_factory=datetime.utcnow)

    expected_return: float = Field(...,
                                   description="Expected return percentage")
    duration_days: int = Field(..., ge=1, description="Investment duration")
    maturity_date: datetime = Field(..., description="Maturity date")

    current_value: int = Field(..., ge=0, description="Current value")
    risk_level: str = Field(..., description="Risk level")

    status: str = Field(default="active", description="Investment status")
    dividends_received: int = Field(default=0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "inv_123",
                "player_id": "player_1",
                "investment_type": "stocks",
                "name": "Tech Corp Shares",
                "description": "Investment in technology company",
                "amount_invested": 10000,
                "expected_return": 15.0,
                "duration_days": 365,
                "current_value": 11500,
                "risk_level": "medium",
                "status": "active"
            }
        }
