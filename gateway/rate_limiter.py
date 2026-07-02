from services.cache_service.redis_client import r

LIMIT = 5


def check_rate_limit(user_id: str):

    key = f"user:{user_id}"

    count = r.get(key)

    if count is None:
        r.set(key, 1, ex=60)
        return True

    if int(count) >= LIMIT:
        return False

    r.incr(key)

    return True