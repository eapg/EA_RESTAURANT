import unittest
from unittest import mock
from injector import Injector
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
)


class SecurityRouteMiddlewareTest(FlaskBaseEndpointFunctionTest):
    def after_base_setup(self):

        self.ioc.get = mock.Mock()
        self.security_route_middleware_blueprint = setup_security_route_middleware(
            self.ioc
        )

    @mock.patch(
        "src.tests.flask.before_request_middleware_function.oauth2_util.validate_roles_and_scopes"
    )
    @mock.patch(
        "src.tests.flask.before_request_middleware_function.oauth2_util.is_endpoint_protected",
        return_value=True,
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
