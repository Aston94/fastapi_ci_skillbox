import pytest
import sys
import json
from sqlalchemy.testing.assertsql import assert_engine

sys.path.append('../')
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import ForeignKey, Integer, String, ForeignKeyConstraint, Table
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from database import Model, RecipesListOrm, RecipeOrm, create_tables, drop_tables
from main import app


DATABASE_URL = "sqlite+aiosqlite:///test.db"


@pytest.fixture(scope="module")
def test_app():
    _engine = create_engine(DATABASE_URL, echo=True)
    _new_session = sessionmaker(_engine, expire_on_commit=False)
    client = TestClient(app)
    create_tables(_engine)

    yield client






