import os
from base64 import b64encode


def _basic_auth(key):
    token = b64encode(f"{key}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def get_b2b_auth_headers():
    return {'Authorization': _basic_auth(os.environ.get('B2B_API_KEY'))}

