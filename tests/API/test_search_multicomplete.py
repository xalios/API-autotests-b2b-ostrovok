import json
import allure
from jsonschema.validators import validate
from .helpers.auth import get_b2b_auth_headers
from .schemas import load_json_schema


@allure.label('owner', 'Pavel')
@allure.feature('Саджест')
@allure.title('Неавторизованный запрос')
@allure.tag('B2B-API')
def test_unauthorized_request(b2b_api):
    schema = load_json_schema('test_search_multicomplete_unauthorized.json')
    payload = {
        "query": "Berlin",
        "Language": "en",
    }

    request = b2b_api.request(
        method="POST",
        url='/search/multicomplete/',
        data=json.dumps(payload)
    )

    validate(request.json(), schema=schema)
    assert request.status_code == 401


@allure.label('owner', 'Pavel')
@allure.feature('Саджест')
@allure.title('Саджест по региону')
@allure.tag('B2B-API')
def test_search_region(b2b_api):
    payload = {
        "query": "Berlin",
        "Language": "en",
    }
    request = b2b_api.request(
        method="POST",
        headers=get_b2b_auth_headers(),
        url='/search/multicomplete/',
        data=json.dumps(payload)
    )
    response = request.json()
    region = response['data']['regions'][0]

    assert request.status_code == 200
    assert region['name'] == 'Berlin'
    assert region['id'] == 536
    assert region['type'] == 'City'
    assert region['country_code'] == 'DE'


@allure.label('owner', 'Pavel')
@allure.feature('Саджест')
@allure.title('Саджест по отелю')
@allure.tag('B2B-API')
def test_search_hotel(b2b_api):
    payload = {
        "query": "Lazurnyij Bereg Hotel",
        "Language": "en",
    }
    request = b2b_api.request(
        method="POST",
        headers=get_b2b_auth_headers(),
        url='/search/multicomplete/',
        data=json.dumps(payload)
    )
    response = request.json()
    region = response['data']['hotels'][0]

    assert request.status_code == 200
    assert region['name'] == 'Lazurnyij Bereg Hotel'
    assert region['region_id'] == 258
    assert region['id'] == 'lazurniy_bereg_2'
