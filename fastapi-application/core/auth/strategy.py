import redis.asyncio
from fastapi_users.authentication import RedisStrategy

from core.config import settings

redis = redis.asyncio.from_url(settings.redis.url, decode_responses=settings.redis.decode_responses,)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, settings.redis.lifetime_seconds)
