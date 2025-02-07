import asyncio
from datetime import datetime

import bson
from bson import ObjectId
from pydantic import BaseModel, Field

from core.mongodb.connection import CONNECTION_REGISTRY, failed_collection
from core.mongodb.schemas import ActionLog
from tasks.celery_app import celery_app, log


class ErrorLog(BaseModel):
    error: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


async def async_process_log(log_data):
    collection_name = log_data.pop("collection_name")
    log_entry = ActionLog(**log_data)
    log_entry.parameters["user"]["id"] = bson.Binary.from_uuid(
        log_entry.parameters["user"]["id"]
    )
    collection_to_log = CONNECTION_REGISTRY.get(collection_name)

    if collection_to_log is not None:
        await collection_to_log.insert_one(log_data)
    else:
        await failed_collection.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_log", max_retries=3)
def process_log(self, log_data):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():  # Проверяем, закрыт ли event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(async_process_log(log_data))

    except Exception as e:
        log.error(e)


async def async_process_error_log(log_data):
    collection_to_log = CONNECTION_REGISTRY.get("errors")

    if collection_to_log is not None:
        await collection_to_log.insert_one(log_data)
    else:
        await failed_collection.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_error", max_retries=3)
def process_error(self, log_data):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():  # Проверяем, закрыт ли event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(async_process_error_log(log_data))

    except Exception as e:
        log.error(str(e))
