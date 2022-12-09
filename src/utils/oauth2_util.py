from datetime import datetime, timedelta

import bcrypt
import jwt

from src.constants.http import HttpMethods
from src.constants.oauth2 import Roles, Scopes
from src.exceptions.exceptions import UnAuthorizedEndpoint
from src.lib.entities.secured_http_request_uri import SecuredHttpRequestUrl
from src.lib.entities.secured_http_request_Url_permissions import (
    SecuredHttpRequestUrlPermissions,
)

ENDPOINT_ROLES_MAP = {
    SecuredHttpRequestUrl(
        path="/chefs", method=HttpMethods.GET.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value],
        scopes=[Scopes.READ.value, Scopes.WRITE.value],
    ),
    SecuredHttpRequestUrl(
        path="/chefs/<chef_id>", method=HttpMethods.GET.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value],
        scopes=[Scopes.READ.value, Scopes.WRITE.value],
    ),
    SecuredHttpRequestUrl(
        path="/chefs", method=HttpMethods.POST.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value], scopes=[Scopes.WRITE.value]
    ),
    SecuredHttpRequestUrl(
        path="/chefs/<chef_id>", method=HttpMethods.DELETE.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value], scopes=[Scopes.WRITE.value]
    ),
    SecuredHttpRequestUrl(
        path="/chefs/<chef_id>", method=HttpMethods.PUT.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value], scopes=[Scopes.WRITE.value]
    ),
    SecuredHttpRequestUrl(
        path="/chefs/available", method=HttpMethods.GET.value
    ): SecuredHttpRequestUrlPermissions(
        roles=[Roles.ADMINISTRATOR.value],
        scopes=[Scopes.READ.value, Scopes.WRITE.value],
    ),
}


def get_endpoint_permissions(secured_http_request_url):

    return ENDPOINT_ROLES_MAP[secured_http_request_url]


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
    roles = user.roles
    token = jwt.encode(
        {
            "username": user.username,
            "name": user.name,
            "last_name": user.last_name,
            "roles": roles.split(","),
            "scopes": scopes,
            "exp": datetime.utcnow()
            + timedelta(seconds=client.access_token_expiration_time),
        },
        secret_key,
        algorithm="HS256",
    )

    return token


def build_user_credential_refresh_token(user, client, secret_key, scopes):
    roles = user.roles
    token = jwt.encode(
        {
            "username": user.username,
            "name": user.name,
            "last_name": user.last_name,
            "roles": roles.split(","),
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


def validate_scopes(scopes, secured_http_request_url):

    endpoint_permissions = get_endpoint_permissions(secured_http_request_url)
    if scopes:
        for scope in scopes:
            if scope in endpoint_permissions.scopes:
                return

    raise UnAuthorizedEndpoint("Unauthorized Endpoint Access")


def validate_roles(roles, secured_http_request_url):
    endpoint_permissions = get_endpoint_permissions(secured_http_request_url)
    if roles:
        for role in roles:
            if role in endpoint_permissions.roles:
                return

    raise UnAuthorizedEndpoint("Unauthorized Endpoint Access")


def validate_roles_and_scopes(secret_key, endpoint_request):

    authorization_header = endpoint_request.headers.get("Authorization")
    authorization_header_split = authorization_header.split(" ")
    token = authorization_header_split[1]
    token_decode = jwt.decode(token, secret_key, algorithms="HS256")
    access_token_roles = token_decode.get("roles")
    access_token_scopes = token_decode.get("scopes")
    secured_http_request_url = SecuredHttpRequestUrl(
        path=str(endpoint_request.url_rule), method=endpoint_request.method
    )
    endpoint_permissions = get_endpoint_permissions(secured_http_request_url)
    validate_scopes(access_token_scopes, secured_http_request_url)

    if endpoint_permissions.roles:

        validate_roles(access_token_roles, secured_http_request_url)


def is_endpoint_protected(endpoint_request):
    if (
        SecuredHttpRequestUrl(
            path=str(endpoint_request.url_rule), method=endpoint_request.method
        )
        in ENDPOINT_ROLES_MAP
    ):
        return True
