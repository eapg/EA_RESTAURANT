from unittest import mock
import jwt

from src.constants.http import HttpMethods
from src.constants.oauth2 import Roles, Scopes

from src.flask.routes.security_route_middleware import setup_security_route_middleware
from src.tests.flask.before_request_middleware_function import before_request_middleware
from src.tests.flask.flask__base_endpoint_function_test import (
    FlaskBaseEndpointFunctionTest,
)
from src.tests.utils.fixtures.endpoint_request_fixture import create_request
from src.tests.utils.fixtures.token_fixture import (
    build_user_access_token,
    build_expire_access_token,
    build_invalid_access_token,
)
from src.utils import oauth2_util


class SecurityRouteMiddlewareIntegrationTest(FlaskBaseEndpointFunctionTest):
    def after_base_setup(self):

        self.security_route_middleware_blueprint = setup_security_route_middleware(
            self.ioc
        )

    @mock.patch(
        "src.tests.flask.before_request_middleware_function.oauth2_util.validate_roles_and_scopes",
        return_value=oauth2_util.validate_roles_and_scopes,
    )
    @mock.patch(
        "src.tests.flask.before_request_middleware_function.oauth2_util.is_endpoint_protected",
        return_value=oauth2_util.is_endpoint_protected,
    )
    def test_before_request_protected_endpoints(
        self, mocked_func_is_endpoint_protected, mocked_func_validate_roles_and_scopes
    ):
        access_token = build_user_access_token(
            roles=Roles.ADMINISTRATOR.value, scopes=Scopes.READ.value
        )
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=access_token,
        )

        self.security_route_middleware_blueprint.before_app_request(
            before_request_middleware(self.ioc, request)
        )
        mocked_func_is_endpoint_protected.assert_called_with(request)
        mocked_func_validate_roles_and_scopes.assert_called_with(
            self.env_config.oauth2_secret_key, request
        )

    @mock.patch(
        "src.tests.flask.before_request_middleware_function.make_response",
        return_value=jwt.exceptions.InvalidSignatureError,
    )
    def test_before_request_invalid_access_token(self, mocked_invalid_token):
        invalid_access_token = build_invalid_access_token()
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=invalid_access_token,
        )

        response = self.security_route_middleware_blueprint.before_app_request(
            before_request_middleware(self.ioc, request)
        )
        self.assertEqual(response, jwt.exceptions.InvalidSignatureError)

    @mock.patch(
        "src.tests.flask.before_request_middleware_function.make_response",
        return_value=jwt.exceptions.ExpiredSignatureError,
    )
    def test_before_request_expired_access_token(self, mocked_make_response):
        expired_access_token = build_expire_access_token()
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=expired_access_token,
        )

        response = self.security_route_middleware_blueprint.before_app_request(
            before_request_middleware(self.ioc, request)
        )
        self.assertEqual(response, jwt.exceptions.ExpiredSignatureError)

    @mock.patch(
        "src.tests.flask.before_request_middleware_function.make_response",
        return_value=jwt.exceptions.DecodeError,
    )
    def test_before_request_token_incorrect(self, mocked_incomplete_token):
        expired_access_token = build_expire_access_token()
        request = create_request(
            url="/chefs/<chef_id>",
            method=HttpMethods.GET.value,
            access_token=expired_access_token,
        )

        response = self.security_route_middleware_blueprint.before_app_request(
            before_request_middleware(self.ioc, request)
        )
        self.assertEqual(response, jwt.exceptions.DecodeError)
