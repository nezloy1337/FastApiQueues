from datetime import date
from pydantic import BaseModel


class CreateQueue(BaseModel):
    name: str
    start_time: date
    max_slots: int | None = None


