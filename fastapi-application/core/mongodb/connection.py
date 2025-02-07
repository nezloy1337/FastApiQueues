from datetime import datetime
from typing import Literal, Mapping, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from core.config import settings

CollectionName = Literal["queues", "queue_entries", "users", "errors", "failed_to_get"]

# Определяем тип документа MongoDB
JSONSerializable = Union[str, int, float, bool, list, dict, None, datetime, ObjectId]


class MongoConnectionManager:
    def __init__(self, url: str, db_name: str) -> None:
        self.client = AsyncIOMotorClient(url)
        self.db = self.client[db_name]
        self._registry: dict[
            CollectionName, AsyncIOMotorCollection[Mapping[str, JSONSerializable]]
        ] = {
            "queues": self.db["queues"],
            "queue_entries": self.db["queue_entries"],
            "users": self.db["users"],
            "errors": self.db["errors"],
            "failed_to_get": self.db["failed_to_get"],
        }

    def get_collection(
        self, name: CollectionName
    ) -> AsyncIOMotorCollection[Mapping[str, JSONSerializable]]:
        return self._registry[name]


def get_mongo_manager() -> MongoConnectionManager:
    return MongoConnectionManager(settings.mongo.url, settings.mongo.db_name)
