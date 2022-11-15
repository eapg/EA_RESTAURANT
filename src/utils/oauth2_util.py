from datetime import datetime, timedelta

import jwt


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
            "username": user.user_name,
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
            "username": user.user_name,
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
