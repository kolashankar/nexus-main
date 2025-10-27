"""E2E test for economy system."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestEconomySystem:
    """Test complete economy flow: earning, spending, trading."""

    @pytest.mark.asyncio
    async def test_full_economy_cycle(self, clean_db):
        """Test earning credits, buying items, trading stocks."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Register player
            register_response = await client.post("/api/auth/register", json={
                "username": "trader",
                "email": "trader@example.com",
                "password": "pass123"
            })
            token = register_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # Give initial credits
            await clean_db.players.update_one(
                {"username": "trader"},
                {"$set": {"currencies.credits": 10000}}
            )

            # 1. Buy a robot (spending credits)
            robot_response = await client.post(
                "/api/robots/purchase",
                headers=headers,
                json={"robot_type": "harvester"}
            )
            assert robot_response.status_code == 200

            # 2. Create and buy stocks
            stock = {
                "ticker": "ROBO",
                "company_name": "Robot Corp",
                "price": 100.0
            }
            await clean_db.stocks.insert_one(stock)

            stock_buy_response = await client.post(
                "/api/market/stocks/buy",
                headers=headers,
                json={"ticker": "ROBO", "quantity": 10}
            )
            assert stock_buy_response.status_code == 200

            # 3. Update stock price (simulate market)
            await clean_db.stocks.update_one(
                {"ticker": "ROBO"},
                {"$set": {"price": 120.0}}  # Price increased
            )

            # 4. Sell stocks at profit
            stock_sell_response = await client.post(
                "/api/market/stocks/sell",
                headers=headers,
                json={"ticker": "ROBO", "quantity": 5}
            )

            if stock_sell_response.status_code == 200:
                profit = stock_sell_response.json().get("profit", 0)
                assert profit > 0  # Made profit from selling

            # 5. Check final balance
            final_profile = await client.get("/api/player/profile", headers=headers)
            final_credits = final_profile.json()["currencies"]["credits"]

            # Should have spent on robot, earned from stocks
            assert final_credits != 10000  # Balance changed