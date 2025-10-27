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
            cls.client = AsyncIOMotorClient(settings.MONGO_URL)
            logger.info("Connected to MongoDB")
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
    return Database.get_db()

# Alias for backward compatibility
db = Database.get_db()
