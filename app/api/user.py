from typing import Any, List
from fastapi import APIRouter, Depends, Query, BackgroundTasks, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi_cache.decorator import cache

from app.crud import user
from app.core import cache
from app.deps.db import get_async_session
from app.models.user import User


router = APIRouter(prefix="/users")


@router.get("", response_model=List[User])
async def get_pagination_cache(
    request: Request,
    bg_tasks: BackgroundTasks,
    skip: int = Query(0),
    limit: int = Query(20),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    """
    Implement logic for caching 
    """
    in_cache = await cache.check_exist(req=request)
    if in_cache:
        return cache.load_cache_data(in_cache)
    data = await user.get_pagination(session, skip, limit)
    bg_tasks.add_task(
        cache.add,
        req=request,
        data=data,
        expire=60
    )
    return data


@router.post(
    "/bulk/{num}"
)
async def bulk_insert(
    num: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    await user.bulk_insert(session, num)
    return { "success": True }


@router.get(
    "/nocache",
    response_model=List[User]
)
async def get_pagination_cache(
    skip: int = Query(0),
    limit: int = Query(20),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    data = await user.get_pagination(session, skip, limit)
    return data