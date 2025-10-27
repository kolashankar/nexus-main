"""E2E test for complete player journey."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestNewPlayerJourney:
    """Test a new player's complete journey through the game."""

    @pytest.mark.asyncio
    async def test_complete_new_player_flow(self, clean_db):
        """Test complete flow: register -> explore -> quest -> combat -> guild."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # 1. Register new player
            register_response = await client.post("/api/auth/register", json={
                "username": "newplayer",
                "email": "newplayer@example.com",
                "password": "securepass123"
            })
            assert register_response.status_code == 200
            token = register_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # 2. View profile
            profile_response = await client.get("/api/player/profile", headers=headers)
            assert profile_response.status_code == 200
            assert profile_response.json()["username"] == "newplayer"

            # 3. Create target player for interactions
            target = {
                "username": "target",
                "email": "target@example.com",
                "currencies": {"credits": 1000},
                "moral_class": "poor"
            }
            await clean_db.players.insert_one(target)

            # 4. Perform help action (positive karma)
            help_response = await client.post(
                "/api/actions/help",
                headers=headers,
                json={"target_username": "target", "amount": 100}
            )
            assert help_response.status_code == 200
            assert help_response.json()["karma_change"] > 0

            # 5. Generate daily quests
            quest_response = await client.post(
                "/api/quests/daily/generate",
                headers=headers
            )
            assert quest_response.status_code == 200

            # 6. Purchase a robot
            robot_response = await client.post(
                "/api/robots/purchase",
                headers=headers,
                json={"robot_type": "harvester"}
            )
            assert robot_response.status_code == 200

            # 7. Create a guild
            guild_response = await client.post(
                "/api/guilds/create",
                headers=headers,
                json={
                    "name": "Newbie Guild",
                    "tag": "NEWB",
                    "description": "A guild for new players"
                }
            )
            assert guild_response.status_code == 200

            # 8. Check final profile state
            final_profile = await client.get("/api/player/profile", headers=headers)
            profile_data = final_profile.json()

            # Verify state changes
            assert profile_data["karma_points"] > 0
            assert len(profile_data["robots"]) > 0
            assert profile_data["guild_id"] is not None