from typing import Optional, Dict
from datetime import datetime
from bson import ObjectId

from pydantic import BaseModel, Field

class QueueEntryLog(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_uuid: str
    queue_id: int
    action: str
    time: datetime
    position: int
    details: Optional[Dict] = None

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
