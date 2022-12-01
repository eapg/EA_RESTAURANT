import unittest

from src.constants.oauth2 import GranType
from src.env_config import get_env_config_instance
from src.lib.repositories.impl_v2.oauth2_repository_impl import Oauth2RepositoryImpl
from unittest import mock

from src.tests.utils.fixtures.oauth2_fixture import (
    build_user,
    build_client,
    build_client_user,
    build_refresh_token,
)
from src.utils.oauth2_util import (
    build_client_credentials_access_token,
    build_client_credentials_refresh_token,
    build_user_credential_access_token,
    build_user_credential_refresh_token,
)


def mock_oauth2_repository(
    oauth2_repository, client, user, client_user, client_scope
):

    oauth2_repository._get_user_by_username = mock.Mock()
    oauth2_repository._get_user_by_username.return_value = user

    oauth2_repository._get_client_by_id = mock.Mock()
    oauth2_repository._get_client_by_id.return_value = client

    oauth2_repository._get_client_by_client_id = mock.Mock()
    oauth2_repository._get_client_by_client_id.return_value = client

    oauth2_repository._get_scope_by_app_client_id = mock.Mock()
    oauth2_repository._get_scope_by_app_client_id.return_value = client_scope

    oauth2_repository._get_client_user_by_username_and_app_client_id = mock.Mock()
    oauth2_repository._get_client_user_by_username_and_app_client_id.return_value = (
        client_user
    )

    oauth2_repository._add_refresh_token = mock.Mock()

    oauth2_repository._add_access_token = mock.Mock()

    oauth2_repository._delete_access_token_by_refresh_token_id = mock.Mock()

    oauth2_repository._delete_refresh_token = mock.Mock()

    return oauth2_repository


