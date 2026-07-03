"""
Redis-backed rate limiter.
"""

from core.config import settings
from core.logging import logger

from services.cache_service.redis_client import r


def check_rate_limit(user_id: str) -> bool:
    """
    Enforce a per-user rate limit using Redis.
    """

    key = f"user:{user_id}"

    count = r.get(key)

    if count is None:

        r.set(
            key,
            1,
            ex=settings.RATE_LIMIT_WINDOW,
        )

        logger.info(
            "Rate limit counter created",
            user=user_id,
        )

        return True

    if int(count) >= settings.RATE_LIMIT:

        logger.warning(
            "Rate limit exceeded",
            user=user_id,
        )

        return False

    r.incr(key)

    return True