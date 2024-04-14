from fastapi import APIRouter

from app.core.config import settings
from app.api import user
from app.api import utils


router = APIRouter(prefix=settings.API_STR + settings.API_VERSION_STR)


router.include_router(user.router, tags=["User"])
router.include_router(utils.router, tags=["Utils"])