import logging
import uuid
from typing import Optional, TYPE_CHECKING

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin

from api.dependencies.users import get_user_db
from core.models.user import User
from core.config import settings

if TYPE_CHECKING:
    from fastapi import Request


log = logging.getLogger(__name__)


class UserManager(
    UUIDIDMixin,
    BaseUserManager[User, uuid.UUID],
):
    reset_password_token_secret = settings.user_manager.reset_password_token_secret
    verification_token_secret = settings.user_manager.verification_token_secret

    async def on_after_register(
        self,
        user: User,
        request: "Request | None" = None,
    ):
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: "Request | None" = None,
    ):
        log.warning(
            "User %r has forgot their password. Reset token: %r",
            user.id,
            token,
        )

    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: "Request | None" = None,
    ):
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
