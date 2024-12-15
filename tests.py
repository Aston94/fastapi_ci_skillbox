import json
import httpx

from module_26_fastapi.homework.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_post_create_recipes():
    """Проверяем передачей валидных данных"""
    new_data_1 = json.dumps({"dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"})

    new_data_2 = json.dumps(
        {"dish_title": "рис",
         "cooking_time": 25,
         "ingredient_list": "вода, рисовая крупа, соль",
         "description": "отварной рис"}
    )

    new_response_1 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_1)
    new_response_2 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_2)

    assert new_response_1.status_code == 200
    assert int(new_response_1.content.decode()) == 1
    assert new_response_2.status_code == 200
    assert int(new_response_2.content.decode()) == 2


def test_invalid_recipe_addition():
    """Проверяем передачей невалидных данных"""
    new_data_1 = json.dumps({"dish_title": 22,
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"})

    new_data_2 = json.dumps({"dish_title": "новое блюдо",
        "cooking_time": 'asd',
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"})

    new_data_3 = json.dumps({"dish_title": "новое блюдо",
        "cooking_time": 15,
        "ingredient_list": 22,
        "description": "классика"})

    new_data_4 = json.dumps({"dish_title": "новое блюдо",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",})

    new_response_1 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_1)
    new_response_2 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_2)
    new_response_3 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_3)
    new_response_4 = httpx.post('http://127.0.0.1:8000/recipes', data=new_data_4)


    assert new_response_1.status_code == 422
    assert new_response_2.status_code == 422
    assert new_response_3.status_code == 422
    assert new_response_4.status_code == 422


def test_adding_an_existing_recipe():
    """Проверяем отправкой существующего рецепта в базе"""
    new_data = json.dumps({"dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика"})

    new_response = httpx.post('http://127.0.0.1:8000/recipes', data=new_data)

    assert {"result": "Такой рецепт уже существует в базе."} == json.loads(new_response.content.decode())


def test_get_all_recipes():
    """Получаем все рецепты в базе"""
    response = httpx.get("http://127.0.0.1:8000/recipes")

    assert response.status_code == 200


def test_get_recipe_by_id():
    """Проверяем получением рецепта по id"""
    response = httpx.get("http://127.0.0.1:8000/recipes/<id:int>?id=1")

    assert json.loads(response.content.decode()) == {
        "dish_title": "гречка",
        "cooking_time": 15,
        "ingredient_list": "вода, гречневая крупа, соль",
        "description": "классика",
        "id": 1
    }


if __name__ == '__main__':

    test_post_create_recipes()
    test_get_all_recipes()
    test_adding_an_existing_recipe()
    test_invalid_recipe_addition()
    test_get_recipe_by_id()
