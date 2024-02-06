from datetime import datetime, timedelta

import jwt


class Request:
    def __init__(self, url_rule=None, method=None, headers=None):
        self.url_rule = url_rule
        self.method = method
        self.headers = headers


def create_request(url, method, access_token):

    request = Request(
        url_rule=url,
        method=method,
        headers={"Authorization": "access_token " + access_token},
    )

    return request


def create_refresh_token_request(
    client_credentials=None,
    access_token=None,
    refresh_token=None,
):

    request = {
        "client_credentials": client_credentials or "cG9zdG1hbjAwMTpwb3N0bWFuc2VjcmV0MDE=",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    return request


def build_refresh_token(secret_key=None):

    refresh_token = jwt.encode(
        {
            "client_name": "test_client",
            "scopes": ["READ"],
            "exp": datetime.utcnow() + timedelta(seconds=120),
        },
        secret_key,
        algorithm="HS256",
    )

    return refresh_token


def build_access_token(secret_key=None):

    access_token = jwt.encode(
        {
            "client_name": "test_client",
            "scopes": ["READ"],
            "exp": datetime.utcnow() + timedelta(seconds=120),
        },
        secret_key,
        algorithm="HS256",
    )

    return access_token
