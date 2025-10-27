"""Stock market schemas."""

from pydantic import BaseModel, Field
from datetime import datetime


class BuyStockRequest(BaseModel):
    """Request to buy stocks."""
    ticker: str = Field(..., description="Stock ticker symbol")
    quantity: int = Field(..., gt=0, description="Number of shares to buy")


class SellStockRequest(BaseModel):
    """Request to sell stocks."""
    ticker: str = Field(..., description="Stock ticker symbol")
    quantity: int = Field(..., gt=0, description="Number of shares to sell")


class StockPriceResponse(BaseModel):
    """Stock price information."""
    ticker: str
    company_name: str
    price: float
    change_24h: float
    change_percent: float
    volume: int
    market_cap: float
    last_updated: datetime
