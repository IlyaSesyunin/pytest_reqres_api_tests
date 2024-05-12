import requests
from jsonschema import validate
from schemas.get_user import get_user
from schemas.put_update_user import update_user
from schemas.patch_update_user import patch_update_user
from schemas.login_successful import login_successful

url = "https://reqres.in/api"


def test_get_list_users():
    page_id = 0

    response = requests.get(f'{url}/users?page={page_id}')

    assert response.status_code == 200


def test_get_single_user():
    user_id = 2
    email = "janet.weaver@reqres.in"
    first_name = "Janet"
    last_name = "Weaver"

    response = requests.get(f'{url}/users/{user_id}')

    body = response.json()

    assert response.status_code == 200
    assert body['data']['first_name'] == first_name
    assert body['data']['last_name'] == last_name
    assert body['data']['email'] == email
    validate(body, schema=get_user)


def test_get_single_user_not_found():
    user_id = 23

    response = requests.get(f'{url}/users/{user_id}')

    assert response.status_code == 404
    assert response.json() == {}


def test_create_user():
    name = "morpheus",
    job = "leader"

    response = requests.post(f'{url}/users/', json={"name": name, "job": job})

    assert response.status_code == 201


def test_put_update_user():
    user_id = 2
    name = "morpheus"
    job = "zion resident"

    response = requests.put(f'{url}/users/{user_id}', json={"name": name, "job": job})

    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=update_user)


def test_patch_update_user():
    user_id = 2
    name = "morpheus"
    job = "zion resident"

    response = requests.patch(f'{url}/users/{user_id}', json={"name": name, "job": job})

    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=patch_update_user)


def test_delete_user():
    user_id = 2

    response = requests.delete(f'{url}/users/{user_id}')

    assert response.status_code == 204
    assert response.text == ''


def test_login_successful():
    token = "QpwL5tke4Pnpja7X4"

    payload = {
        "email": "eve.holt@reqres.in",
        "password": "cityslicka"
    }

    response = requests.post(f'{url}/login', data=payload)
    body = response.json()

    assert response.status_code == 200
    assert body['token'] == token
    validate(body, schema=login_successful)


def test_login_unsuccessful():
    payload = {
        "email": "test@mail.ru",
        "password": 111
    }

    response = requests.post(f'{url}/login', data=payload)

    assert response.status_code == 400
