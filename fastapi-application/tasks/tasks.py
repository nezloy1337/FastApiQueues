import asyncio
from datetime import datetime
from typing import Any, SupportsBytes

import bson
from bson import ObjectId
from celery import Task
from pydantic import BaseModel, Field

from core.mongodb.connection import get_mongo_manager
from core.mongodb.schemas import ActionLog
from tasks.celery_app import celery_app, log


class ErrorLog(BaseModel):
    error: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


async def async_process_log(log_data: dict[str, Any]) -> None:
    collection_name = log_data.pop("collection_name")
    log_entry = ActionLog(**log_data)
    log_entry.parameters["user"]["id"] = bson.Binary.from_uuid(
        log_entry.parameters["user"]["id"]
    )
    mongo_manager = get_mongo_manager()
    collection_to_log = mongo_manager.get_collection(collection_name)
    await collection_to_log.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_log", max_retries=3)
def process_log(self: Task, log_data: dict[str, SupportsBytes]) -> None:
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():  # Проверяем, закрыт ли event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(async_process_log(log_data))

    except Exception as e:
        log.error(e)


async def async_process_error_log(log_data):
    mongo_manager = get_mongo_manager()
    collection_to_log = mongo_manager.get_collection("errors")
    await collection_to_log.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_error", max_retries=3)
def process_error(self: Task, log_data: dict[str, SupportsBytes]):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():  # Проверяем, закрыт ли event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(async_process_error_log(log_data))

    except Exception as e:
        log.error(str(e))