class Oauth2RepositoryImplTest(unittest.TestCase):
    def setUp(self):
        self.env_config = get_env_config_instance()
        self.mocked_engine = mock.Mock()
        self.mocked_engine.begin.return_value.__enter__ = mock.Mock()
        self.mocked_engine.begin.return_value.__exit__ = mock.Mock()

        self.oauth2_repository = Oauth2RepositoryImpl(self.mocked_engine)

        self.test_client_id = "client1234"
        self.test_client_secret = "1234"

    @mock.patch(
        "src.lib.repositories.impl_v2.oauth2_repository_impl.build_client_credentials_refresh_token",
    )
    @mock.patch(
        "src.lib.repositories.impl_v2.oauth2_repository_impl.build_client_credentials_access_token",
    )
    def test_login_client_successfully(
        self, mocked_build_client_access_token, mocked_build_client_refresh_token
    ):
        user = build_user()
        client = build_client()
        client_user = build_client_user()
        client_scope = ["READ/WRITE", "WRITE"]

        client_access_token = build_client_credentials_access_token(
            client, client_scope, self.env_config.oauth2_secret_key
        )
        mocked_build_client_access_token.return_value = client_access_token
        client_refresh_token = build_client_credentials_refresh_token(
            client, client_scope, self.env_config.oauth2_secret_key
        )
        mocked_build_client_refresh_token.return_value = client_refresh_token

        mocked_oauth2_repository = (
            mock_oauth2_repository(
                self.oauth2_repository, client, user, client_user, client_scope
            )
        )

        app_refresh_token = build_refresh_token(
            id=1,
            token=client_refresh_token,
            grant_type=GranType.CLIENT_CREDENTIALS.value,
        )
        mocked_oauth2_repository._add_refresh_token.return_value = (
            app_refresh_token
        )

        tokens = mocked_oauth2_repository.login_client(
            self.test_client_id, self.test_client_secret
        )

        mocked_oauth2_repository._get_client_by_client_id.assert_called_with(
            self.test_client_id
        )
        mocked_oauth2_repository._get_scope_by_app_client_id.assert_called_with(
            client.id
        )
        mocked_build_client_access_token.assert_called_with(
            client, client_scope, self.env_config.oauth2_secret_key
        )
        mocked_build_client_refresh_token.assert_called_with(
            client, client_scope, self.env_config.oauth2_secret_key
        )

        mocked_oauth2_repository._add_refresh_token.assert_called_with(
            tokens["refresh_token"], client.id, GranType.CLIENT_CREDENTIALS.value
        )

        mocked_oauth2_repository._add_access_token.assert_called_with(
            app_refresh_token.id, tokens["access_token"]
        )
        self.assertEqual(client_access_token, tokens["access_token"])
        self.assertEqual(client_refresh_token, tokens["refresh_token"])

    @mock.patch(
        "src.lib.repositories.impl_v2.oauth2_repository_impl.build_user_credential_refresh_token",
    )
    @mock.patch(
        "src.lib.repositories.impl_v2.oauth2_repository_impl.build_user_credential_access_token",
    )
    def test_login_user_successfully(
        self, mocked_build_user_access_token, mocked_build_user_refresh_token
    ):
        user = build_user()
        client = build_client()
        client_user = build_client_user()
        client_scope = ["READ/WRITE", "WRITE"]

        user_access_token = build_user_credential_access_token(
            user, client, self.env_config.oauth2_secret_key, client_scope
        )
        mocked_build_user_access_token.return_value = user_access_token
        user_refresh_token = build_user_credential_refresh_token(
            user, client, self.env_config.oauth2_secret_key, client_scope
        )
        mocked_build_user_refresh_token.return_value = user_refresh_token

        mocked_oauth2_repository = (
            mock_oauth2_repository(
                self.oauth2_repository, client, user, client_user, client_scope
            )
        )

        app_refresh_token = build_refresh_token(
            id=1,
            token=user_refresh_token,
            grant_type=GranType.PASSWORD.value,
        )
        mocked_oauth2_repository._add_refresh_token.return_value = (
            app_refresh_token
        )

        tokens = mocked_oauth2_repository.login_user(
            self.test_client_id, self.test_client_secret, user.username, user.password
        )

        mocked_oauth2_repository._get_client_by_client_id.assert_called_with(
            self.test_client_id
        )
        mocked_oauth2_repository._get_scope_by_app_client_id.assert_called_with(
            client.id
        )
        mocked_build_user_access_token.assert_called_with(
            user, client, self.env_config.oauth2_secret_key, client_scope
        )
        mocked_build_user_refresh_token.assert_called_with(
            user, client, self.env_config.oauth2_secret_key, client_scope
        )

        mocked_oauth2_repository._add_refresh_token(
            tokens["refresh_token"], client.id, GranType.CLIENT_CREDENTIALS.value
        )
        mocked_oauth2_repository._add_refresh_token.assert_called_with(
            tokens["refresh_token"], client.id, GranType.CLIENT_CREDENTIALS.value
        )

        mocked_oauth2_repository._add_access_token.assert_called_with(
            app_refresh_token.id, tokens["access_token"]
        )
        self.assertEqual(user_access_token, tokens["access_token"])
        self.assertEqual(user_refresh_token, tokens["refresh_token"])

    @mock.patch("src.lib.repositories.impl_v2.oauth2_repository_impl.jwt")
    def test_validate_token_successfully(self, mocked_jwt):
        user = build_user()
        client = build_client()
        client_scope = ["READ/WRITE", "WRITE"]

        access_token_to_validate = build_user_credential_access_token(
            user, client, self.env_config.oauth2_secret_key, client_scope
        )
        self.oauth2_repository.validate_token(access_token_to_validate)
        mocked_jwt.decode.assert_called_with(
            access_token_to_validate,
            self.env_config.oauth2_secret_key,
            algorithms="HS256",
        )

    @mock.patch(
        "src.lib.repositories.impl_v2.oauth2_repository_impl.build_client_credentials_access_token",
    )
    def test_refresh_token_successfully(self, mocked_build_client_access_token):
        user = build_user()
        client = build_client()
        client_user = build_client_user()
        client_scope = ["READ/WRITE", "WRITE"]

        new_client_access_token = build_client_credentials_access_token(
            client, client_scope, self.env_config.oauth2_secret_key
        )
        mocked_build_client_access_token.return_value = new_client_access_token
        client_refresh_token = build_client_credentials_refresh_token(
            client, client_scope, self.env_config.oauth2_secret_key
        )

        app_refresh_token = build_refresh_token(
            id=1,
            token=client_refresh_token,
            grant_type=GranType.CLIENT_CREDENTIALS.value,
        )

        mocked_oauth2_repository = (
            mock_oauth2_repository(
                self.oauth2_repository, client, user, client_user, client_scope
            )
        )
        mocked_oauth2_repository._get_refresh_token_by_token = (
            mock.Mock()
        )
        mocked_oauth2_repository._get_refresh_token_by_token.return_value = (
            app_refresh_token
        )

        token = mocked_oauth2_repository.refresh_token(
            client_refresh_token
        )
        mocked_oauth2_repository._delete_access_token_by_refresh_token_id.assert_called_with(
            app_refresh_token.id
        )
        mocked_oauth2_repository._add_access_token.assert_called_with(
            app_refresh_token.id, new_client_access_token
        )
        self.assertEqual(new_client_access_token, token["access_token"])
