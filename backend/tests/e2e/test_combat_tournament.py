"""E2E test for combat tournament."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestCombatTournament:
    """Test complete tournament flow."""

    @pytest.mark.asyncio
    async def test_tournament_participation(self, clean_db):
        """Test registering for and participating in a tournament."""
        async with AsyncClient(app=app, base_url="http://test") as client:
            # Create tournament
            tournament = {
                "name": "Weekly PvP Championship",
                "type": "single_elimination",
                "status": "registration",
                "max_participants": 8,
                "participants": []
            }
            result = await clean_db.tournaments.insert_one(tournament)
            tournament_id = str(result.inserted_id)

            # Register 4 players
            players = []
            for i in range(4):
                username = f"fighter{i}"
                register_response = await client.post("/api/auth/register", json={
                    "username": username,
                    "email": f"{username}@example.com",
                    "password": "pass123"
                })
                token = register_response.json()["access_token"]
                players.append({"username": username, "token": token})

                # Register for tournament
                headers = {"Authorization": f"Bearer {token}"}
                tournament_register = await client.post(
                    f"/api/tournaments/{tournament_id}/register",
                    headers=headers
                )
                assert tournament_register.status_code == 200

            # Check tournament participants
            tournament_status = await client.get(
                f"/api/tournaments/{tournament_id}",
                headers={"Authorization": f"Bearer {players[0]['token']}"}
            )
            assert len(tournament_status.json()["participants"]) == 4

            # Start tournament (change status to active)
            await clean_db.tournaments.update_one(
                {"_id": result.inserted_id},
                {"$set": {"status": "active"}}
            )

            # Check bracket
            bracket_response = await client.get(
                f"/api/tournaments/{tournament_id}/bracket",
                headers={"Authorization": f"Bearer {players[0]['token']}"}
            )
            assert bracket_response.status_code == 200