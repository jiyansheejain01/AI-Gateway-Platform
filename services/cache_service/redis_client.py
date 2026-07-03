"""
Shared Redis client.

Every service should import this client instead of creating
its own Redis connection.
"""

import redis

from core.config import settings
from core.logging import logger


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True,
)


try:
    r.ping()
    logger.info(
        "Connected to Redis",
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
    )

except Exception as e:
    logger.error(
        "Failed to connect to Redis",
        error=str(e),
    )
    raise