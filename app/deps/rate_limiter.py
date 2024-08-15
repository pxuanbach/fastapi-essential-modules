import re
import time
from typing import Any, Final
from fastapi import Request

from app.core.redis import redis_client


PATTERN: Final[str] = "(\d+)\/(\d+(s|m|h))+"


class RateLimiterException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Something wrong with Rate-limiter"


class RetrieveRuleException(RateLimiterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Can not retrieve Rate-limiter rule."


def retrieve_rule(rule: str):
    try:
        limit = re.search(PATTERN, rule).group(1)
        duration = re.search(PATTERN, rule).group(2)
        return limit, duration
    except (re.error, AttributeError):
        raise RetrieveRuleException


def req_key_builder(req: Request, **kwargs):
    return ":".join([req.method.lower(), req.client.host, req.url.path])


class RateLimiter():
    def __init__(
        self,
        rule: str,
        exception_message: str = "Too many Request!",
        exception_status: int = 400
    ) -> None:
        self.limit, self.duration = retrieve_rule(rule)
        self.exp_message = exception_message
        self.exp_status = exception_status

    async def __call__(
        self,
        request: Request
    ) -> Any:
        key = req_key_builder(request)  
        current_time = time.time()
        ttl, in_cache = await redis_client.check_cache(key)

        

        return True
