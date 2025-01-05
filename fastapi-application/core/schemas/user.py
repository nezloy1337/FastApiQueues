import uuid

from pydantic import BaseModel
from fastapi_users import schemas


class FirstAndLastNamesMixin(BaseModel):
    first_name: str
    last_name: str


class UserRead(FirstAndLastNamesMixin, schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(FirstAndLastNamesMixin, schemas.BaseUserCreate):
    pass


class UserUpdate(FirstAndLastNamesMixin, schemas.BaseUserUpdate):
    pass


class UserForEntry(FirstAndLastNamesMixin, BaseModel):
    pass
