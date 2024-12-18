from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, ForeignKeyConstraint, Table

DATABASE_URL = "sqlite+aiosqlite:///recipes.db"

engine = create_async_engine(DATABASE_URL, echo=True)
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class RecipeOrm(Model):
    __tablename__ = "detailed_recipe_information"

    id: Mapped[int] = mapped_column(primary_key=True)
    dish_title: Mapped[str] = mapped_column(unique=True)
    cooking_time: Mapped[int]
    ingredient_list: Mapped[str]
    description: Mapped[str]


class RecipesListOrm(Model):
    __tablename__ = "recipes_list"

    id: Mapped[int] = mapped_column(primary_key=True)
    recipe_id: Mapped[int] = mapped_column(ForeignKey("detailed_recipe_information.id"))
    view_count: Mapped[int]
    cooking_time: Mapped[int] = mapped_column(ForeignKey("detailed_recipe_information.cooking_time"))

    recipe_id_rel = relationship("RecipeOrm", foreign_keys=[recipe_id])
    cooking_rime_rel = relationship("RecipeOrm", foreign_keys=[cooking_time])


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
