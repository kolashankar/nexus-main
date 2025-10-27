from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from .config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: Optional[AsyncIOMotorClient] = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls.client is None:
            # Use serverSelectionTimeoutMS to fail fast if MongoDB is unreachable
            cls.client = AsyncIOMotorClient(
                settings.MONGO_URL,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000
            )
            logger.info("MongoDB client initialized")
        return cls.client

    @classmethod
    def get_db(cls):
        client = cls.get_client()
        return client[settings.DB_NAME]

    @classmethod
    async def close(cls):
        if cls.client:
            cls.client.close()
            logger.info("Closed MongoDB connection")

def get_database():
    """Dependency for getting database instance."""
    return Database.get_db()
