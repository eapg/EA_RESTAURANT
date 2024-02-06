from enum import Enum


class HttpStatus(Enum):
    OK = 200
    CREATED = 201
    UNAUTHORIZED = 401


class HttpMethods(Enum):
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"
