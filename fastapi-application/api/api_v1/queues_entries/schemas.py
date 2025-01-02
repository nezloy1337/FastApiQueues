from pydantic import BaseModel
from uuid import UUID

from core.schemas.user import UserForEntry


class QueueEntry(BaseModel):
    user_id: UUID
    position: int


class CreateQueueEntry(QueueEntry):
    queue_id: int
    position: int

class GetQueueEntryAndUser(BaseModel):
    position: int
    user: UserForEntry
