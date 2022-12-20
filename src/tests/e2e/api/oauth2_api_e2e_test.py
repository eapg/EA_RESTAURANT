from datetime import datetime, timedelta

import jwt

from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.endpoint_request_fixture import (
    create_refresh_token_request,
    build_access_token,
    build_refresh_token,
)
from src.tests.utils.fixtures.mapping_orm_fixtures import (
    create_user_with_procedure,
    insert_access_and_refresh_token_in_db,
)
from src.tests.utils.fixtures.oauth2_fixture import (
    build_login_client_json,
    build_login_user_json,
)
from src.tests.utils.fixtures.token_fixture import build_expire_access_token


class Oauth2ApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        self.engine.execute(f"TRUNCATE app_access_tokens RESTART IDENTITY CASCADE;")
        self.engine.execute(f"TRUNCATE app_refresh_tokens RESTART IDENTITY CASCADE;")
        self.login_client = build_login_client_json()
        self.login_user = build_login_user_json()

        self.test_access_token = build_access_token(self.env_config.oauth2_secret_key)
        self.test_refresh_token = build_refresh_token(self.env_config.oauth2_secret_key)

    def test_login_client_successfully(self):

        request = self.client.post("/login", json=self.login_client)
        request_as_json = request.get_json()
        token_decoded = jwt.decode(
            request_as_json.get("access_token"),
            self.env_config.oauth2_secret_key,
            algorithms="HS256",
        )

        self.assertEqual(
            token_decoded.get("client_name"), request_as_json.get("client_name")
        )
        self.assertEqual(token_decoded.get("scopes"), request_as_json.get("scopes"))

    def test_login_user_successfully(self):
        create_user_with_procedure(
            engine=self.engine,
            user_name="ea_test",
            username="ep_1234",
            password="1234abcd",
        )
        request = self.client.post("/login", json=self.login_user)
        request_as_json = request.get_json()
        token_decoded = jwt.decode(
            request_as_json.get("access_token"),
            self.env_config.oauth2_secret_key,
            algorithms="HS256",
        )

        self.assertEqual(
            token_decoded.get("user").get("username"),
            request_as_json.get("user").get("username"),
        )
        self.assertEqual(
            token_decoded.get("user").get("name"),
            request_as_json.get("user").get("name"),
        )
        self.assertEqual(
            token_decoded.get("user").get("last_name"),
            request_as_json.get("user").get("last_name"),
        )
        self.assertEqual(
            token_decoded.get("user").get("roles"),
            request_as_json.get("user").get("roles"),
        )
        self.assertEqual(token_decoded.get("scopes"), request_as_json.get("scopes"))

    def test_refresh_token_endpoint_with_valid_access_token(self):

        refresh_token_request = create_refresh_token_request(
            access_token=self.test_access_token, refresh_token=self.test_refresh_token
        )
        insert_access_and_refresh_token_in_db(
            engine=self.engine,
            access_token=self.test_access_token,
            refresh_token=self.test_refresh_token,
        )

        request = self.client.post("/refresh_token", json=refresh_token_request)
        request_as_json = request.get_json()

        self.assertEqual(
            refresh_token_request.get("access_token"),
            request_as_json.get("access_token"),
        )

    def test_refresh_token_endpoint_with_expired_access_token(self):

        expired_access_token = build_expire_access_token()
        refresh_token_request = create_refresh_token_request(
            access_token=expired_access_token, refresh_token=self.test_refresh_token
        )
        insert_access_and_refresh_token_in_db(
            engine=self.engine,
            access_token=expired_access_token,
            refresh_token=self.test_refresh_token,
        )
        request = self.client.post("/refresh_token", json=refresh_token_request)
        request_as_json = request.get_json()
        decoded_access_token = jwt.decode(
            request_as_json.get("access_token"),
            self.env_config.oauth2_secret_key,
            algorithms="HS256",
        )
        self.assertEqual(decoded_access_token.get("client_name"), "postman")
        self.assertNotEqual(
            refresh_token_request.get("access_token"),
            request_as_json.get("access_token"),
        )
