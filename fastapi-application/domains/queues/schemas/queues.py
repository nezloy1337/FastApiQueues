from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from domains.queues.schemas.queue_entries import GetQueueEntryAndUser
from domains.tags.schemas import TagBase


class QueueBase(BaseModel):
    name: str
    start_time: datetime
    max_slots: int | None = None

class GetQueue(QueueBase):
    id: int
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags")


class GetQueueWithEntries(QueueBase):
    entries: list[GetQueueEntryAndUser] = []
    tags: list[TagBase] = Field(default_factory=list, alias="queue_tags") #разобратся как работает alias


class CreateQueue(QueueBase):
    pass


class PutQueue(QueueBase):
    name: Optional[str] = None
    start_time: Optional[datetime] = None
    max_slots: Optional[int] = None


