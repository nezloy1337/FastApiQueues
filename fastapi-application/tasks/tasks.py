import asyncio
from typing import Any, SupportsBytes

from bson import ObjectId
from celery import Task
from pydantic import BaseModel

from core.mongodb.connection import get_mongo_manager
from core.mongodb.schemas import ActionLog
from tasks.celery_app import celery_app, log


class ErrorLog(BaseModel):
    error: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


async def async_process_log(log_data: dict[str, Any]) -> None:
    collection_name = log_data.pop("collection_name")
    log_entry = ActionLog(**log_data)
    mongo_manager = get_mongo_manager()
    collection_to_log = mongo_manager.get_collection(collection_name)
    await collection_to_log.insert_one(log_entry.model_dump())


@celery_app.task(bind=True, name="tasks.process_log", max_retries=3)
def process_log(
    self: Task,
    log_data: dict[str, SupportsBytes],
) -> None:
    try:
        asyncio.run(async_process_log(log_data))
    except Exception as e:
        log.error(e)


async def async_process_error_log(log_data):
    mongo_manager = get_mongo_manager()
    collection_to_log = mongo_manager.get_collection("errors")
    await collection_to_log.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_error", max_retries=3)
def process_error(
    self: Task,
    log_data: dict[str, SupportsBytes],
) -> None:
    try:
        asyncio.run(async_process_log(log_data))
    except Exception as e:
        log.error(str(e))
