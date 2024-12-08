from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel import create_engine

from app.main import app
from app.core.config import settings
from app.deps.db import get_async_session, get_db
from app.models import SQLModel


test_async_db = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI_ASYNC), echo=True)
TestAsyncSessionLocal = sessionmaker(
    test_async_db, 
    class_=AsyncSession, 
    expire_on_commit=False, 
    autocommit=False,
    autoflush=False,
)
test_db = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
TestSessionLocal = sessionmaker(
    test_db, 
    class_=Session, 
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    # Initalize database
    async with test_async_db.begin() as conn:
        print("Initalize database", SQLModel.metadata)
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    # clean database test
    async with test_async_db.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_db():
    async with TestAsyncSessionLocal() as session:
        yield session


@pytest.fixture(scope="function")
def db():
    db = None
    try:
        db = TestSessionLocal()
        SQLModel.metadata.drop_all(bind=test_db)
        SQLModel.metadata.create_all(bind=test_db)
        yield db
    finally:
        if db:
            db.close()



# Override dependencies
@pytest.fixture(scope="function")
def client(async_db, db):
    def override_get_sync_db():
        yield db

    def override_get_async_db():
        yield async_db

    app.dependency_overrides[get_db] = override_get_sync_db
    app.dependency_overrides[get_async_session] = override_get_async_db

    with TestClient(app) as c:
        yield c
