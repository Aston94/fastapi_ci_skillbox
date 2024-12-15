from pydantic import BaseModel
from typing import Optional


class RecipeAdd(BaseModel):
    dish_title: str
    cooking_time: int
    ingredient_list: str
    description: str


class Recipe(RecipeAdd):
    id: int


class RecipesList(BaseModel):
    id: int
    recipe_id: int
    view_count: int
    cooking_time: int
