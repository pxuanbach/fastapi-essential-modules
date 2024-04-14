from typing import Any
from fastapi import APIRouter, BackgroundTasks, Query
import logging


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