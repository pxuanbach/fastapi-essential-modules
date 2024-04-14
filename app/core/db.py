from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from app.core.config import settings


async_engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI_ASYNC))
async_session_maker = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# We still have a second old style sync SQLAlchemy engine for shell and alembic
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), future=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
SQLModel.metadata = Base.metadata
