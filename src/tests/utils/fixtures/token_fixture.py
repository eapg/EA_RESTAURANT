from datetime import datetime, timedelta

import jwt

from src.constants.oauth2 import Roles, Scopes
from src.env_config import get_env_config_instance
from src.tests.utils.fixtures.oauth2_fixture import build_user, build_client
from src.utils.oauth2_util import (
    build_user_credential_access_token,
    build_client_credentials_access_token,
)


def build_user_access_token(roles=None, scopes=None):
    env_config = get_env_config_instance()
    user = build_user(roles=roles)
    client = build_client()
    access_token = build_user_credential_access_token(
        user, client, env_config.oauth2_secret_key, scopes
    )

    return access_token


def build_client_access_token(scopes=None):
    env_config = get_env_config_instance()
    client = build_client()
    access_token = build_client_credentials_access_token(
        client, scopes, env_config.oauth2_secret_key
    )

    return access_token


def build_expire_access_token():
    env_config = get_env_config_instance()
    token = jwt.encode(
        {
            "username": "test",
            "roles": [Roles.ADMINISTRATOR.value],
            "scopes": Scopes.READ.value,
            "exp": datetime.today() - timedelta(days=1),
        },
        env_config.oauth2_secret_key,
        algorithm="HS256",
    )

    return token


def build_invalid_access_token():

    invalid_access_token = (
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz"
        + "Y29wZXMiOlsiV1JJVEUiXSwicm9sZXMiOiJBRE1JTklTVFJBVE9SIiwiZXhwIj"
        + "oxNjcwOTQ1OTMxfQ.q9540ay8wEaVOCt8zP9JVozuDqR_YwTw5R2ZsAeJxB6"
    )
    return invalid_access_token


def build_incomplete_access_token():
    incomplete_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJz"
    return incomplete_access_token
