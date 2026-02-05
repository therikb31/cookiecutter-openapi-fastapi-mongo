from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional


class MongoManager:
    _client: Optional[AsyncIOMotorClient] = None

    @classmethod
    def connect(cls, uri: str):
        """Connect to MongoDB."""
        cls._client = AsyncIOMotorClient(uri)

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        """Get the MongoDB client. Raises exception if not connected."""
        if cls._client is None:
            raise RuntimeError(
                "MongoDB client is not initialized. Call connect() first."
            )
        return cls._client

    @classmethod
    def close(cls):
        """Close the MongoDB connection."""
        if cls._client:
            cls._client.close()
            cls._client = None
