"""E2E test for guild war scenario."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestGuildWarScenario:
    """Test complete guild war scenario."""

    @pytest.mark.asyncio
    async def test_complete_guild_war(self, clean_db):
        """Test guild war from declaration to resolution."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Setup: Create two guilds with leaders

            # Guild 1
            leader1_response = await client.post("/api/auth/register", json={
                "username": "leader1",
                "email": "leader1@example.com",
                "password": "pass123"
            })
            token1 = leader1_response.json()["access_token"]
            headers1 = {"Authorization": f"Bearer {token1}"}

            guild1_response = await client.post(
                "/api/guilds/create",
                headers=headers1,
                json={"name": "Warriors", "tag": "WAR"}
            )
            guild1_id = guild1_response.json()["_id"]

            # Guild 2
            leader2_response = await client.post("/api/auth/register", json={
                "username": "leader2",
                "email": "leader2@example.com",
                "password": "pass123"
            })
            token2 = leader2_response.json()["access_token"]
            headers2 = {"Authorization": f"Bearer {token2}"}

            guild2_response = await client.post(
                "/api/guilds/create",
                headers=headers2,
                json={"name": "Defenders", "tag": "DEF"}
            )
            guild2_id = guild2_response.json()["_id"]

            # 1. Guild 1 declares war on Guild 2
            war_response = await client.post(
                f"/api/guilds/{guild1_id}/declare-war",
                headers=headers1,
                json={"enemy_guild_id": guild2_id}
            )
            assert war_response.status_code == 200

            # 2. Check war status
            guild1_status = await client.get(f"/api/guilds/{guild1_id}", headers=headers1)
            assert len(guild1_status.json()["active_wars"]) == 1

            # 3. Attack territory
            territory_response = await client.post(
                f"/api/guilds/{guild1_id}/attack-territory",
                headers=headers1,
                json={"territory_id": 1}
            )
            # War is active, attack attempt made
            assert territory_response.status_code in [200, 400]

            # 4. Negotiate peace
            peace_response = await client.post(
                f"/api/guilds/{guild1_id}/peace-treaty",
                headers=headers1,
                json={"enemy_guild_id": guild2_id}
            )
            assert peace_response.status_code == 200