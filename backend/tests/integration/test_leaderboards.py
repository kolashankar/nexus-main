"""Integration tests for leaderboard system."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestLeaderboardFetching:
    """Test fetching various leaderboards."""

    @pytest.mark.asyncio
    async def test_get_karma_leaderboard(self, auth_headers, clean_db):
        """Test getting karma leaderboard."""
        # Create players with different karma
        players = [
            {"username": "player1", "karma_points": 1000},
            {"username": "player2", "karma_points": 500},
            {"username": "player3", "karma_points": 1500}
        ]
        await clean_db.players.insert_many(players)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/leaderboards/karma",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["rankings"]) > 0
            # Should be sorted by karma descending
            assert data["rankings"][0]["karma_points"] >= data["rankings"][-1]["karma_points"]

    @pytest.mark.asyncio
    async def test_get_wealth_leaderboard(self, auth_headers, clean_db):
        """Test getting wealth leaderboard."""
        players = [
            {"username": "rich1", "currencies": {"credits": 100000}},
            {"username": "rich2", "currencies": {"credits": 50000}},
            {"username": "rich3", "currencies": {"credits": 200000}}
        ]
        await clean_db.players.insert_many(players)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/leaderboards/wealth",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["rankings"]) > 0

    @pytest.mark.asyncio
    async def test_get_combat_leaderboard(self, auth_headers, clean_db):
        """Test getting combat leaderboard."""
        players = [
            {"username": "fighter1", "stats": {"pvp_wins": 50, "pvp_losses": 10}},
            {"username": "fighter2", "stats": {"pvp_wins": 30, "pvp_losses": 20}},
            {"username": "fighter3", "stats": {"pvp_wins": 100, "pvp_losses": 15}}
        ]
        await clean_db.players.insert_many(players)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/leaderboards/combat",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["rankings"]) > 0

    @pytest.mark.asyncio
    async def test_leaderboard_pagination(self, auth_headers, clean_db):
        """Test leaderboard pagination."""
        # Create many players
        players = [
            {"username": f"player{i}", "karma_points": i * 100}
            for i in range(50)
        ]
        await clean_db.players.insert_many(players)

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Get first page
            response = await client.get(
                "/api/leaderboards/karma?page=1&limit=10",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["rankings"]) <= 10
            assert "total_pages" in data


class TestPlayerRanking:
    """Test individual player ranking."""

    @pytest.mark.asyncio
    async def test_get_my_rank(self, auth_headers, clean_db):
        """Test getting current player's rank."""
        # Set test user karma
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"karma_points": 750}}
        )

        # Create other players
        players = [
            {"username": "player1", "karma_points": 1000},
            {"username": "player2", "karma_points": 500}
        ]
        await clean_db.players.insert_many(players)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/leaderboards/karma/my-rank",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "rank" in data
            assert data["rank"] == 2  # 2nd place