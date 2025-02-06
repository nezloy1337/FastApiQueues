import asyncio

import bson

from core.celery_app import celery_app, log
from core.mongodb.connection import CONNECTION_REGISTRY, failed_collection
from core.mongodb.schemas import ActionLog


async def async_process_log(log_data):
    collection_name = log_data.pop("collection_name")
    log_entry = ActionLog(**log_data)
    log_entry.parameters["user"]["id"] = bson.Binary.from_uuid(
        log_entry.parameters["user"]["id"]
    )
    collection_to_log = CONNECTION_REGISTRY.get(collection_name)

    if collection_to_log:
        await collection_to_log.insert_one(log_data)
    else:
        await failed_collection(collection_name)


@celery_app.task
def process_log(log_data):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():  # Проверяем, закрыт ли event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(async_process_log(log_data))

    except Exception as e:
        log.error(e)
