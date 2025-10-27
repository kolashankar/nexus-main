import pytest
import asyncio
from typing import AsyncGenerator, Generator
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
import os

# Import app components
from server import app
from backend.core.database import get_database

# Test database name
TEST_DB_NAME = "karma_nexus_test"


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db_client() -> AsyncGenerator:
    """Create test database client"""
    mongo_url = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    client = AsyncIOMotorClient(mongo_url)
    yield client

    # Cleanup: drop test database
    await client.drop_database(TEST_DB_NAME)
    client.close()


@pytest.fixture(scope="function")
async def test_db(test_db_client):
    """Get test database"""
    db = test_db_client[TEST_DB_NAME]

    # Clear all collections before each test
    for collection_name in await db.list_collection_names():
        await db[collection_name].delete_many({})

    yield db


@pytest.fixture(scope="function")
async def client(test_db) -> AsyncGenerator:
    """Create test client"""
    # Override database dependency
    app.dependency_overrides[get_database] = lambda: test_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(test_db):
    """Create a test user"""
    from core.security import get_password_hash

    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": get_password_hash("testpass123"),
        "karma_points": 0,
        "level": 1,
        "xp": 0,
        "economic_class": "middle",
        "moral_class": "average",
        "currencies": {
            "credits": 10000,
            "karma_tokens": 0,
            "dark_matter": 0,
            "prestige_points": 0,
            "guild_coins": 0,
            "legacy_shards": 0,
        },
        "traits": {
            # Initialize all traits at 50
            **{f"trait_{i}": 50 for i in range(1, 61)}
        },
        "meta_traits": {
            **{f"meta_trait_{i}": 50 for i in range(1, 21)}
        },
        "visibility": {
            "privacy_tier": "public",
            "cash": True,
            "karma_score": True,
        },
    }

    result = await test_db["players"].insert_one(user_data)
    user_data["_id"] = result.inserted_id

    return user_data


@pytest.fixture
async def auth_token(client, test_user):
    """Get authentication token for test user"""
    response = await client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "testpass123",
        },
    )

    data = response.json()
    return data["access_token"]


@pytest.fixture
async def auth_headers(auth_token):
    """Get authentication headers"""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def test_robot(test_db, test_user):
    """Create a test robot"""
    robot_data = {
        "owner_id": test_user["_id"],
        "name": "Test Robot",
        "class": "worker",
        "level": 1,
        "xp": 0,
        "stats": {
            "efficiency": 50,
            "durability": 50,
            "speed": 50,
        },
        "price": 1000,
    }

    result = await test_db["robots"].insert_one(robot_data)
    robot_data["_id"] = result.inserted_id

    return robot_data


@pytest.fixture
async def test_guild(test_db, test_user):
    """Create a test guild"""
    guild_data = {
        "name": "Test Guild",
        "tag": "TST",
        "description": "A test guild",
        "leader_id": test_user["_id"],
        "members": [
            {
                "player_id": test_user["_id"],
                "rank": "leader",
                "contribution": 0,
            }
        ],
        "total_members": 1,
        "max_members": 10,
        "level": 1,
        "xp": 0,
        "guild_bank": {
            "credits": 0,
        },
        "controlled_territories": [],
        "guild_karma": 0,
    }

    result = await test_db["guilds"].insert_one(guild_data)
    guild_data["_id"] = result.inserted_id

    return guild_data


@pytest.fixture
async def test_quest(test_db, test_user):
    """Create a test quest"""
    quest_data = {
        "quest_type": "personal",
        "title": "Test Quest",
        "description": "A test quest description",
        "lore": "Test quest lore",
        "player_id": test_user["_id"],
        "status": "available",
        "objectives": [
            {
                "description": "Complete test objective",
                "type": "collect",
                "target": "test_item",
                "current": 0,
                "required": 5,
                "completed": False,
            }
        ],
        "rewards": {
            "credits": 1000,
            "xp": 500,
            "karma": 10,
        },
    }

    result = await test_db["quests"].insert_one(quest_data)
    quest_data["_id"] = result.inserted_id

    return quest_data


# Helper functions
def assert_success_response(response):
    """Assert that response is successful"""
    assert response.status_code in [
        200, 201], f"Expected success, got {response.status_code}: {response.text}"


def assert_error_response(response, expected_status=400):
    """Assert that response is an error"""
    assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"
