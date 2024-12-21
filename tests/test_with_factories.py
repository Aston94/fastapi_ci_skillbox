import pytest
from main import app
from fastapi.testclient import TestClient
import asyncio

@pytest.mark.asyncio
async def test_post_create_recipes(client_fixture):
    new_recipe = {
            "dish_title": "рис",
            "cooking_time": 25,
            "ingredient_list": "вода, рисовая крупа, соль",
            "description": "отварной рис",
        }
    new_response_1 = client_fixture.post("/recipes", json=new_recipe)
    # get_response = test_app.get("/recipes")
    assert new_response_1.status_code in (200, 201)
    # assert get_response.status_code == 200






