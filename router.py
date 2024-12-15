from fastapi import APIRouter, Depends
from typing import Annotated

from schemas import Recipe, RecipesList, RecipeAdd
from repository import RecipeRepository


router = APIRouter(
    prefix="/recipes",
    tags=['Рецепты']
)


@router.post("")
async def add_recipe(
        recipe: RecipeAdd,
) -> int | dict[str, str]:

    recipe_id = await RecipeRepository.add_one(recipe)
    return recipe_id


@router.get("")
async def get_recipes() -> list[RecipesList]:
    recipes = await RecipeRepository.find_all()
    return recipes


@router.get("/<id:int>")
async def get_recipe(id) -> Recipe | dict[str, str]:
    recipe = await RecipeRepository.find_recipe_by_id(id)
    return recipe
