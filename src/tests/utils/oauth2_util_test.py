import unittest

from src.constants.http import HttpMethods
from src.constants.oauth2 import Roles, Scopes
from src.env_config import get_env_config_instance
from src.exceptions.exceptions import UnAuthorizedEndpoint
from src.tests.utils.fixtures.endpoint_request_fixture import create_request
from src.tests.utils.fixtures.token_fixture import build_user_access_token
from src.utils.oauth2_util import (
    validate_roles_and_scopes,
    is_endpoint_protected,
)


class Oauth2UtilTest(unittest.TestCase):
    def test_validated_roles_and_scopes_with_valid_role(self):
        env_config = get_env_config_instance()
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=Scopes.READ.value
        )
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=access_token,
        )
        validation = validate_roles_and_scopes(env_config.oauth2_secret_key, request)
        self.assertEqual(validation, None)

    def test_validated_roles_and_scopes_without_valid_role(self):
        env_config = get_env_config_instance()
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
            env_config.oauth2_secret_key,
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
