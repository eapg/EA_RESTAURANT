import grpc


class UnAuthorizedEndpoint(Exception):
    pass


class BcryptException(Exception):
    pass


class WrongCredentialsException(Exception):
    pass


class GrpcPermissionDeniedException(grpc.RpcError):
    def __init__(self, code):
        self._code = code

    def code(self):
        return self._code
