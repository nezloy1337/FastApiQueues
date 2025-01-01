import uuid

from alembic.command import current
from fastapi_users import FastAPIUsers

from core.models import User
from core.auth.backend import auth_backend
from core.auth.user_manager import get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True,superuser=True)