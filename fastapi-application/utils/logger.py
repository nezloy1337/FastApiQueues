from core.schemas.logging import QueueEntryLog
from core.models.mongodb import queue_logs_collection

from utils.exception_handlers import delete_queue_entry_handle_exception


async def log_queue_entry(**queue_entry_data):
    try:
        queue_entry_log = QueueEntryLog(**queue_entry_data)
        await queue_logs_collection.insert_one(queue_entry_log.model_dump(exclude_none=True))
    except Exception as e:
        delete_queue_entry_handle_exception(e)



