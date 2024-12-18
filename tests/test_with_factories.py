import pytest


def test_post_create_recipes(test_app):

    new_recipe = {
            "dish_title": "рис",
            "cooking_time": 25,
            "ingredient_list": "вода, рисовая крупа, соль",
            "description": "отварной рис",
        }
    new_response_1 = test_app.post("/recipes", json=new_recipe)
    # get_response = test_app.get("/recipes")
    assert new_response_1.status_code == 201
    # assert get_response.status_code == 200






