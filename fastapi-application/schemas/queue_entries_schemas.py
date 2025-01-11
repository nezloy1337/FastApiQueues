from uuid import UUID
from pydantic import BaseModel

from core.schemas.user import UserForEntry


class QueueEntry(BaseModel):
    user_uuid: UUID
    position: int


class GetQueueEntryAndUser(BaseModel):
    position: int
    user: UserForEntry


class CreateQueueEntry(BaseModel):
    position: int
    queue_id: int
