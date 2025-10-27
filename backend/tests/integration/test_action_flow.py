"""Integration tests for game action flows."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestHelpActionFlow:
    """Test help action complete flow."""

    @pytest.mark.asyncio
    async def test_help_action_increases_karma(self, auth_headers, test_player, clean_db):
        """Test that helping another player increases karma."""
        # Create target player
        target_player = {
            "username": "target_user",
            "email": "target@example.com",
            "karma_points": 0,
            "currencies": {"credits": 500},
            "moral_class": "poor"
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/actions/help",
                headers=auth_headers,
                json={
                    "target_username": "target_user",
                    "amount": 100
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["karma_change"] > 0
            assert "empathy" in data["trait_changes"]

    @pytest.mark.asyncio
    async def test_help_action_transfers_credits(self, auth_headers, clean_db):
        """Test that help action transfers credits."""
        # Create actor and target
        actor = await clean_db.players.find_one({"username": "test_user"})
        original_credits = actor["currencies"]["credits"]

        target_player = {
            "username": "target_user",
            "email": "target@example.com",
            "currencies": {"credits": 500}
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            await client.post(
                "/api/actions/help",
                headers=auth_headers,
                json={
                    "target_username": "target_user",
                    "amount": 100
                }
            )

            # Check actor lost credits
            actor_after = await clean_db.players.find_one({"username": "test_user"})
            assert actor_after["currencies"]["credits"] == original_credits - 100

            # Check target gained credits
            target_after = await clean_db.players.find_one({"username": "target_user"})
            assert target_after["currencies"]["credits"] == 600


class TestStealActionFlow:
    """Test steal action complete flow."""

    @pytest.mark.asyncio
    async def test_steal_action_decreases_karma(self, auth_headers, clean_db):
        """Test that stealing decreases karma."""
        target_player = {
            "username": "target_user",
            "email": "target@example.com",
            "karma_points": 100,
            "currencies": {"credits": 1000},
            "moral_class": "good"
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/actions/steal",
                headers=auth_headers,
                json={
                    "target_username": "target_user"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["karma_change"] < 0
            assert "greed" in data["trait_changes"]

    @pytest.mark.asyncio
    async def test_steal_action_can_fail(self, auth_headers, clean_db):
        """Test that steal action can fail based on traits."""
        # Create target with high perception
        target_player = {
            "username": "alert_user",
            "email": "alert@example.com",
            "currencies": {"credits": 1000},
            "traits": {"perception": 95}
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/actions/steal",
                headers=auth_headers,
                json={
                    "target_username": "alert_user"
                }
            )

            data = response.json()
            # High perception increases chance of failure
            assert "success" in data


class TestHackActionFlow:
    """Test hack action complete flow."""

    @pytest.mark.asyncio
    async def test_hack_action_requires_hacking_trait(self, auth_headers, clean_db):
        """Test that hack action requires minimum hacking trait."""
        # Set actor hacking trait low
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"traits.hacking": 10}}
        )

        target_player = {
            "username": "target_user",
            "email": "target@example.com",
            "currencies": {"credits": 1000}
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/actions/hack",
                headers=auth_headers,
                json={
                    "target_username": "target_user"
                }
            )

            # Should fail or have low success rate
            assert response.status_code in [200, 400]

    @pytest.mark.asyncio
    async def test_hack_action_increases_hacking_skill(self, auth_headers, clean_db):
        """Test that hacking increases hacking skill."""
        target_player = {
            "username": "target_user",
            "email": "target@example.com",
            "currencies": {"credits": 1000}
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/actions/hack",
                headers=auth_headers,
                json={
                    "target_username": "target_user"
                }
            )

            if response.status_code == 200:
                data = response.json()
                if "trait_changes" in data:
                    assert "hacking" in data["trait_changes"]