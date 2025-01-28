import logging
import uuid
from typing import AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, UUIDIDMixin

from core.auth.get_db import get_user_db
from core.config import settings
from domains.users import User

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
        request: Request | None = None,
    ) -> None:
        log.warning(
            "User %r has registered.",
            user.id,
        )

    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: "Request | None" = None,
    ) -> None:
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
    ) -> None:
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)
