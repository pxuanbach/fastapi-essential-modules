from typing import Any, List
from fastapi import APIRouter, Depends, Query, BackgroundTasks, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import attr
from app.deps.db import get_async_session
from app.models.attr import Attr


router = APIRouter(prefix="/attrs")


@router.get(
    "",
    response_model=List[Attr]
)
async def get_pagination(
    skip: int = Query(0),
    limit: int = Query(20),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    data = await attr.get_pagination(session, skip, limit)
    return data


@router.post(
    "/bulk/{num}",
    name="attr:bulk_insert"
)
async def bulk_insert(
    num: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    await attr.bulk_insert(session, num)
    return { "success": True }


