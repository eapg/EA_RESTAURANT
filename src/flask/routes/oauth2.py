from flask import Blueprint, make_response, request

from src.constants.http import HttpStatus
from src.constants.oauth2 import GranTypes
from src.exceptions.exceptions import BcryptException, WrongCredentialsException
from src.lib.repositories.impl_v2.oauth2_repository_impl import Oauth2RepositoryImpl
from src.utils.oauth2_util import decrypt_client_credentials


def setup_oauth2_routes(ioc):

    oauth2_blueprint = Blueprint("oauth2_routes", __name__)
    oauth2_repository = ioc.get(Oauth2RepositoryImpl)

    @oauth2_blueprint.route("/login", methods=["POST"])
    def login():
        login_credentials = request.get_json()
        authorization_header = request.headers.get("Authorization")
        authorization_header_split = authorization_header.split(" ")
        decrypted_client_credentials = decrypt_client_credentials(
            authorization_header_split[1]
        )

        try:
            if login_credentials["grant_type"] == GranTypes.CLIENT_CREDENTIALS.value:

                token_response = oauth2_repository.login_client(
                    decrypted_client_credentials["client_id"],
                    decrypted_client_credentials["client_secret"],
                )

                login_response = make_response(token_response, HttpStatus.OK.value)

            elif login_credentials["grant_type"] == GranTypes.PASSWORD.value:

                token_response = oauth2_repository.login_user(
                    decrypted_client_credentials["client_id"],
                    decrypted_client_credentials["client_secret"],
                    login_credentials["username"],
                    login_credentials["password"],
                )

                login_response = make_response(token_response, HttpStatus.OK.value)

            return login_response

        except BcryptException as invalid_credentials:
            exception_response = make_response(
                str(invalid_credentials), HttpStatus.UNAUTHORIZED.value
            )
            return exception_response

        except WrongCredentialsException as invalid_credentials:
            exception_response = make_response(
                str(invalid_credentials), HttpStatus.UNAUTHORIZED.value
            )
            return exception_response

    @oauth2_blueprint.route("/refresh_token", methods=["POST"])
    def refresh_token():

        try:
            refresh_token_request = request.get_json()
            decrypted_client_credentials = decrypt_client_credentials(
                refresh_token_request["client_credentials"]
            )
            refresh_token = refresh_token_request["refresh_token"]
            access_token = refresh_token_request["access_token"]
            client_id = decrypted_client_credentials["client_id"]
            client_secret = decrypted_client_credentials["client_secret"]

            access_token_response = oauth2_repository.refresh_token(
                refresh_token, access_token, client_id, client_secret
            )
            refresh_token_response = make_response(
                access_token_response, HttpStatus.OK.value
            )
            return refresh_token_response

        except WrongCredentialsException as invalid_credentials:
            exception_response = make_response(
                str(invalid_credentials), HttpStatus.UNAUTHORIZED.value
            )
            return exception_response

    return oauth2_blueprint
