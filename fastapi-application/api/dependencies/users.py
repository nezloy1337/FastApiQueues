from uuid import UUID

from core.auth import auth_backend, get_user_manager
from domains.users import User
from fastapi_users import FastAPIUsers

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)
"""
Dependencies for retrieving authenticated users.
Retrieves the currently authenticated active user or superuser.

:returns: The currently authenticated active user or superuser.
:raises:
    - HTTPException (401): If the user is not authenticated.

:usage:
    Use this dependency in routes where any active user can access::

        @app.get("/profile/")
        def get_profile(user=Depends(current_user)):
            return {"username": user.username, "email": user.email}

"""
