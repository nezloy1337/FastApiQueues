from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings

client = AsyncIOMotorClient(settings.mongo.url)
mongodb = client[settings.mongo.db_name]

queue_logs_collection = mongodb["queue_entries"]
error_collection = mongodb['errors']