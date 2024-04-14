import json
import logging
from typing import Any, Dict
from fastapi import Request

from app.core.redis import redis_client
from app.utils import ORJsonCoder


def req_key_builder(req: Request, **kwargs):
    return ":".join([req.method.lower(), req.url.path, req.query_params])


def cache(req: Request, data: Any, expire: int = 60):
    redis_client.set(req_key_builder(req), json.encoder(data), ex=expire)
    return True

def add_to_cache(key: str, value: Dict, expire: int) -> bool:
    response_data = None
    try:
        response_data = ORJsonCoder().encode(value)
    except TypeError:
        message = f"Object of type {type(value)} is not JSON-serializable"
        logging.error(message)
        return False
    cached = redis_client.set(name=key, value=response_data, ex=expire)
    if cached:
        logging.info(f"{key} added to cache")
    else:  # pragma: no cover
        logging.warning(f"Failed to cache key {key}")
    return cached
