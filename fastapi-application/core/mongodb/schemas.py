from typing import Optional, Dict
from datetime import datetime, date
from bson import ObjectId

from pydantic import BaseModel, Field


class ObjectIdTimeActionMixin(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    action: str
    timestamp: datetime

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class QueueLog(ObjectIdTimeActionMixin,BaseModel):
    name: str
    start_time: datetime
    max_slots: int


class QueueEntryLog(ObjectIdTimeActionMixin,BaseModel):
    user_uuid: str
    queue_id: int
    position: int
    details: Optional[Dict] = None


class ExceptionLogTemplate(BaseModel):
    description: Optional[str] = None
    timestamp: Optional[datetime] = None

