from fastapi import FastAPI
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.logger import setup as setup_logging
from app.core.config import settings
from app.api import router


def custom_generate_unique_id(route: APIRoute) -> str:
    if len(route.tags) > 0:
        f"{route.tags[0]}-{route.name}"
    return f"{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # start up
    setup_logging()
    yield
    # shut down
    pass


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}{settings.API_VERSION_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan
)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


app.include_router(router)