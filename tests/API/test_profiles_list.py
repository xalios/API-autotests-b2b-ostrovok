import json
import allure
from jsonschema.validators import validate
from .helpers.auth import get_b2b_auth_headers
from .schemas import load_json_schema


@allure.label('owner', 'Pavel')
@allure.feature('Список профайлов')
@allure.title('Неавторизованный запрос')
@allure.tag('B2B-API')
def test_unauthorized_request(b2b_api):
    schema = load_json_schema('test_profiles_list_unauthorized.json')

    request = b2b_api.request(url='/profiles/list/')

    validate(request.json(), schema=schema)
    assert request.status_code == 401


@allure.label('owner', 'Pavel')
@allure.feature('Список профайлов')
@allure.title('Получение списка профайлов')
@allure.tag('B2B-API')
def test_get_profiles(b2b_api):
    schema = load_json_schema('test_profiles_list.json')

    request = b2b_api.request(
        url='/profiles/list/',
        headers=get_b2b_auth_headers()
    )

    assert request.status_code == 200
    validate(request.json(), schema=schema)
