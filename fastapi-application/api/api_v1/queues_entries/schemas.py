from pydantic import BaseModel
from uuid import UUID

from core.schemas.user import UserForEntry


class QueueEntry(BaseModel):
    user_uuid: UUID
    position: int


class CreateQueueEntry(QueueEntry):
    queue_id: int


class GetQueueEntryAndUser(BaseModel):
    position: int
    user: UserForEntry



class CreateQueueEntryWithAuth(BaseModel):
    position: int
    queue_id: int
