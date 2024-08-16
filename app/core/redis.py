from typing import Any, Dict, Tuple
import redis.asyncio as aioredis
import logging

from app.utils import ORJsonCoder


class RedisClient:
    async def connect(self, redis_url: str):
        self.pool = aioredis.ConnectionPool().from_url(redis_url)
        self.redis = aioredis.Redis.from_pool(self.pool)
        if await self.redis.ping():
            logging.info("Redis connected")
            return True
        logging.warning("Cannot connect to Redis")
        return False
    
    async def add_to_cache(self, key: str, value: Dict, expire: int) -> bool:
        response_data = None
        try:
            response_data = ORJsonCoder().encode(value)
        except TypeError:
            message = f"Object of type {type(value)} is not JSON-serializable"
            logging.error(message)
            return False
        cached = await self.redis.set(name=key, value=response_data, ex=expire)
        if cached:
            logging.info(f"{key} added to cache")
        else:  # pragma: no cover
            logging.warning(f"Failed to cache key {key}")
        return cached
    
    async def check_cache(self, key: str) -> Tuple[int, str]:
        pipe = self.redis.pipeline()
        ttl, in_cache = await pipe.ttl(key).get(key).execute()
        if in_cache:
            logging.info(f"Key {key} found in cache")
        return (ttl, in_cache)

    async def disconnect(self):
        if await self.redis.ping():
            await self.redis.aclose()
            logging.info("Redis disconnected")
        return None
    
    @staticmethod
    def decode_cache(data: str):
        return ORJsonCoder().decode(data)
    
    async def ping(self):
        if await self.redis.ping():
            return True
        return False


redis_client = RedisClient()