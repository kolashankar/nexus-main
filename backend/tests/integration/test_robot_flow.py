"""Integration tests for robot system flow."""
import pytest
from httpx import AsyncClient
from backend.server import app


class TestRobotPurchase:
    """Test robot purchase flow."""

    @pytest.mark.asyncio
    async def test_purchase_robot_from_marketplace(self, auth_headers, clean_db):
        """Test purchasing a robot from marketplace."""
        # Set player credits
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"currencies.credits": 10000}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/robots/purchase",
                headers=auth_headers,
                json={
                    "robot_type": "harvester"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert "robot_id" in data
            assert data["robot"]["type"] == "harvester"

    @pytest.mark.asyncio
    async def test_cannot_purchase_without_credits(self, auth_headers, clean_db):
        """Test that purchase fails without sufficient credits."""
        # Set player credits low
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"currencies.credits": 100}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/robots/purchase",
                headers=auth_headers,
                json={
                    "robot_type": "sentinel_prime"  # Expensive robot
                }
            )

            assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_robot_added_to_inventory(self, auth_headers, clean_db):
        """Test that purchased robot is added to inventory."""
        await clean_db.players.update_one(
            {"username": "test_user"},
            {"$set": {"currencies.credits": 10000}}
        )

        async with AsyncClient(app=app, base_url="http://test") as client:
            # Purchase robot
            await client.post(
                "/api/robots/purchase",
                headers=auth_headers,
                json={"robot_type": "harvester"}
            )

            # Check inventory
            inventory_response = await client.get(
                "/api/robots/my-robots",
                headers=auth_headers
            )

            assert inventory_response.status_code == 200
            inventory = inventory_response.json()
            assert len(inventory["robots"]) > 0


class TestRobotTraining:
    """Test robot training flow."""

    @pytest.mark.asyncio
    async def test_train_robot(self, auth_headers, clean_db):
        """Test training a robot to increase XP."""
        # Create robot
        robot = {
            "owner_id": "test_user",
            "type": "harvester",
            "level": 1,
            "xp": 0
        }
        result = await clean_db.robots.insert_one(robot)
        robot_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/robots/{robot_id}/train",
                headers=auth_headers,
                json={
                    "training_type": "basic"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["xp"] > 0

    @pytest.mark.asyncio
    async def test_robot_levels_up(self, auth_headers, clean_db):
        """Test robot leveling up after training."""
        robot = {
            "owner_id": "test_user",
            "type": "guardian",
            "level": 1,
            "xp": 900  # Close to level up
        }
        result = await clean_db.robots.insert_one(robot)
        robot_id = str(result.inserted_id)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                f"/api/robots/{robot_id}/train",
                headers=auth_headers,
                json={
                    "training_type": "intensive"
                }
            )

            data = response.json()
            # Should level up if enough XP gained
            if data["xp"] >= 1000:
                assert data["level"] > 1


class TestRobotFusion:
    """Test robot fusion flow."""

    @pytest.mark.asyncio
    async def test_fuse_two_robots(self, auth_headers, clean_db):
        """Test fusing two robots to create stronger one."""
        # Create two robots
        robot1 = {
            "owner_id": "test_user",
            "type": "harvester",
            "level": 5,
            "xp": 500
        }
        robot2 = {
            "owner_id": "test_user",
            "type": "harvester",
            "level": 4,
            "xp": 300
        }

        result1 = await clean_db.robots.insert_one(robot1)
        result2 = await clean_db.robots.insert_one(robot2)

        async with AsyncClient(app=app, base_url="http://test") as client:
            response = await client.post(
                "/api/robots/fuse",
                headers=auth_headers,
                json={
                    "robot1_id": str(result1.inserted_id),
                    "robot2_id": str(result2.inserted_id)
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["fused_robot"]["level"] >= 5
            assert data["fused_robot"]["xp"] >= 800