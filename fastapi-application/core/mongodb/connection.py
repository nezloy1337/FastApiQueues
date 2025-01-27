from typing import Type

from motor.motor_asyncio import AsyncIOMotorClient

from core.config import settings

client = AsyncIOMotorClient(settings.mongo.url)
mongodb = client[settings.mongo.db_name]

queue_entries_logs_collection = mongodb["queue_entries"]
queue_logs_collection = mongodb["queues"]
users_logs_collection = mongodb["users"]
error_collection = mongodb["errors"]


CONNECTION_REGISTRY: dict[
    str,
    Type[mongodb],
] = {
    "queues": queue_logs_collection,
    "queue_entries": queue_entries_logs_collection,
    "users": users_logs_collection,
    "errors": error_collection,
}
