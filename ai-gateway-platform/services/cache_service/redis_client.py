import redis
import fakeredis

from core.config import settings
from core.logging import logger

if settings.LOCAL_MODE:

    r = fakeredis.FakeRedis(
        decode_responses=True
    )

    logger.info("Using FakeRedis (LOCAL_MODE)")

else:

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