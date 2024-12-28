from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from .transport import cookie_transport
from .strategy import get_redis_strategy
SECRET = "SECRET"

auth_backend = AuthenticationBackend(
    name="redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)
