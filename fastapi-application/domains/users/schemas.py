import uuid
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


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


class ManageUserPermissions(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None
