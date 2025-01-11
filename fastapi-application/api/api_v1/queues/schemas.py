from datetime import date
from typing import List

from pydantic import BaseModel, Field

from api.api_v1.queues_entries.schemas import GetQueueEntryAndUser
from api.api_v1.tags.schemas import TagBase


class Queue(BaseModel):
    name: str
    start_time: date
    max_slots: int | None = None

class GetQueue(Queue):
    id: int
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags")


class GetQueueWithEntries(Queue):
    entries: list[GetQueueEntryAndUser] = []
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags") #разобратся как работает alias

class CreateQueue(Queue):
    pass


