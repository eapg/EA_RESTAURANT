import base64
import unittest

from src.constants.http import HttpMethods
from src.constants.oauth2 import Roles, Scopes
from src.env_config import get_env_config_instance
from src.exceptions.exceptions import UnAuthorizedEndpoint
from src.tests.utils.fixtures.endpoint_request_fixture import create_request
from src.tests.utils.fixtures.token_fixture import (
    build_user_access_token,
    build_client_access_token,
)
from src.utils.oauth2_util import (
    validate_roles_and_scopes,
    is_endpoint_protected,
    build_authentication_response,
)


class Oauth2UtilTest(unittest.TestCase):
    def setUp(self) -> None:
        self.env_config = get_env_config_instance()

    def test_validated_roles_and_scopes_with_valid_role(self):

        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=Scopes.READ.value
        )
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=access_token,
        )
        validation = validate_roles_and_scopes(
            self.env_config.oauth2_secret_key, request
        )
        print(validation)
        self.assertEqual(validation, None)

    def test_validated_roles_and_scopes_without_valid_role(self):

        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=Scopes.READ.value
        )
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=access_token,
        )
        self.assertRaises(
            UnAuthorizedEndpoint,
            validate_roles_and_scopes,
            self.env_config.oauth2_secret_key,
            request,
        )

    def test_is_endpoint_protected(self):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=Scopes.READ.value
        )
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=access_token,
        )

        protected = is_endpoint_protected(request)
        self.assertTrue(protected)

    def test_build_authentication_response_for_user_login_successfully(self):

        access_token = build_user_access_token(
            scopes=[Scopes.READ.value], roles=Roles.ADMINISTRATOR.value
        )
        refresh_token = "test refresh token"
        authorization_response = build_authentication_response(
            self.env_config.oauth2_secret_key, access_token, refresh_token
        )
        self.assertEqual(authorization_response.get("access_token"), access_token)
        self.assertEqual(authorization_response.get("refresh_token"), refresh_token)
        self.assertEqual(authorization_response.get("scopes"), [Scopes.READ.value])
        self.assertEqual(
            authorization_response.get("user").get("roles"), [Roles.ADMINISTRATOR.value]
        )
        print(authorization_response)

    def test_build_authentication_response_for_client_login_successfully(self):

        access_token = build_client_access_token(scopes=[Scopes.READ.value])
        refresh_token = "test refresh token"
        authorization_response = build_authentication_response(
            self.env_config.oauth2_secret_key, access_token, refresh_token
        )

        self.assertEqual(authorization_response.get("scopes"), [Scopes.READ.value])
        self.assertNotIn("user", authorization_response)

    def test_decrypt_client_credentials(self):

        client_credentials = "client_id:client_secret"
        client_credentials_encrypted = base64.b64encode(
            client_credentials.encode("utf-8")
        )
        decrypted_client_credentials = base64.b64decode(
            client_credentials_encrypted
        ).decode("utf-8")

        self.assertEqual(client_credentials, decrypted_client_credentials)
