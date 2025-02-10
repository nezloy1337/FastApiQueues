from uuid import UUID

from fastapi_users import FastAPIUsers

from core.auth import auth_backend, get_user_manager
from domains.users import User

"""
Dependencies for retrieving authenticated users.

These dependencies retrieve the currently authenticated active user 
or superuser based on authentication status.

Returns:
    User: The currently authenticated active user or superuser.

Raises:
    HTTPException (401): If the user is not authenticated.

Usage:
    Use `current_user` in routes where any active user can access::

        @app.get("/profile/")
        def get_profile(user=Depends(current_user)):
            return {"username": user.username, "email": user.email}

    Use `current_super_user` in routes that require superuser access::

        @app.get("/admin/")
        def admin_dashboard(user=Depends(current_super_user)):
            return {"message": "Welcome, admin!"}
"""

fastapi_users = FastAPIUsers[User, UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)
