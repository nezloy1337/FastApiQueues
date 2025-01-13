from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from schemas.users import UserForEntry


class QueueEntry(BaseModel):
    user_uuid: UUID
    position: int


class GetQueueEntryAndUser(BaseModel):
    position: int
    user: UserForEntry


class CreateQueueEntry(BaseModel):
    user_id: Optional[UUID] = None
    position: int
    queue_id: int
