from datetime import date
from pydantic import BaseModel


class Queue(BaseModel):
    name: str
    start_time: date
    max_slots: int | None = None

class CreateQueue(Queue):
    pass


