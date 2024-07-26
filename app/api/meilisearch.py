import json
from typing import Any, List
from fastapi import APIRouter, Depends, Query, BackgroundTasks, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from meilisearch.models.index import IndexStats

from .user import get_pagination_view
from app.crud import user, attr, user_attr
from app.core import cache, meilisearch
from app.deps.db import get_async_session
from app.models.user import User, UserView


router = APIRouter(prefix="/meilisearch")


@router.get(
    "",
)
async def search(
    q: str,
    # session: AsyncSession = Depends(get_async_session)
) -> Any:
    index = meilisearch.client.index('users')
    search = index.search(q, {
        'facets': ['attrs', 'full_name', 'email']
    })
    print(search)
    return search


@router.post(
    "/index"
)
async def index(
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    # An index is where the documents are stored.
    index = meilisearch.client.index('users')

    data: List[UserView] = await user.get_pagination_view(session, 0, 999999)
    documents = []
    for row in data:
        documents.append(UserView.model_validate(row).dict())

    # If the index 'movies' does not exist, Meilisearch creates it when you first add the documents.
    index.add_documents(documents) # => { "uid": 0 }

    index.update_filterable_attributes([
        'email',
        'full_name',
        'attrs',
    ])
    return { "success": True }


@router.post(
    "/bulk/{num}",
    name="meilisearch:prepare_data",
    response_model=dict
)
async def prepare_data(
    num: int,
    session: AsyncSession = Depends(get_async_session)
) -> Any:
    # init user_attrs
    await user_attr.bulk_insert(session, num)

    return { "success": True }

