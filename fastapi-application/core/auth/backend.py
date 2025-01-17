from fastapi_users.authentication import AuthenticationBackend

from .strategy import get_redis_strategy
from .transport import bearer_transport

auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)


