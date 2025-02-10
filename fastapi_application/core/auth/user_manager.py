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
        """
        Hook executed after a user registers.

        Args:
            user (User): The registered user instance.
            request (Request | None, optional): The HTTP request, if available.
        """
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
        """
        Hook executed after a user requests password reset.

        Args:
            user (User): The user requesting password reset.
            token (str): The reset token.
            request (Request | None, optional): The HTTP request, if available.
        """
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
        """
        Hook executed when a user requests verification.

        Args:
            user (User): The user requesting verification.
            token (str): The verification token.
            request (Request | None, optional): The HTTP request, if available.
        """
        log.warning(
            "Verification requested for user %r. Verification token: %r",
            user.id,
            token,
        )


async def get_user_manager(
    user_db=Depends(get_user_db),
) -> AsyncGenerator[UserManager]:
    """
    Dependency function to get an instance of the UserManager.

    Args:
        user_db (SQLAlchemyUserDatabase): Injected via Depends.

    Yields:
        UserManager: The user manager instance.
    """
    yield UserManager(user_db)
