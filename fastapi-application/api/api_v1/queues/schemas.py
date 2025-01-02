from datetime import date
from pydantic import BaseModel

from api.api_v1.queues_entries.schemas import QueueEntry, GetQueueEntryAndUser


class Queue(BaseModel):
    name: str
    start_time: date
    max_slots: int | None = None

class GetQueue(Queue):
    id: int

class GetQueueWithEntries(Queue):
    entries: list[GetQueueEntryAndUser] = []



class CreateQueue(Queue):
    pass


