import asyncio
import logging
from typing import Any, SupportsBytes

from bson import ObjectId
from celery import Task
from pydantic import BaseModel

from core.mongodb.connection import get_mongo_manager
from core.mongodb.schemas import ActionLog
from tasks.celery_app import celery_app


class ErrorLog(BaseModel):
    error: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


log = logging.getLogger(__name__)


async def async_process_log(log_data: dict[str, Any]) -> None:
    """
    Process and save a log entry in MongoDB.

    Expects 'collection_name' in log_data to select the target collection.
    """
    try:
        collection_name = log_data.pop("collection_name")
    except KeyError:
        log.error("Missing 'collection_name' in log_data: %s", log_data)
        raise

    log_entry = ActionLog(**log_data)
    mongo_manager = get_mongo_manager()
    collection = mongo_manager.get_collection(collection_name)
    await collection.insert_one(log_entry.model_dump())


@celery_app.task(bind=True, name="tasks.process_log", max_retries=3)
def process_log(self: Task, log_data: dict[str, SupportsBytes]) -> None:
    """
    Celery task to process a log entry.
    """
    log.info("start consuming log")
    try:
        asyncio.run(async_process_log(log_data))
    except Exception as exc:
        log.exception("Error processing log_data: %s", log_data)
        raise self.retry(exc=exc, countdown=10)


async def async_process_error_log(log_data: dict[str, Any]) -> None:
    """
    Process and save an error log in MongoDB.
    """
    mongo_manager = get_mongo_manager()
    collection = mongo_manager.get_collection("errors")
    await collection.insert_one(log_data)


@celery_app.task(bind=True, name="tasks.process_error", max_retries=3)
def process_error(self: Task, log_data: dict[str, SupportsBytes]) -> None:
    """
    Celery task to process an error log.
    """
    try:
        asyncio.run(async_process_error_log(log_data))
    except Exception as exc:
        log.exception("Error processing error log_data: %s", log_data)
        raise self.retry(exc=exc, countdown=10)
