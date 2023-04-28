import grpc


class GrpcClient:
    def __init__(self, host, server_port):
        self.host = host
        self.server_port = server_port
        self.channel = grpc.insecure_channel(
            "{}:{}".format(self.host, self.server_port)
        )

    def get_channel(self):
        return self.channel
