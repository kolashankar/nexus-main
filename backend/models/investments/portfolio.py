from pydantic import BaseModel, Field
from typing import List, Dict
from datetime import datetime


class PortfolioSummary(BaseModel):
    """Investment portfolio summary."""
    player_id: str = Field(..., description="Player ID")

    total_invested: int = Field(
        default=0, ge=0, description="Total amount invested")
    current_value: int = Field(
        default=0, ge=0, description="Current portfolio value")
    total_profit_loss: int = Field(default=0, description="Total profit/loss")
    roi_percentage: float = Field(
        default=0.0, description="Return on investment percentage")

    active_investments: int = Field(
        default=0, ge=0, description="Number of active investments")
    total_dividends: int = Field(
        default=0, ge=0, description="Total dividends received")

    last_updated: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "player_id": "player_1",
                "total_invested": 50000,
                "current_value": 60000,
                "total_profit_loss": 10000,
                "roi_percentage": 20.0,
                "active_investments": 5,
                "total_dividends": 2000,
                "last_updated": "2025-01-01T12:00:00Z"
            }
        }


class Portfolio(BaseModel):
    """Complete investment portfolio."""
    summary: PortfolioSummary
    investments: List[Dict] = Field(default_factory=list)
    performance_history: List[Dict] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "summary": {
                    "player_id": "player_1",
                    "total_invested": 50000,
                    "current_value": 60000,
                    "total_profit_loss": 10000,
                    "roi_percentage": 20.0,
                    "active_investments": 5,
                    "total_dividends": 2000
                },
                "investments": [],
                "performance_history": []
            }
        }
