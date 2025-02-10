from datetime import datetime
from typing import Any, Dict

from bson import ObjectId
from pydantic import BaseModel


class ActionLog(BaseModel):
    action: str
    timestamp: datetime
    status: str
    parameters: Dict[str, Any]
    error: str | None = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
