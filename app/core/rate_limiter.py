import re
import time
from typing import Any, Final
from fastapi import Request, HTTPException, status

from app.core.redis import redis_client, RedisClient, NoScriptError
from app.core.lua_script import SLIDING_WINDOW_COUNTER


PATTERN: Final[str] = "(\d+)\/((\d+)(s|m|h))+"


class BaseRateLimiterException(Exception):
    pass


class RedisUnavailableException(BaseRateLimiterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Redis is not available."


class RetrieveRuleException(BaseRateLimiterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Can not retrieve Rate-limiter rule."


class LimitRuleException(BaseRateLimiterException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.msg = "Limit value must be greater than 1."


def retrieve_rule(rule: str):
    try:
        limit = re.search(PATTERN, rule).group(1)
        duration = re.search(PATTERN, rule).group(3)
        period = re.search(PATTERN, rule).group(4)
        limit = int(limit)
        duration = int(duration)
    except (re.error, AttributeError, ValueError):
        raise RetrieveRuleException
    
    if limit < 1 or duration < 0:
        raise LimitRuleException

    duration_in_s = duration    # second
    if period == "m":
        duration_in_s = duration * 60
    elif period == "h":
        duration_in_s = duration * 60 * 60
    return limit, duration_in_s


class RateLimiter():
    def __init__(
        self,
        rule: str,
        exception_message: str = "Too many Request!",
        exception_status: int = status.HTTP_429_TOO_MANY_REQUESTS,
        redis: RedisClient = redis_client,
        lua_script: str = SLIDING_WINDOW_COUNTER
    ) -> None:
        (
            self.limit,  # count requests in duration time
            self.duration_in_second
        ) = retrieve_rule(rule)
        self.exp_message = exception_message
        self.exp_status = exception_status
        if redis_client:
            self.redis_client = redis
        self.lua_script = lua_script
        self.lua_sha = ""
    
    @staticmethod
    def req_key_builder(req: Request, **kwargs):
        return ":".join([req.method.lower(), req.client.host, req.url.path])

    async def check(self, key: str, **kwargs):
        return await self.redis_client.evaluate_sha(
            self.lua_sha, 1, [key, self.duration_in_second, self.limit]
        )

    async def __call__(self, request: Request) -> Any:
        if not await self.redis_client.ping():
            raise RedisUnavailableException

        key = self.req_key_builder(request)  
        try:
            is_valid = await self.check(key)
        except NoScriptError:
            self.lua_sha = await self.redis_client.load_script(self.lua_script)
            is_valid = await self.check(key)

        if is_valid == 0:
            return True
        raise HTTPException(status_code=self.exp_status, detail=self.exp_message)
