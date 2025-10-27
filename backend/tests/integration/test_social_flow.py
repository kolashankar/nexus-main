"""Integration tests for social system flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestAlliances:
    """Test alliance system flow."""

    @pytest.mark.asyncio
    async def test_create_alliance(self, auth_headers, clean_db):
        """Test creating an alliance with another player."""
        # Create target player
        target = {
            "username": "ally_player",
            "email": "ally@example.com"
        }
        await clean_db.players.insert_one(target)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/alliance",
                headers=auth_headers,
                json={
                    "target_username": "ally_player"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "alliance_id" in data

    @pytest.mark.asyncio
    async def test_max_alliance_limit(self, auth_headers, clean_db):
        """Test that alliance limit is enforced (max 3)."""
        # Create player with 3 existing alliances
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {
                "allies": ["ally1", "ally2", "ally3"]
            }}
        )

        # Try to create 4th alliance
        target = {
            "username": "ally4",
            "email": "ally4@example.com"
        }
        await clean_db.players.insert_one(target)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/alliance",
                headers=auth_headers,
                json={
                    "target_username": "ally4"
                }
            )

            assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_break_alliance(self, auth_headers, clean_db):
        """Test breaking an alliance."""
        # Create alliance
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$push": {"allies": "ally_player"}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.delete(
                "/api/social/alliance/ally_player",
                headers=auth_headers
            )

            assert response.status_code == 200


class TestMarriage:
    """Test marriage system flow."""

    @pytest.mark.asyncio
    async def test_propose_marriage(self, auth_headers, clean_db):
        """Test proposing marriage to another player."""
        # Create target player
        target = {
            "username": "soulmate",
            "email": "soulmate@example.com"
        }
        await clean_db.players.insert_one(target)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/marry",
                headers=auth_headers,
                json={
                    "target_username": "soulmate"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "proposal_id" in data

    @pytest.mark.asyncio
    async def test_divorce(self, auth_headers, clean_db):
        """Test divorcing a spouse."""
        # Set up marriage
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"spouse_id": "spouse_user"}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/divorce",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert "karma_cost" in data  # Divorce has karma cost


class TestMentorship:
    """Test mentorship system flow."""

    @pytest.mark.asyncio
    async def test_request_mentorship(self, auth_headers, clean_db):
        """Test requesting mentorship from veteran player."""
        # Create veteran player
        veteran = {
            "username": "veteran_player",
            "email": "veteran@example.com",
            "level": 50,
            "can_mentor": True
        }
        await clean_db.players.insert_one(veteran)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/mentor/request",
                headers=auth_headers,
                json={
                    "mentor_username": "veteran_player"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "request_id" in data

    @pytest.mark.asyncio
    async def test_graduate_apprentice(self, auth_headers, clean_db):
        """Test graduating an apprentice."""
        # Set up mentorship
        apprentice = {
            "username": "apprentice",
            "email": "apprentice@example.com",
            "mentor_id": "test_user",
            "level": 50  # Reached graduation level
        }
        await clean_db.players.insert_one(apprentice)

        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$push": {"apprentices": "apprentice"}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/social/mentor/graduate",
                headers=auth_headers,
                json={
                    "apprentice_username": "apprentice"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "legacy_points" in data  # Mentor gets legacy points