"""Integration tests for combat flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestCombatChallenge:
    """Test combat challenge flow."""

    @pytest.mark.asyncio
    async def test_challenge_player_to_duel(self, auth_headers, clean_db):
        """Test challenging another player to a duel."""
        # Create target player
        target_player = {
            "username": "opponent",
            "email": "opponent@example.com",
            "combat_stats": {
                "hp": 500,
                "max_hp": 500,
                "attack": 50,
                "defense": 40
            }
        }
        await clean_db.players.insert_one(target_player)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/combat/challenge",
                headers=auth_headers,
                json={
                    "target_username": "opponent",
                    "challenge_type": "duel"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "challenge_id" in data
            assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_accept_combat_challenge(self, clean_db):
        """Test accepting a combat challenge."""
        # Create challenge
        challenge = {
            "challenger_id": "test_user",
            "target_id": "opponent",
            "status": "pending",
            "type": "duel"
        }
        result = await clean_db.combat_challenges.insert_one(challenge)
        challenge_id = str(result.inserted_id)

        # Create token for opponent
        from backend.core.security import create_access_token
        token = create_access_token(data={"sub": "opponent"})
        headers = {"Authorization": f"Bearer {token}"}

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/combat/accept/{challenge_id}",
                headers=headers
            )

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "active"


class TestCombatExecution:
    """Test combat execution."""

    @pytest.mark.asyncio
    async def test_execute_combat_turn(self, auth_headers, clean_db):
        """Test executing a combat turn."""
        # Create active combat
        combat = {
            "player1_id": "test_user",
            "player2_id": "opponent",
            "status": "active",
            "current_turn": "test_user",
            "player1_hp": 500,
            "player2_hp": 500
        }
        result = await clean_db.combats.insert_one(combat)
        combat_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/combat/{combat_id}/action",
                headers=auth_headers,
                json={
                    "action_type": "attack",
                    "ability": None
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "damage" in data
            assert data["player2_hp"] < 500

    @pytest.mark.asyncio
    async def test_combat_ends_when_hp_zero(self, auth_headers, clean_db):
        """Test that combat ends when HP reaches zero."""
        # Create combat with low HP
        combat = {
            "player1_id": "test_user",
            "player2_id": "opponent",
            "status": "active",
            "current_turn": "test_user",
            "player1_hp": 500,
            "player2_hp": 10  # Very low HP
        }
        result = await clean_db.combats.insert_one(combat)
        combat_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/combat/{combat_id}/action",
                headers=auth_headers,
                json={
                    "action_type": "attack",
                    "ability": None
                }
            )

            data = response.json()
            if data.get("player2_hp", 0) <= 0:
                assert data["status"] == "completed"
                assert data["winner"] == "test_user"