"""Integration tests for guild system flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestGuildCreation:
    """Test guild creation flow."""

    @pytest.mark.asyncio
    async def test_create_guild(self, auth_headers, clean_db):
        """Test creating a new guild."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/guilds/create",
                headers=auth_headers,
                json={
                    "name": "Test Guild",
                    "tag": "TEST",
                    "description": "A test guild for testing"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["name"] == "Test Guild"
            assert data["tag"] == "TEST"
            assert data["leader_id"] == "test_user"

    @pytest.mark.asyncio
    async def test_cannot_create_guild_with_duplicate_name(self, auth_headers, clean_db):
        """Test that duplicate guild names are rejected."""
        # Create first guild
        guild = {
            "name": "Existing Guild",
            "tag": "EXST",
            "leader_id": "other_user"
        }
        await clean_db.guilds.insert_one(guild)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/guilds/create",
                headers=auth_headers,
                json={
                    "name": "Existing Guild",
                    "tag": "TEST"
                }
            )

            assert response.status_code == 400


class TestGuildMembership:
    """Test guild membership flow."""

    @pytest.mark.asyncio
    async def test_join_guild(self, auth_headers, clean_db):
        """Test joining a guild."""
        # Create guild
        guild = {
            "name": "Open Guild",
            "tag": "OPEN",
            "leader_id": "leader_user",
            "recruitment_open": True,
            "members": [{"player_id": "leader_user", "rank": "leader"}]
        }
        result = await clean_db.guilds.insert_one(guild)
        guild_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/guilds/{guild_id}/join",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert any(m["player_id"] == "test_user" for m in data["members"])

    @pytest.mark.asyncio
    async def test_leave_guild(self, auth_headers, clean_db):
        """Test leaving a guild."""
        # Create guild with player as member
        guild = {
            "name": "Test Guild",
            "tag": "TEST",
            "leader_id": "leader_user",
            "members": [
                {"player_id": "leader_user", "rank": "leader"},
                {"player_id": "test_user", "rank": "member"}
            ]
        }
        result = await clean_db.guilds.insert_one(guild)
        guild_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/guilds/{guild_id}/leave",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert not any(m["player_id"] ==
                           "test_user" for m in data["members"])


class TestGuildWars:
    """Test guild war flow."""

    @pytest.mark.asyncio
    async def test_declare_war(self, auth_headers, clean_db):
        """Test declaring war on another guild."""
        # Create attacker guild (test_user is leader)
        guild1 = {
            "name": "Attacker Guild",
            "tag": "ATK",
            "leader_id": "test_user",
            "members": [{"player_id": "test_user", "rank": "leader"}],
            "active_wars": []
        }
        result1 = await clean_db.guilds.insert_one(guild1)
        guild1_id = str(result1.inserted_id)

        # Create target guild
        guild2 = {
            "name": "Target Guild",
            "tag": "TGT",
            "leader_id": "other_user",
            "members": [{"player_id": "other_user", "rank": "leader"}]
        }
        result2 = await clean_db.guilds.insert_one(guild2)
        guild2_id = str(result2.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/guilds/{guild1_id}/declare-war",
                headers=auth_headers,
                json={
                    "enemy_guild_id": guild2_id
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["active_wars"]) == 1
            assert data["active_wars"][0]["enemy_guild_id"] == guild2_id