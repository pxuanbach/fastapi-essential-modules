from typing import Any, Tuple
import redis.asyncio as aioredis
import logging


class RedisClient:
    async def connect(self, redis_url: str):
        self.pool = aioredis.ConnectionPool().from_url(redis_url)
        self.redis = aioredis.Redis.from_pool(self.pool)
        if await self.redis.ping():
            logging.info("Redis connected")
            return True
        logging.warning("Cannot connect to Redis")
        return False
        
    def set(self, key: str, response_data: Any, expire=60):
        return self.redis.set(name=key, value=response_data, ex=expire)
    
    def check_cache(self, key: str) -> Tuple[int, str]:
        pipe = self.redis.pipeline()
        ttl, in_cache = pipe.ttl(key).get(key).execute()
        if in_cache:
            logging.info(f"Key {key} found in cache")
        return (ttl, in_cache)

    async def disconnect(self):
        if await self.redis.ping():
            await self.redis.aclose()
            logging.info("Redis disconnected")
        return None


redis_client = RedisClient()