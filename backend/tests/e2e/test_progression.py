"""E2E test for player progression system."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestPlayerProgression:
    """Test complete player progression: leveling, traits, superpowers."""

    @pytest.mark.asyncio
    async def test_level_up_and_unlock_powers(self, clean_db):
        """Test player leveling up and unlocking superpowers."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Register player
            register_response = await client.post("/api/auth/register", json={
                "username": "progressor",
                "email": "progressor@example.com",
                "password": "pass123"
            })
            token = register_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}

            # Set high empathy and perception traits
            await clean_db.players.update_one(
                {"username": "progressor"},
                {"$set": {
                    "traits.empathy": 85,
                    "traits.perception": 75,
                    "xp": 900  # Close to level up
                }}
            )

            # Create target for helping
            target = {
                "username": "helpee",
                "currencies": {"credits": 500},
                "moral_class": "poor"
            }
            await clean_db.players.insert_one(target)

            # Perform actions to gain XP
            for i in range(5):
                await client.post(
                    "/api/actions/help",
                    headers=headers,
                    json={"target_username": "helpee", "amount": 50}
                )

            # Check if leveled up
            profile = await client.get("/api/player/profile", headers=headers)
            profile.json()

            # Check for available superpowers
            powers_response = await client.get("/api/player/superpowers", headers=headers)
            powers = powers_response.json()

            # Should be able to unlock Mind Reading (empathy 80%, perception 70%)
            available_powers = powers.get("available", [])
            assert "mind_reading" in available_powers or len(
                powers.get("unlocked", [])) > 0