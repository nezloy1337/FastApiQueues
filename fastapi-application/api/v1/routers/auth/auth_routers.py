import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from core.auth import auth_backend, get_user_manager
from models import User
from schemas.users import UserRead, UserCreate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
)


# /register
router.include_router(
    fastapi_users.get_register_router(
        UserRead,
        UserCreate,
    )
)
