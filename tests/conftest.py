from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
import sys

sys.path.append(".")

from database import Model, new_session
from main import app as _app


_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
TestSessionLocal = async_sessionmaker(
    bind=_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(autouse=True, scope="session")
async def initialize_database() -> None:

    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session_override(initialize_database) -> async_sessionmaker[TestSessionLocal]:
    async def override_get_session():
        async with TestSessionLocal() as session:
            yield session

    _app.dependency_overrides[new_session] = override_get_session
    yield
    _app.dependency_overrides.pop(new_session, None)


@pytest_asyncio.fixture(scope="function")
async def client_fixture(session_override) -> TestClient:
    with TestClient(_app) as client:
        yield client
