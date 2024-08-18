from typing import Any
from fastapi import APIRouter, BackgroundTasks, Depends, Query
import logging

from app.core.rate_limiter import RateLimiter


router = APIRouter(prefix="/utils")


@router.post(
    "/logs",
)
async def create_log(
    bg_tasks: BackgroundTasks,
    text: str = Query('')
) -> Any:
    bg_tasks.add_task(
        logging.info,
        text
    )
    bg_tasks.add_task(
        logging.warning,
        text
    )
    bg_tasks.add_task(
        logging.error,
        text
    )
    bg_tasks.add_task(
        logging.critical,
        text
    )
    return { "success": True }


@router.get(
    "/limiting1",
    dependencies=[Depends(RateLimiter("5/15s"))]
)
async def test_rate_limiting1():
    return { "success": True }


@router.get(
    "/limiting2",
    dependencies=[Depends(RateLimiter("1/1m"))]
)
async def test_rate_limiting2():
    return { "success": True }
