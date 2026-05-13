import redis.asyncio as redis
from .config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

# Redis client
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

# Rate limiter setup
def get_ipaddr(request: Request):
    # Use X-Forwarded-For if available
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0]
    return get_remote_address(request)

limiter = Limiter(key_func=get_ipaddr, default_limits=[settings.RATE_LIMIT])
