from typing import Any, List
from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud import user
from app.deps.db import get_async_session
from app.models.user import User


router = APIRouter(prefix="/users")


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
async def get_pagination_nocache(
    skip: int = Query(0),
    limit: int = Query(20),
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    data = await user.get_pagination(session, skip, limit)
    return data