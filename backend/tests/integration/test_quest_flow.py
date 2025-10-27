"""Integration tests for quest system flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestQuestGeneration:
    """Test quest generation flow."""

    @pytest.mark.asyncio
    async def test_generate_daily_quests(self, auth_headers, clean_db):
        """Test generating daily quests for player."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/quests/daily/generate",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["quests"]) <= 3  # Max 3 daily quests

            for quest in data["quests"]:
                assert "title" in quest
                assert "objectives" in quest
                assert "rewards" in quest

    @pytest.mark.asyncio
    async def test_get_available_quests(self, auth_headers, clean_db):
        """Test getting list of available quests."""
        # Create some quests
        quests = [
            {
                "player_id": "test_user",
                "quest_type": "daily",
                "title": "Test Quest 1",
                "status": "available"
            },
            {
                "player_id": "test_user",
                "quest_type": "weekly",
                "title": "Test Quest 2",
                "status": "available"
            }
        ]
        await clean_db.quests.insert_many(quests)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.get(
                "/api/quests/available",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert len(data["quests"]) >= 2


class TestQuestAcceptance:
    """Test quest acceptance and activation."""

    @pytest.mark.asyncio
    async def test_accept_quest(self, auth_headers, clean_db):
        """Test accepting a quest."""
        # Create quest
        quest = {
            "player_id": "test_user",
            "quest_type": "personal",
            "title": "Test Quest",
            "status": "available",
            "objectives": [
                {"description": "Complete task", "current": 0, "required": 1}
            ]
        }
        result = await clean_db.quests.insert_one(quest)
        quest_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/quests/{quest_id}/accept",
                headers=auth_headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "active"

    @pytest.mark.asyncio
    async def test_cannot_accept_quest_twice(self, auth_headers, clean_db):
        """Test that quest cannot be accepted twice."""
        quest = {
            "player_id": "test_user",
            "status": "active",
            "title": "Active Quest"
        }
        result = await clean_db.quests.insert_one(quest)
        quest_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/quests/{quest_id}/accept",
                headers=auth_headers
            )

            assert response.status_code == 400


class TestQuestCompletion:
    """Test quest completion flow."""

    @pytest.mark.asyncio
    async def test_complete_quest_with_rewards(self, auth_headers, clean_db):
        """Test completing a quest and receiving rewards."""
        # Get player's current credits
        player = await clean_db.players.find_one({"username": "test_user"})
        original_credits = player["currencies"]["credits"]
        original_xp = player.get("xp", 0)

        # Create completed quest
        quest = {
            "player_id": "test_user",
            "status": "active",
            "title": "Test Quest",
            "objectives": [
                {"description": "Task", "current": 1,
                    "required": 1, "completed": True}
            ],
            "rewards": {
                "credits": 500,
                "xp": 100,
                "karma": 10
            }
        }
        result = await clean_db.quests.insert_one(quest)
        quest_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/quests/{quest_id}/complete",
                headers=auth_headers
            )

            assert response.status_code == 200
            response.json()

            # Check rewards were given
            player_after = await clean_db.players.find_one({"username": "test_user"})
            assert player_after["currencies"]["credits"] == original_credits + 500
            assert player_after["xp"] == original_xp + 100