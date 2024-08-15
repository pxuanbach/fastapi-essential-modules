import re
import time
from typing import Any, Final
from fastapi import Request, HTTPException

from app.core.redis import redis_client, RedisClient
from app.models.rate_limit import CachedRateLimit


PATTERN: Final[str] = "(\d+)\/((\d+)(s|m|h))+"


class BaseRateLimiterException(Exception):
    pass


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
    except (re.error, AttributeError, ValueError):
        raise RetrieveRuleException
    
    if limit < 1:
        raise LimitRuleException

    duration_in_s = duration
    if period == "m":
        duration_in_s = duration * 60
    elif period == "h":
        duration_in_s = duration * 60 * 60

    return limit, duration_in_s


def req_key_builder(req: Request, **kwargs):
    return ":".join([req.method.lower(), req.client.host, req.url.path])


class RateLimiter():
    def __init__(
        self,
        rule: str,
        exception_message: str = "Too many Request!",
        exception_status: int = 400
    ) -> None:
        (
            self.limit,  # count requests in duration time
            self.duration_in_second
        ) = retrieve_rule(rule)
        self.exp_message = exception_message
        self.exp_status = exception_status

    async def __call__(
        self,
        request: Request
    ) -> Any:
        key = req_key_builder(request)  
        current_time = time.time()
        ttl, in_cache = await redis_client.check_cache(key)

        if in_cache is None:
            # initialize cache
            cached_data = CachedRateLimit(
                last_hit_time=current_time,
                count=1
            )
            await redis_client.add_to_cache(
                key, cached_data.model_dump(), self.duration_in_second)
            return True


        cached_data = CachedRateLimit.model_validate(
            RedisClient.decode_cache(in_cache))
        
        if (
            (current_time - cached_data.last_hit_time) < self.duration_in_second 
            and cached_data.count >= self.limit
        ):
            raise HTTPException(status_code=self.exp_status, detail=self.exp_message)
        else:
            cached_data.last_hit_time = current_time
            if cached_data.count >= self.limit:
                cached_data.count = 1  
            else: 
                cached_data.count += 1

            await redis_client.add_to_cache(
                key, cached_data.model_dump(), self.duration_in_second)
        return True
