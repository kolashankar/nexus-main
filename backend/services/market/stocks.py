"""Stock market service - AI Economist managed."""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import random

from backend.core.database import get_database
from backend.services.economy.currency import CurrencyService


class StockMarketService:
    """Manage stock market operations."""

    # Virtual companies in Karma Nexus world
    COMPANIES = {
        "ROBO": {
            "name": "RoboCorp Industries",
            "description": "Leading robot manufacturer",
            "sector": "Technology",
            "base_price": 100.0
        },
        "HACK": {
            "name": "HackerGuild Inc",
            "description": "Cyber security and hacking services",
            "sector": "Technology",
            "base_price": 75.0
        },
        "MEDIC": {
            "name": "MediTech Solutions",
            "description": "Healthcare and medical services",
            "sector": "Healthcare",
            "base_price": 120.0
        },
        "KARMA": {
            "name": "Karma Energy Corp",
            "description": "Spiritual energy and karma trading",
            "sector": "Energy",
            "base_price": 90.0
        },
        "GUILD": {
            "name": "Guild Holdings",
            "description": "Guild management and territory",
            "sector": "Real Estate",
            "base_price": 150.0
        },
        "NEXUS": {
            "name": "Nexus Systems",
            "description": "AI and neural network development",
            "sector": "AI",
            "base_price": 200.0
        }
    }

    def __init__(self):
        self.currency_service = CurrencyService()

    async def initialize_market(self):
        """Initialize stock market with base prices."""
        db = await get_database()

        for ticker, company_data in self.COMPANIES.items():
            existing = await db.stocks.find_one({"ticker": ticker})

            if not existing:
                stock = {
                    "ticker": ticker,
                    "company_name": company_data["name"],
                    "description": company_data["description"],
                    "sector": company_data["sector"],
                    "price": company_data["base_price"],
                    "change_24h": 0.0,
                    "change_percent": 0.0,
                    "volume": 0,
                    "market_cap": company_data["base_price"] * 1000000,
                    "last_updated": datetime.utcnow()
                }
                await db.stocks.insert_one(stock)

    async def get_all_stocks(self) -> List[Dict[str, Any]]:
        """Get all stocks."""
        db = await get_database()
        stocks = await db.stocks.find().to_list(length=100)
        return stocks

    async def get_stock(self, ticker: str) -> Dict[str, Any] | None:
        """Get specific stock information."""
        db = await get_database()
        stock = await db.stocks.find_one({"ticker": ticker.upper()})
        return stock

    async def buy_stock(
        self,
        player_id: str,
        ticker: str,
        quantity: int
    ) -> Dict[str, Any]:
        """Buy stocks."""
        ticker = ticker.upper()

        # Get stock
        stock = await self.get_stock(ticker)
        if not stock:
            raise ValueError("Stock not found")

        # Calculate cost
        cost = int(stock["price"] * quantity)

        # Check balance
        balance = await self.currency_service.get_balance(player_id, "credits")
        if balance < cost:
            raise ValueError("Insufficient credits")

        # Deduct credits
        await self.currency_service.deduct_currency(
            player_id,
            "credits",
            cost,
            reason=f"buy_stock_{ticker}"
        )

        # Add to portfolio
        db = await get_database()
        await db.portfolios.update_one(
            {"player_id": player_id},
            {
                "$inc": {f"holdings.{ticker}": quantity},
                "$set": {"updated_at": datetime.utcnow()}
            },
            upsert=True
        )

        # Update volume
        await db.stocks.update_one(
            {"ticker": ticker},
            {"$inc": {"volume": quantity}}
        )

        return {
            "success": True,
            "ticker": ticker,
            "quantity": quantity,
            "price_per_share": stock["price"],
            "total_cost": cost,
            "message": f"Bought {quantity} shares of {ticker}"
        }

    async def sell_stock(
        self,
        player_id: str,
        ticker: str,
        quantity: int
    ) -> Dict[str, Any]:
        """Sell stocks."""
        ticker = ticker.upper()

        # Get stock
        stock = await self.get_stock(ticker)
        if not stock:
            raise ValueError("Stock not found")

        # Check portfolio
        db = await get_database()
        portfolio = await db.portfolios.find_one({"player_id": player_id})

        if not portfolio:
            raise ValueError("No portfolio found")

        holdings = portfolio.get("holdings", {})
        current_quantity = holdings.get(ticker, 0)

        if current_quantity < quantity:
            raise ValueError(
                f"Insufficient shares. You have {current_quantity}")

        # Calculate proceeds
        proceeds = int(stock["price"] * quantity)

        # Remove from portfolio
        await db.portfolios.update_one(
            {"player_id": player_id},
            {
                "$inc": {f"holdings.{ticker}": -quantity},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )

        # Add credits
        await self.currency_service.add_currency(
            player_id,
            "credits",
            proceeds,
            reason=f"sell_stock_{ticker}"
        )

        # Update volume
        await db.stocks.update_one(
            {"ticker": ticker},
            {"$inc": {"volume": quantity}}
        )

        return {
            "success": True,
            "ticker": ticker,
            "quantity": quantity,
            "price_per_share": stock["price"],
            "total_proceeds": proceeds,
            "message": f"Sold {quantity} shares of {ticker}"
        }

    async def get_portfolio(self, player_id: str) -> Dict[str, Any]:
        """Get player's stock portfolio."""
        db = await get_database()

        portfolio = await db.portfolios.find_one({"player_id": player_id})

        if not portfolio:
            return {
                "player_id": player_id,
                "holdings": {},
                "total_value": 0,
                "total_invested": 0,
                "profit_loss": 0
            }

        holdings = portfolio.get("holdings", {})

        # Calculate current value
        total_value = 0
        detailed_holdings = []

        for ticker, quantity in holdings.items():
            if quantity > 0:
                stock = await self.get_stock(ticker)
                if stock:
                    current_value = stock["price"] * quantity
                    total_value += current_value

                    detailed_holdings.append({
                        "ticker": ticker,
                        "quantity": quantity,
                        "current_price": stock["price"],
                        "current_value": current_value,
                        "change_percent": stock.get("change_percent", 0)
                    })

        return {
            "player_id": player_id,
            "holdings": detailed_holdings,
            "total_value": total_value,
            "updated_at": portfolio.get("updated_at")
        }

    async def update_stock_prices(self):
        """Update all stock prices (called periodically by AI Economist)."""
        db = await get_database()

        stocks = await self.get_all_stocks()

        for stock in stocks:
            # Random price movement (±5%)
            change_percent = random.uniform(-5.0, 5.0)
            new_price = stock["price"] * (1 + change_percent / 100)

            # Ensure minimum price
            new_price = max(1.0, new_price)

            change_24h = new_price - stock["price"]

            await db.stocks.update_one(
                {"ticker": stock["ticker"]},
                {
                    "$set": {
                        "price": round(new_price, 2),
                        "change_24h": round(change_24h, 2),
                        "change_percent": round(change_percent, 2),
                        "last_updated": datetime.utcnow()
                    }
                }
            )

    async def get_stock_history(
        self,
        ticker: str,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get historical stock prices."""
        db = await get_database()

        history = await db.stock_history.find({
            "ticker": ticker.upper(),
            "date": {"$gte": datetime.utcnow() - timedelta(days=days)}
        }).sort("date", 1).to_list(length=days)

        return history

    async def record_daily_price(self):
        """Record daily closing prices for history."""
        db = await get_database()

        stocks = await self.get_all_stocks()

        for stock in stocks:
            history_entry = {
                "ticker": stock["ticker"],
                "date": datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0),
                "open": stock["price"],
                "close": stock["price"],
                "high": stock["price"],
                "low": stock["price"],
                "volume": stock.get("volume", 0)
            }

            await db.stock_history.insert_one(history_entry)
