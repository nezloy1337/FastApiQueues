from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from .transport import cookie_transport
from .strategy import get_redis_strategy
SECRET = "SECRET"


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)
