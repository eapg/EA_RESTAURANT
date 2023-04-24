import grpc
from src.proto import java_etl_grpc_client_pb2_grpc


class GrpcClient:
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port)
        )

    def get_service_stub(self):
        return java_etl_grpc_client_pb2_grpc.Oauth2ServiceStub(self.channel)
