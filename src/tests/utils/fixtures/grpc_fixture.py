from src.proto import java_etl_grpc_client_pb2


def build_login_client_response():
    return java_etl_grpc_client_pb2.Oauth2TokenResponse(
        accessToken="test access token",
        refreshToken="test refresh token",
        expiresIn=10,
        scopes="READ",
        clientName="test client",
    )


def build_refresh_token_request():
    return java_etl_grpc_client_pb2.RefreshTokenRequest(
        refreshToken="test refresh token",
        accessToken="test access token",
        clientId="postman001",
        clientSecret="postmansecret01",
    )
