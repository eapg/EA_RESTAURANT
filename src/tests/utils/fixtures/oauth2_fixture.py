from src.constants.oauth2 import GranTypes
from src.lib.entities.abstract_entity import AbstractEntity
from src.utils.oauth2_util import encrypt_password

"""
Those classes are created as fixtures because they dont have a service,
they are use to test the oauth2 services. when a service will create the
class will be created as entity in src/lib/entities.
"""


class Client(AbstractEntity):
    def __init__(self):
        self.id = None
        self.client_name = None
        self.client_id = None
        self.client_secret = None
        self.access_token_expiration_time = None
        self.refresh_token_expiration_time = None


class User(AbstractEntity):
    def __init__(self):
        self.id = None
        self.name = None
        self.last_name = None
        self.username = None
        self.password = None
        self.roles = None


class RefreshToken:
    def __init__(self):
        self.id = None
        self.token = None
        self.grant_type = None
        self.app_client_id = None


class AccessToken:
    def __init__(self):
        self.id = None
        self.refresh_token_id = None
        self.token = None


class ClientUser:
    def __init__(self):
        self.id = None
        self.app_client_id = None
        self.username = None


def build_client(
    id=None,
    client_name=None,
    client_id=None,
    client_secret=None,
    access_token_expiration_time=None,
    refresh_token_expiration_time=None,
):
    client = Client()
    client.id = id or 1
    client.client_name = client_name or "client"
    client.client_id = client_id or "client1234"
    client_secret_encrypted = encrypt_password(client_secret or "1234")
    client.client_secret = client_secret_encrypted
    client.access_token_expiration_time = access_token_expiration_time or 60
    client.refresh_token_expiration_time = refresh_token_expiration_time or 120
    return client


def build_user(
    id=None, name=None, last_name=None, username=None, password=None, roles=None
):
    user = User()
    user.id = id or 1
    user.name = name or "juan"
    user.last_name = last_name or "perez"
    user.username = username or "juperez"
    password_encrypted = encrypt_password(password or "1234abcd")
    user.password = password_encrypted
    user.roles = roles or "administrator"
    return user


def build_refresh_token(id=None, token=None, grant_type=None, app_client_id=None):

    refresh_token = RefreshToken()
    refresh_token.id = id or 1
    refresh_token.token = token or "this_is_a_refresh_token"
    refresh_token.grant_type = grant_type or GranTypes.CLIENT_CREDENTIALS.value
    refresh_token.app_client_id = app_client_id or 1

    return refresh_token


def build_access_token(id=None, token=None, refresh_token_id=None):

    access_token = RefreshToken()
    access_token.id = id or 1
    access_token.token = token or "this_is_an_access_token"
    access_token.grant_type = refresh_token_id or 1

    return access_token


def build_client_user(id=None, app_client_id=None, username=None):

    client_user = ClientUser()
    client_user.id = id or 1
    client_user.app_client_id = app_client_id or 1
    client_user.username = username or "juperez"

    return client_user


def build_login_client_json(client_id=None, client_secret=None):

    login_client = {
        "client_id": client_id or "postman001",
        "client_secret": client_secret or "postmansecret01",
        "grant_type": "CLIENT_CREDENTIALS",
    }

    return login_client


def build_login_user_json(
    client_id=None, client_secret=None, username=None, password=None
):

    login_user = {
        "client_id": client_id or "postman001",
        "client_secret": client_secret or "postmansecret01",
        "username": username or "ep_1234",
        "password": password or "1234abcd",
        "grant_type": "PASSWORD",
    }

    return login_user
