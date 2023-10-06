import json
import allure
from jsonschema.validators import validate
from .helpers.auth import get_b2b_auth_headers
from .helpers.dates import is_order_by_ascending, is_order_by_descending
from .schemas import load_json_schema


@allure.label('owner', 'Pavel')
@allure.feature('Информация об отельном заказе')
@allure.title('Неавторизованный запрос')
@allure.tag('B2B-API')
def test_unauthorized_request(b2b_api):
    schema = load_json_schema('test_hotel_order_info_unauthorized.json')
    payload = {
        "ordering": {
            "ordering_type": "asc",
            "ordering_by": "checkin_at"
        },
        "pagination": {
            "page_size": "1",
            "page_number": "1"
        }
    }

    request = b2b_api.request(
        method="POST",
        url='/hotel/order/info/',
        data=json.dumps(payload)
    )

    validate(request.json(), schema=schema)
    assert request.status_code == 401


@allure.label('owner', 'Pavel')
@allure.feature('Информация об отельном заказе')
@allure.title('Сортировка заказов по дате заезда по возрастанию')
@allure.tag('B2B-API')
def test_order_by_checkin_asc(b2b_api):
    schema = load_json_schema('test_hotel_order_info.json')
    payload = {
        "ordering": {
            "ordering_type": "asc",
            "ordering_by": "checkin_at"
        },
        "pagination": {
            "page_size": "10",
            "page_number": "1"
        }
    }

    request = b2b_api.request(
        method="POST",
        headers=get_b2b_auth_headers(),
        url='/hotel/order/info/',
        data=json.dumps(payload)
    )
    response = request.json()
    orders_checkins = [x['checkin_at'] for x in response['data']['orders']]

    assert request.status_code == 200
    validate(request.json(), schema=schema)
    assert is_order_by_ascending(orders_checkins)


@allure.label('owner', 'Pavel')
@allure.feature('Информация об отельном заказе')
@allure.title('Сортировка заказов по дате выезда по убыванию')
@allure.tag('B2B-API')
def test_search_hotel(b2b_api):
    schema = load_json_schema('test_hotel_order_info.json')
    payload = {
        "ordering": {
            "ordering_type": "desc",
            "ordering_by": "checkout_at"
        },
        "pagination": {
            "page_size": "10",
            "page_number": "1"
        }
    }

    request = b2b_api.request(
        method="POST",
        headers=get_b2b_auth_headers(),
        url='/hotel/order/info/',
        data=json.dumps(payload)
    )
    response = request.json()
    orders_checkouts = [x['checkout_at'] for x in response['data']['orders']]

    assert request.status_code == 200
    validate(request.json(), schema=schema)
    assert is_order_by_descending(orders_checkouts)
