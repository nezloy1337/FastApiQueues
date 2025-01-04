from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from .transport import bearer_transport
from .strategy import get_redis_strategy
SECRET = "SECRET"

auth_backend = AuthenticationBackend(
    name="redis",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)
