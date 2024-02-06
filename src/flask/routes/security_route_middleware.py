from flask import Blueprint, request, make_response

import jwt

from src.constants.http import HttpStatus
from src.env_config import get_env_config_instance
from src.exceptions.exceptions import UnAuthorizedEndpoint
from src.lib.repositories.impl_v2.oauth2_repository_impl import Oauth2RepositoryImpl
from src.utils.oauth2_util import (
    validate_roles_and_scopes,
    is_endpoint_protected,
    get_request_token,
)


def setup_security_route_middleware(ioc):

    security_route_middleware_blueprint = Blueprint(
        "security_route_middleware_blueprint", __name__
    )
    oauth2_repository = ioc.get(Oauth2RepositoryImpl)

    @security_route_middleware_blueprint.before_app_request
    def before_request_middleware():
        env_config = get_env_config_instance()
        endpoint_protected = is_endpoint_protected(request)

        if endpoint_protected:
            try:

                token = get_request_token(request)
                oauth2_repository.validate_token(token)
                validate_roles_and_scopes(env_config.oauth2_secret_key, request)

            except jwt.exceptions.ExpiredSignatureError as token_expired:
                response = make_response(
                    str(token_expired), HttpStatus.UNAUTHORIZED.value
                )
                return response

            except jwt.exceptions.InvalidSignatureError as token_invalid:
                response = make_response(
                    str(token_invalid), HttpStatus.UNAUTHORIZED.value
                )
                return response

            except jwt.exceptions.DecodeError as token_incomplete:
                response = make_response(
                    str(token_incomplete), HttpStatus.UNAUTHORIZED.value
                )
                return response

            except UnAuthorizedEndpoint as unauthorized_access:
                response = make_response(
                    str(unauthorized_access), HttpStatus.UNAUTHORIZED.value
                )
                return response

    return security_route_middleware_blueprint
