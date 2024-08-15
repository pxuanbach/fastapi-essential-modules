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
    "/limiting",
    dependencies=[Depends(RateLimiter("5/15s"))]
)
async def test_rate_limiting():
    return { "success": True }
