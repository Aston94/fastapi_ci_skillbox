from sqlalchemy.exc import IntegrityError

from database import RecipeOrm, RecipesListOrm, new_session
from schemas import Recipe, RecipesList, RecipeAdd
import json
from sqlalchemy import select, update, desc


class RecipeRepository:
    @classmethod
    async def add_one(cls, data: RecipeAdd) -> int | dict[str, str]:
        async with new_session() as session:
            recipe_dict = data.model_dump()
            recipe = RecipeOrm(**recipe_dict)
            session.add(recipe)
            try:
                await session.flush()
            except IntegrityError:
                return {"result": "Такой рецепт уже существует в базе."}
            recipe_list = RecipesListOrm(
                recipe_id=recipe.id,
                view_count=0,
                cooking_time=recipe.cooking_time,
            )
            session.add(recipe_list)
            await session.commit()
            return recipe.id

    @classmethod
    async def find_all(cls) -> list[RecipesList] | str:
        async with new_session() as session:
            query = (
                select(RecipesListOrm)
                .order_by(desc(RecipesListOrm.view_count))
                .order_by(desc(RecipesListOrm.cooking_time))
            )

            try:
                result = await session.execute(query)
                recipes_list = result.scalars().all()
                recipes_models = [
                    RecipesList.model_validate(recipe_model, from_attributes=True)
                    for recipe_model in recipes_list
                ]
            except Exception as e:
                return f"error - {e}"
            return recipes_models

    @classmethod
    async def find_recipe_by_id(cls, id) -> Recipe | dict[str, str]:
        async with new_session() as session:
            query_select = select(RecipeOrm).where(RecipeOrm.id == id)
            recipe = await session.execute(query_select)
            result = recipe.scalars().one_or_none()

            if result:
                query_check_id = (
                    update(RecipesListOrm)
                    .where(RecipesListOrm.recipe_id == id)
                    .values(view_count=RecipesListOrm.view_count + 1)
                )
                await session.execute(query_check_id)
                await session.commit()
                validate_result = Recipe.model_validate(result, from_attributes=True)
                return validate_result
            else:
                return {"response": "Рецепта с таким id не существует."}
