"""The Economist AI - manages stock market and economy."""

from typing import Dict, Any
import random
from datetime import datetime

from backend.core.database import get_database
from backend.services.market.stocks import StockMarketService


class Economist:
    """The Economist - AI-driven market management."""

    def __init__(self):
        self.stock_service = StockMarketService()

    async def update_market_prices(self):
        """Update all stock prices based on market conditions."""
        await self.stock_service.update_stock_prices()

    async def trigger_market_event(self, event_type: str = None):
        """Trigger a market event."""
        if event_type is None:
            # Random event
            events = ["boom", "crash", "inflation", "stability"]
            event_type = random.choice(events)

        db = await get_database()

        event_data = {
            "event_type": event_type,
            "triggered_at": datetime.utcnow(),
            "description": self._get_event_description(event_type),
            "effects": self._get_event_effects(event_type)
        }

        # Store event
        await db.market_events.insert_one(event_data)

        # Apply effects
        await self._apply_event_effects(event_type)

        return event_data

    def _get_event_description(self, event_type: str) -> str:
        """Get description for market event."""
        descriptions = {
            "boom": "Economic boom! Stock prices surge across all sectors.",
            "crash": "Market crash! Panic selling causes widespread losses.",
            "inflation": "Inflation rises! Currency values decrease, prices increase.",
            "stability": "Market stabilization. Prices return to normal levels."
        }
        return descriptions.get(event_type, "Market event occurred.")

    def _get_event_effects(self, event_type: str) -> Dict[str, Any]:
        """Get effects for market event."""
        effects = {
            "boom": {"price_multiplier": 1.2, "duration_hours": 24},
            "crash": {"price_multiplier": 0.7, "duration_hours": 12},
            "inflation": {"price_multiplier": 1.1, "duration_hours": 48},
            "stability": {"price_multiplier": 1.0, "duration_hours": 0}
        }
        return effects.get(event_type, {})

    async def _apply_event_effects(self, event_type: str):
        """Apply market event effects to stocks."""
        effects = self._get_event_effects(event_type)
        multiplier = effects.get("price_multiplier", 1.0)

        db = await get_database()

        # Apply to all stocks
        stocks = await self.stock_service.get_all_stocks()

        for stock in stocks:
            new_price = stock["price"] * multiplier
            new_price = max(1.0, new_price)  # Minimum price

            await db.stocks.update_one(
                {"ticker": stock["ticker"]},
                {"$set": {"price": round(new_price, 2)}}
            )

    async def analyze_market_trends(self) -> Dict[str, Any]:
        """Analyze current market trends."""
        stocks = await self.stock_service.get_all_stocks()

        total_change = sum(stock.get("change_percent", 0) for stock in stocks)
        avg_change = total_change / len(stocks) if stocks else 0

        if avg_change > 5:
            trend = "bullish"
        elif avg_change < -5:
            trend = "bearish"
        else:
            trend = "neutral"

        return {
            "trend": trend,
            "avg_change_percent": round(avg_change, 2),
            "total_stocks": len(stocks),
            "recommendation": self._get_recommendation(trend)
        }

    def _get_recommendation(self, trend: str) -> str:
        """Get investment recommendation based on trend."""
        recommendations = {
            "bullish": "Strong buying opportunity - market is rising!",
            "bearish": "Caution advised - consider selling or holding cash.",
            "neutral": "Stable market - good time for balanced investing."
        }
        return recommendations.get(trend, "Market conditions unclear.")
