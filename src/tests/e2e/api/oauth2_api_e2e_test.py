import jwt

from src.tests.e2e.base_flask_setup_test import BaseFlaskSetupTest
from src.tests.utils.fixtures.mapping_orm_fixtures import create_user_with_procedure
from src.tests.utils.fixtures.oauth2_fixture import (
    build_login_client_json,
    build_login_user_json,
)


class Oauth2ApiE2ETest(BaseFlaskSetupTest):
    def after_base_setup(self):
        self.engine.execute(f"TRUNCATE app_access_tokens RESTART IDENTITY CASCADE;")
        self.engine.execute(f"TRUNCATE app_refresh_tokens RESTART IDENTITY CASCADE;")
        self.login_client = build_login_client_json()
        self.login_user = build_login_user_json()

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
