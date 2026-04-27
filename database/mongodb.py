from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGODB_URL, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect(self):
        try:
            self.client = AsyncIOMotorClient(MONGODB_URL)
            self.db = self.client[DATABASE_NAME]
            # Test the connection
            await self.client.admin.command('ping')
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    async def disconnect(self):
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")

    def get_collection(self, collection_name):
        return self.db[collection_name]

# Global instance
mongodb = MongoDB()