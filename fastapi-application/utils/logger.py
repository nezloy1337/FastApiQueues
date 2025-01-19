from core.mongodb.connection import queue_logs_collection, queue_entries_logs_collection
from core.mongodb.schemas import QueueEntryLog, QueueLog
from utils.exception_handlers import handle_unexpected_error


async def log_queue_entry(**queue_entry_data):
    try:
        queue_entry_log = QueueEntryLog(**queue_entry_data)
        await queue_entries_logs_collection.insert_one(queue_entry_log.model_dump(exclude_none=True))
    except Exception as e:
        handle_unexpected_error(e)

async def log_queue(**queue_data):
    try:
        queue_entry_log = QueueLog(**queue_data)
        await queue_logs_collection.insert_one(queue_entry_log.model_dump(exclude_none=True))
    except Exception as e:
        handle_unexpected_error(e)


