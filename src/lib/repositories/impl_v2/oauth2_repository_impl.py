from injector import inject
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
import jwt
from src.exceptions.exceptions import WrongCredentialsException, InvalidCredentialsException
from src.env_config import get_env_config_instance
from src.password_encoder.password_encoder import PasswordEncoder
from src.utils.oauth2_util import (
    build_client_credentials_access_token,
    build_client_credentials_refresh_token,
    build_user_credential_access_token,
    build_user_credential_refresh_token,
    build_authentication_response,
)
from src.constants.oauth2 import GranTypes
from src.utils.sql_oath2_queries import (
    SQL_QUERY_TO_GET_USER_BY_USERNAME,
    SQL_QUERY_TO_GET_CLIENT_BY_CLIENT_ID,
    SQL_QUERY_TO_GET_CLIENT_BY_ID,
    SQL_QUERY_TO_ADD_ACCESS_TOKEN,
    SQL_QUERY_TO_ADD_REFRESH_TOKEN,
    SQL_QUERY_TO_GET_SCOPES_BY_CLIENT_ID,
    SQL_QUERY_TO_DELETE_ACCESS_TOKEN_BY_REFRESH_TOKEN_ID,
    SQL_QUERY_TO_DELETE_REFRESH_TOKEN,
    SQL_QUERY_TO_GET_CLIENT_USER_BY_USERNAME_AND_CLIENT_ID,
    SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_ACCESS_REFRESH_TOKEN_AND_CLIENT,
    SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_TOKEN,
)


