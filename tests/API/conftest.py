from utils.base_session import BaseSession
import os
import pytest
from dotenv import load_dotenv


@pytest.fixture(scope='session', autouse=True)
def b2b_api():
    load_dotenv()
    b2b_api_url = os.getenv('B2B_API_URL')

    return BaseSession(b2b_api_url)
