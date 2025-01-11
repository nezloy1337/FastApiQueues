from datetime import date
from typing import List

from pydantic import BaseModel, Field

from api.api_v1.queues_entries.schemas import GetQueueEntryAndUser
from api.api_v1.tags.schemas import TagBase


class QueueBase(BaseModel):
    name: str
    start_time: date
    max_slots: int | None = None

class GetQueue(QueueBase):
    id: int
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags")


class GetQueueWithEntries(QueueBase):
    entries: list[GetQueueEntryAndUser] = []
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags") #разобратся как работает alias

class CreateQueue(QueueBase):
    pass


