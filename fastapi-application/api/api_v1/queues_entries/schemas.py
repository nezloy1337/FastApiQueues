from pydantic import BaseModel


class CreateQueueEntry(BaseModel):
    queue_id: int
    user_id: int
    position: int