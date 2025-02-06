from typing import Any, Mapping

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from core.config import settings

client = AsyncIOMotorClient(settings.mongo.url)
mongodb = client[settings.mongo.db_name]

queue_entries_logs_collection = mongodb["queue_entries"]
queue_logs_collection = mongodb["queues"]
users_logs_collection = mongodb["users"]
error_collection = mongodb["errors"]
failed_collection = mongodb["failed_to_get"]


CONNECTION_REGISTRY: dict[str, AsyncIOMotorCollection[Mapping[str, Any]]] = {
    "queues": queue_logs_collection,
    "queue_entries": queue_entries_logs_collection,
    "users": users_logs_collection,
    "errors": error_collection,
    "failed_to_get": failed_collection,
}