class Oauth2RepositoryImpl:
    @inject
    def __init__(self, engine: Engine, password_encoder: PasswordEncoder):
        self.engine = engine
        self.password_encoder = password_encoder
        self.env_config = get_env_config_instance()

    def login_client(self, client_id, client_secret):
        return self._login(
            client_id=client_id,
            client_secret=client_secret,
            grant_type=GranTypes.CLIENT_CREDENTIALS,
        )

    def login_user(self, client_id, client_secret, username, password):
        return self._login(
            username=username,
            password=password,
            client_id=client_id,
            client_secret=client_secret,
            grant_type=GranTypes.PASSWORD,
        )

    def _login(
        self,
        client_id=None,
        client_secret=None,
        username=None,
        password=None,
        grant_type=None,
    ):
        self._validate_client_credentials(client_id, client_secret)

        client = self._get_client_by_client_id(client_id)

        client_scopes = self._get_scope_by_app_client_id(client.id)

        if grant_type == GranTypes.CLIENT_CREDENTIALS:

            access_token = build_client_credentials_access_token(
                client, client_scopes, self.env_config.oauth2_secret_key
            )
            refresh_token = build_client_credentials_refresh_token(
                client, client_scopes, self.env_config.oauth2_secret_key
            )

            authentication_response = build_authentication_response(
                self.env_config.oauth2_secret_key, access_token, refresh_token
            )

        elif grant_type == GranTypes.PASSWORD:
            self._validate_user_credentials(client, username, password)

            user = self._get_user_by_username(username)

            access_token = build_user_credential_access_token(
                user, client, self.env_config.oauth2_secret_key, client_scopes
            )
            refresh_token = build_user_credential_refresh_token(
                user, client, self.env_config.oauth2_secret_key, client_scopes
            )

            authentication_response = build_authentication_response(
                self.env_config.oauth2_secret_key, access_token, refresh_token
            )

        persisted_refresh_token = self._add_refresh_token(
            refresh_token, client.id, grant_type.value
        )
        self._add_access_token(persisted_refresh_token.id, access_token)

        return authentication_response

    def validate_token(self, token):
        # That is the way how jwt library validates the token
        jwt.decode(token, self.env_config.oauth2_secret_key, algorithms="HS256")

    def refresh_token(self, refresh_token, access_token, client_id, client_secret):

        self._validate_client_credentials(client_id, client_secret)

        try:
            self.validate_token(access_token)
            return build_authentication_response(
                self.env_config.oauth2_secret_key, access_token, refresh_token
            )

        except jwt.exceptions.ExpiredSignatureError:

            refresh_token_decoded = jwt.decode(
                refresh_token, self.env_config.oauth2_secret_key, algorithms="HS256"
            )

            app_refresh_token = (
                self._get_refresh_token_by_access_refresh_token_and_client_id(
                    access_token,
                    refresh_token,
                    client_id,
                    refresh_token_decoded.get("user", {}).get("username"),
                )
            )
            client = self._get_client_by_id(app_refresh_token.app_client_id)
            client_scopes = self._get_scope_by_app_client_id(
                app_refresh_token.app_client_id
            )

            if app_refresh_token.grant_type == GranTypes.CLIENT_CREDENTIALS.value:

                new_access_token = build_client_credentials_access_token(
                    client, client_scopes, self.env_config.oauth2_secret_key
                )

                authentication_response = build_authentication_response(
                    self.env_config.oauth2_secret_key, new_access_token, refresh_token
                )

            else:
                refresh_token_decoded = jwt.decode(
                    refresh_token, self.env_config.oauth2_secret_key, algorithms="HS256"
                )

                user = self._get_user_by_username(
                    refresh_token_decoded.get("user").get("username")
                )
                new_access_token = build_user_credential_access_token(
                    user, client, self.env_config.oauth2_secret_key, client_scopes
                )

                authentication_response = build_authentication_response(
                    self.env_config.oauth2_secret_key, new_access_token, refresh_token
                )

            self._delete_access_token_by_refresh_token_id(app_refresh_token.id)
            self._add_access_token(app_refresh_token.id, new_access_token)

            return authentication_response

    def _validate_client_credentials(self, client_id, client_secret):
        client = self._get_client_by_client_id(client_id)

        if self.password_encoder.validate_password(client_secret, client.client_secret) is False:
            raise InvalidCredentialsException("Invalid credentials")

    def _validate_user_credentials(self, client, username, password):
        user = self._get_user_by_username(username)

        if self.password_encoder.validate_password(password, user.password) is False:
            raise InvalidCredentialsException("Invalid credentials")
        self._get_client_user_by_username_and_app_client_id(username, client.id)

    def _get_user_by_username(self, username):
        with self.engine.begin() as conn:
            user = conn.execute(
                text(SQL_QUERY_TO_GET_USER_BY_USERNAME),
                {"username": username},
            )
            user_as_dict = user.mappings().first()

            if not user_as_dict:
                raise WrongCredentialsException("Invalid credentials")
        return user_as_dict

    def _get_client_by_id(self, app_client_id):
        with self.engine.begin() as conn:
            client = conn.execute(
                text(SQL_QUERY_TO_GET_CLIENT_BY_ID),
                {"id": app_client_id},
            )
            client_as_dict = client.mappings().first()

            if not client_as_dict:
                raise WrongCredentialsException("Invalid credentials")

        return client_as_dict

    def _get_client_by_client_id(self, client_id):
        with self.engine.begin() as conn:
            client = conn.execute(
                text(SQL_QUERY_TO_GET_CLIENT_BY_CLIENT_ID),
                {"client_id": client_id},
            )
            client_as_dict = client.mappings().first()

            if not client_as_dict:
                raise WrongCredentialsException("Invalid credentials")

        return client_as_dict

    def _get_refresh_token_by_access_refresh_token_and_client_id(
        self, access_token, refresh_token, client_id, username
    ):

        with self.engine.begin() as conn:
            refresh_token = conn.execute(
                text(SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_ACCESS_REFRESH_TOKEN_AND_CLIENT),
                {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "client_id": client_id,
                    "username": username or "",
                },
            )
            refresh_token_as_dict = refresh_token.mappings().first()

            if not refresh_token_as_dict:
                raise WrongCredentialsException("Invalid credentials")

        return refresh_token_as_dict

    def _get_scope_by_app_client_id(self, app_client_id):
        with self.engine.begin() as conn:
            client_scope = conn.execute(
                text(SQL_QUERY_TO_GET_SCOPES_BY_CLIENT_ID),
                {"id": app_client_id},
            )

            if not client_scope:
                raise WrongCredentialsException("Invalid credentials")

        return [scope[0] for scope in client_scope]

    def _get_client_user_by_username_and_app_client_id(self, username, app_client_id):
        with self.engine.begin() as conn:
            client_user = conn.execute(
                text(SQL_QUERY_TO_GET_CLIENT_USER_BY_USERNAME_AND_CLIENT_ID),
                {"username": username, "app_client_id": app_client_id},
            )
            client_user_as_dict = client_user.mappings().first()

            if not client_user_as_dict:
                raise WrongCredentialsException("Invalid credentials")

        return client_user_as_dict

    def _add_refresh_token(self, token, app_client_id, grant_type):
        with self.engine.begin() as conn:
            conn.execute(
                text(SQL_QUERY_TO_ADD_REFRESH_TOKEN),
                {
                    "token": token,
                    "app_client_id": app_client_id,
                    "grant_type": grant_type,
                },
            )

            persisted_refresh_token = conn.execute(
                text(SQL_QUERY_TO_GET_REFRESH_TOKEN_BY_TOKEN), {"token": token}
            )
            persisted_refresh_token_as_dict = persisted_refresh_token.mappings().first()
        return persisted_refresh_token_as_dict

    def _add_access_token(self, refresh_token_id, token):
        with self.engine.begin() as conn:
            conn.execute(
                text(SQL_QUERY_TO_ADD_ACCESS_TOKEN),
                {"refresh_token_id": refresh_token_id, "token": token},
            )

    def _delete_access_token_by_refresh_token_id(self, refresh_token_id):
        with self.engine.begin() as conn:
            conn.execute(
                text(SQL_QUERY_TO_DELETE_ACCESS_TOKEN_BY_REFRESH_TOKEN_ID),
                {"app_refresh_token_id": refresh_token_id},
            )

    def _delete_refresh_token(self, token):
        with self.engine.begin() as conn:
            conn.execute(
                text(SQL_QUERY_TO_DELETE_REFRESH_TOKEN),
                {"token": token},
            )
