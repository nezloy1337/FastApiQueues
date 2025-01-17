from uuid import UUID

from fastapi_users import FastAPIUsers

from core.auth import auth_backend, get_user_manager
from models import User

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)



