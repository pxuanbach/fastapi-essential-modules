from typing import Any
from urllib.parse import urlencode
from fastapi import Request
from fastapi.datastructures import QueryParams

from app.core.redis import redis_client
from app.utils import ORJsonCoder


def query_params_builder(params: QueryParams) -> str:
    sorted_query_params = sorted(params.items())
    return urlencode(sorted_query_params, doseq=True)


def req_key_builder(req: Request, **kwargs):
    return ":".join([req.method.lower(), req.url.path, query_params_builder(req.query_params)])


async def add(req: Request, data: Any, expire: int = 60):   
    cached = await redis_client.add_to_cache(req_key_builder(req), data, expire)
    if not cached:
        return False
    return True


async def check_exist(req: Request) -> str:
    key = req_key_builder(req)
    ttl, in_cache = await redis_client.check_cache(key)
    return in_cache


def load_cache_data(data: str):
    return ORJsonCoder().decode(data)
