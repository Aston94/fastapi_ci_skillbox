import pytest
import sys

sys.path.append('../')
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from fastapi.testclient import TestClient
from database import Model, RecipesListOrm, RecipeOrm, new_session, engine
from main import app
# from sqlmodel import Session, SQLModel, create_engine
import pytest_asyncio

_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
TestSessionLocal = async_sessionmaker(bind=_engine, class_=AsyncSession, echo=True)


@pytest_asyncio.fixture(scope="session")
async def initialize_database():
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
    yield
    async with _engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


app.dependency_overrides[engine] = _engine
app.dependency_overrides[new_session] = TestSessionLocal


@pytest_asyncio.fixture
async def client_fixture():
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

