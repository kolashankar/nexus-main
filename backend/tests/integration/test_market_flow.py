"""Integration tests for market system flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestStockMarket:
    """Test stock market trading flow."""

    @pytest.mark.asyncio
    async def test_get_stock_listings(self, auth_headers, clean_db):
        """Test getting stock market listings."""
        # Create some stocks
        stocks = [
            {
                "ticker": "ROBO",
                "company_name": "Robot Corp",
                "price": 100.50,
                "change_24h": 2.5
            },
            {
                "ticker": "HACK",
                "company_name": "Hacker Guild Inc",
                "price": 75.25,
                "change_24h": -1.2
            }
        ]
        await clean_db.stocks.insert_many(stocks)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/market/stocks",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["stocks"]) >= 2

    @pytest.mark.asyncio
    async def test_buy_stock(self, auth_headers, clean_db):
        """Test buying stocks."""
        # Set player credits
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"currencies.credits": 10000}}
        )

        # Create stock
        stock = {
            "ticker": "ROBO",
            "company_name": "Robot Corp",
            "price": 100.0
        }
        await clean_db.stocks.insert_one(stock)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/market/stocks/buy",
                headers=auth_headers,
                json={
                    "ticker": "ROBO",
                    "quantity": 10
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "portfolio" in data

    @pytest.mark.asyncio
    async def test_sell_stock(self, auth_headers, clean_db):
        """Test selling stocks."""
        # Create player portfolio
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {
                "portfolio": [
                    {"ticker": "ROBO", "quantity": 10, "buy_price": 100.0}
                ]
            }}
        )

        # Create stock
        stock = {
            "ticker": "ROBO",
            "price": 110.0  # Sell at profit
        }
        await clean_db.stocks.insert_one(stock)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/market/stocks/sell",
                headers=auth_headers,
                json={
                    "ticker": "ROBO",
                    "quantity": 5
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "profit" in data


class TestItemMarketplace:
    """Test item marketplace flow."""

    @pytest.mark.asyncio
    async def test_list_item_for_sale(self, auth_headers, clean_db):
        """Test listing an item for sale."""
        # Add item to player inventory
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$push": {
                "items": {
                    "item_id": "health_potion",
                    "quantity": 5
                }
            }}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/market/items/sell",
                headers=auth_headers,
                json={
                    "item_id": "health_potion",
                    "quantity": 2,
                    "price": 50
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "listing_id" in data

    @pytest.mark.asyncio
    async def test_buy_item_from_marketplace(self, auth_headers, clean_db):
        """Test buying an item from marketplace."""
        # Set player credits
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"currencies.credits": 1000}}
        )

        # Create marketplace listing
        listing = {
            "seller_id": "other_user",
            "item_id": "sword_of_power",
            "quantity": 1,
            "price": 500
        }
        result = await clean_db.market_listings.insert_one(listing)
        listing_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/market/items/buy/{listing_id}",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "item" in data