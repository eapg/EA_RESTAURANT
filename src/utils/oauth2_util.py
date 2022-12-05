from datetime import datetime, timedelta

from src.constants.oauth2 import Roles, Scopes
from src.constants.http import HttpMethods
from src.lib.entities.secured_http_request_uri import SecuredHttpRequestUrl

import bcrypt
import jwt

from src.exceptions.exceptions import UnAuthorizedEndpoint

ENDPOINT_ROLES_MAP = {
    SecuredHttpRequestUrl(path="/chefs", method=HttpMethods.GET.value): [
        Roles.ADMINISTRATOR.value,
        Scopes.WRITE.value,
    ],
    SecuredHttpRequestUrl(path="/chefs/<chef_id>", method=HttpMethods.GET.value): [
        Roles.ADMINISTRATOR.value
    ],
    SecuredHttpRequestUrl(path="/chefs, POST", method=HttpMethods.POST.value): [
        Roles.ADMINISTRATOR.value
    ],
    SecuredHttpRequestUrl(path="/chefs/<chef_id>", method=HttpMethods.DELETE.value): [
        Roles.ADMINISTRATOR.value
    ],
    SecuredHttpRequestUrl(path="/chefs/<chef_id>", method=HttpMethods.PUT.value): [
        Roles.ADMINISTRATOR.value
    ],
    SecuredHttpRequestUrl(path="/chefs/available", method=HttpMethods.GET.value): [
        Roles.ADMINISTRATOR.value
    ],
}


def build_client_credentials_access_token(client, scopes, secret_key):

    token = jwt.encode(
        {
            "scopes": scopes,
            "exp": datetime.utcnow()
            + timedelta(seconds=client.access_token_expiration_time),
        },
        secret_key,
        algorithm="HS256",
    )

    return token


def build_client_credentials_refresh_token(client, scopes, secret_key):
    token = jwt.encode(
        {
            "scopes": scopes,
            "exp": datetime.utcnow()
            + timedelta(seconds=client.refresh_token_expiration_time),
        },
        secret_key,
        algorithm="HS256",
    )

    return token


def build_user_credential_access_token(user, client, secret_key, scopes):
    token = jwt.encode(
        {
            "username": user.username,
            "name": user.name,
            "last_name": user.last_name,
            "roles": user.roles,
            "scopes": scopes,
            "exp": datetime.utcnow()
            + timedelta(seconds=client.access_token_expiration_time),
        },
        secret_key,
        algorithm="HS256",
    )

    return token


def build_user_credential_refresh_token(user, client, secret_key, scopes):

    token = jwt.encode(
        {
            "username": user.username,
            "name": user.name,
            "last_name": user.last_name,
            "roles": user.roles,
            "scopes": scopes,
            "exp": datetime.utcnow()
            + timedelta(seconds=client.refresh_token_expiration_time),
        },
        secret_key,
        algorithm="HS256",
    )

    return token


def encrypt_password(password):

    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password_bytes, salt)
    decode_hash_password = hash_password.decode("utf-8")
    return decode_hash_password


def validate_roles_and_scopes(secret_key, endpoint_request):

    token = endpoint_request.args.get("access_token")
    token_decode = jwt.decode(token, secret_key, algorithms="HS256")
    roles = token_decode.get("roles")
    scopes = token_decode.get("scopes")
    secured_http_request_url = SecuredHttpRequestUrl(
        path=endpoint_request.path, method=endpoint_request.method
    )
    unauthorized_exception = UnAuthorizedEndpoint("Unauthorized Endpoint Access")
    if roles and roles not in ENDPOINT_ROLES_MAP[secured_http_request_url]:
        raise unauthorized_exception

    if not roles and all(
            scope not in ENDPOINT_ROLES_MAP[secured_http_request_url] for scope in scopes
    ):
        raise unauthorized_exception


def is_endpoint_protected(endpoint_request):

    if (
        SecuredHttpRequestUrl(
            path=endpoint_request.path, method=endpoint_request.method
        )
        in ENDPOINT_ROLES_MAP
    ):
        return True

