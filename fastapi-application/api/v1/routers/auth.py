from fastapi import APIRouter

from core.auth import auth_backend
from domains.users import UserRead, UserCreate
from ..dependencies.users import fastapi_users

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
