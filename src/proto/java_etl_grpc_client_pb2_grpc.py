# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from src.proto import java_etl_grpc_client_pb2 as src_dot_proto_dot_java__etl__grpc__client__pb2


class Oauth2ServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.loginClient = channel.unary_unary(
                '/Oauth2Service/loginClient',
                request_serializer=src_dot_proto_dot_java__etl__grpc__client__pb2.NotParametersRequest.SerializeToString,
                response_deserializer=src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.FromString,
                )
        self.refreshToken = channel.unary_unary(
                '/Oauth2Service/refreshToken',
                request_serializer=src_dot_proto_dot_java__etl__grpc__client__pb2.RefreshTokenRequest.SerializeToString,
                response_deserializer=src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.FromString,
                )


class Oauth2ServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def loginClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def refreshToken(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_Oauth2ServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'loginClient': grpc.unary_unary_rpc_method_handler(
                    servicer.loginClient,
                    request_deserializer=src_dot_proto_dot_java__etl__grpc__client__pb2.NotParametersRequest.FromString,
                    response_serializer=src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.SerializeToString,
            ),
            'refreshToken': grpc.unary_unary_rpc_method_handler(
                    servicer.refreshToken,
                    request_deserializer=src_dot_proto_dot_java__etl__grpc__client__pb2.RefreshTokenRequest.FromString,
                    response_serializer=src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Oauth2Service', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Oauth2Service(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def loginClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Oauth2Service/loginClient',
            src_dot_proto_dot_java__etl__grpc__client__pb2.NotParametersRequest.SerializeToString,
            src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def refreshToken(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Oauth2Service/refreshToken',
            src_dot_proto_dot_java__etl__grpc__client__pb2.RefreshTokenRequest.SerializeToString,
            src_dot_proto_dot_java__etl__grpc__client__pb2.Oauth2TokenResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)