from src.proto import java_etl_grpc_client_pb2
from src.utils.grpc_util import generate_basic_token_from_credentials


class EaRestaurantJavaEtlGrpcClient:
    def __init__(self, grpc_client):
        self.grpc_client = grpc_client
        self.service_stub = grpc_client.get_service_stub()

    def login_client(self, client_id, client_secret):
        basic_token = generate_basic_token_from_credentials(client_id, client_secret)
        metadata = (("authorization", basic_token),)
        no_param = java_etl_grpc_client_pb2.NotParametersRequest()
        return self.service_stub.loginClient(no_param, metadata=metadata)

    def refresh_token(self, refresh_token, access_token, client_id, client_secret):
        refresh_token_request = java_etl_grpc_client_pb2.RefreshTokenRequest(
            refreshToken=refresh_token,
            accessToken=access_token,
            clientId=client_id,
            clientSecret=client_secret,
        )
        return self.service_stub.refreshToken(refresh_token_request)