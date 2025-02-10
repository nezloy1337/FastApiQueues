from datetime import datetime
from typing import Literal, Mapping, Union

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from core.config import settings

# Define collection names and serializable types
CollectionName = Literal["queues", "queue_entries", "users", "errors", "failed_to_get"]
JSONSerializable = Union[str, int, float, bool, list, dict, None, datetime, ObjectId]


class MongoConnectionManager:
    """
    Manages MongoDB connection and provides access to predefined collections.
    """

    def __init__(self, url: str, db_name: str) -> None:
        self.client = AsyncIOMotorClient(
            url,
            uuidRepresentation="standard",
        )

        self.db = self.client[db_name]

        self._registry: dict[
            CollectionName,
            AsyncIOMotorCollection[Mapping[str, JSONSerializable]],
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
        """
        Retrieves an AsyncIOMotorCollection for the given collection name.
        """
        return self._registry[name]


def get_mongo_manager() -> MongoConnectionManager:
    """
    Creates and returns a MongoConnectionManager instance.
    """
    return MongoConnectionManager(settings.mongo.url, settings.mongo.db_name)
