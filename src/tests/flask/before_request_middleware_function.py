import jwt

from flask import make_response
from src.constants.http import HttpStatus
from src.env_config import get_env_config_instance
from src.exceptions.exceptions import UnAuthorizedEndpoint
from src.lib.repositories.impl_v2.oauth2_repository_impl import Oauth2RepositoryImpl
from src.utils import oauth2_util


def before_request_middleware(ioc_instance, request):
    ioc = ioc_instance
    oauth2_repository = ioc.get(Oauth2RepositoryImpl)
    env_config = get_env_config_instance()
    endpoint_protected = oauth2_util.is_endpoint_protected(request)

    if endpoint_protected:
        try:

            authorization_header = request.headers.get("Authorization")
            authorization_header_split = authorization_header.split(" ")
            access_token = authorization_header_split[1]
            oauth2_repository.validate_token(access_token)

            oauth2_util.validate_roles_and_scopes(env_config.oauth2_secret_key, request)

        except jwt.exceptions.ExpiredSignatureError as token_expired:
            response = make_response(str(token_expired), HttpStatus.UNAUTHORIZED.value)
            return response

        except jwt.exceptions.InvalidSignatureError as token_invalid:
            response = make_response(str(token_invalid), HttpStatus.UNAUTHORIZED.value)
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
