import json
import pytest


@pytest.mark.asyncio
async def test_post_create_recipes(client_fixture) -> None:
    """Отправляет валидный POST запрос. Проверяет ожидаемые статус коды и id рецепта"""

    new_recipe_1 = {
        "dish_title": "рис",
        "cooking_time": 25,
        "ingredient_list": "вода, рисовая крупа, соль",
        "description": "отварной рис",
    }

    new_recipe_2 = {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    new_response_1 = client_fixture.post("/recipes", json=new_recipe_1)
    new_response_2 = client_fixture.post("/recipes", json=new_recipe_2)

    assert new_response_1.content.decode() == '1'
    assert new_response_2.content.decode() == '2'
    assert new_response_1.status_code == 200
    assert new_response_2.status_code == 200


@pytest.mark.asyncio
async def test_invalid_recipe_addition(client_fixture) -> None:
    """Проверяем передачей невалидных данных. Ожидаем 422 код ошибки"""

    new_data_1 = {
        "dish_title": 22,
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    new_data_2 = {
        "dish_title": "новое блюдо",
        "cooking_time": 'asd',
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    new_data_3 = {
        "dish_title": "новое блюдо",
        "cooking_time": 15,
        "ingredient_list": 22,
        "description": "классика"
    }

    new_data_4 = {
        "dish_title": "новое блюдо",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль"
    }

    new_response_1 = client_fixture.post("/recipes", json=new_data_1)
    new_response_2 = client_fixture.post("/recipes", json=new_data_2)
    new_response_3 = client_fixture.post("/recipes", json=new_data_3)
    new_response_4 = client_fixture.post("/recipes", json=new_data_4)

    assert new_response_1.status_code == 422
    assert new_response_2.status_code == 422
    assert new_response_3.status_code == 422
    assert new_response_4.status_code == 422


@pytest.mark.asyncio
async def test_adding_an_existing_recipe(client_fixture) -> None:
    """Проверяем отправкой существующего рецепта в базе. Ожидаем получить словарь с ошибкой"""

    new_data = {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    client_fixture.post("/recipes", json=new_data)

    new_data_duplicate = {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    new_response_2 = client_fixture.post("/recipes", json=new_data_duplicate)

    assert {"result": "Такой рецепт уже существует в базе."} == json.loads(
        new_response_2.content.decode()
    )


@pytest.mark.asyncio
async def test_get_all_recipes(client_fixture) -> None:
    """Получаем все рецепты в базе"""

    response = client_fixture.get("/recipes")

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_recipe_by_id(client_fixture) -> None:
    """Проверяем получением рецепта по id"""

    new_data = {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"
    }

    client_fixture.post("/recipes", json=new_data)

    response = client_fixture.get("/recipes/<id:int>?id=1")

    assert json.loads(response.content.decode()) == {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика",
        "id": 1,
    }
