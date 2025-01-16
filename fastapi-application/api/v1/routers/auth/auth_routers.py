from fastapi import APIRouter

from api.v1.routers.auth.fastapi_users_routers import fastapi_users
from core.auth.backend import auth_backend
from schemas.users import UserRead, UserCreate

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

