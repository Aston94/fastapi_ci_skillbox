import pytest
import sys

sys.path.append('../')
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from fastapi.testclient import TestClient
from database import Model, RecipesListOrm, RecipeOrm, create_tables, drop_tables, new_session
from main import app
# from sqlmodel import Session, SQLModel, create_engine
import pytest_asyncio


@pytest_asyncio.fixture(name='session')
async def session_fixture():
    _engine = create_async_engine("sqlite+aiosqlite:///test.db")
    _new_session = async_sessionmaker(_engine, expire_on_commit=False)
    async with _new_session() as session:
        yield session

@pytest_asyncio.fixture(name='client')
async def client_fixture(session):
    async def get_session_override():
        yield session
    app.dependency_overrides[new_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
