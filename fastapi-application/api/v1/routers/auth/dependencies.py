from .auth_routers import fastapi_users

current_user = fastapi_users.current_user(active=True)
current_super_user = fastapi_users.current_user(active=True, superuser=True)