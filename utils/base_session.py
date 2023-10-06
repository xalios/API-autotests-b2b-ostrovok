import allure
import json
import logging
from json import JSONDecodeError


from allure_commons.types import AttachmentType
from requests import Session
from curlify import to_curl


class BaseSession(Session):
    def __init__(self, url):
        super(BaseSession, self).__init__()
        self.url = url

    def request(self, url, method="GET", **kwargs):
        with allure.step(f"{method} {url}"):
            response = super().request(method, self.url + url, **kwargs)
            logging.info(f'{response.status_code} {to_curl(response.request)}')

            allure.attach(body=to_curl(response.request).encode("utf8"),
                          name=f"Request {response.status_code}",
                          attachment_type=AttachmentType.TEXT,
                          extension=".txt")
            try:
                allure.attach(body=json.dumps(response.json(), indent=4).encode("utf8"),
                              name=f"Response {response.status_code}",
                              attachment_type=AttachmentType.JSON,
                              extension=".json")
            except JSONDecodeError:
                allure.attach(body=response.text.encode("utf8"),
                              name=f"Response {response.status_code}",
                              attachment_type=AttachmentType.TEXT,
                              extension=".txt")
        return response


