from fastapi import APIRouter

from app.core.config import settings
from app.api import user, utils, meilisearch, attr


router = APIRouter(prefix=settings.API_STR + settings.API_VERSION_STR)


router.include_router(user.router, tags=["User"])
router.include_router(utils.router, tags=["Utils"])
router.include_router(attr.router, tags=["Attrs"])
router.include_router(meilisearch.router, tags=["Meilisearch"])