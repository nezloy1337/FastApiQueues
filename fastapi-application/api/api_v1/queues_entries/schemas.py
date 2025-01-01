from uuid import UUID

from pydantic import BaseModel

class QueueEntry(BaseModel):
    user_id: int
    position: int


class CreateQueueEntry(QueueEntry):
    queue_id: int
    user_uuid: UUID
    position: int