from enum import Enum


class GranTypes(Enum):

    CLIENT_CREDENTIALS = "CLIENT_CREDENTIALS"
    PASSWORD = "PASSWORD"


class Roles(Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    CHEF = "CHEF"
    CLIENT = "CLIENT"
    CASHIER = "CASHIER"
    SEEDER = "SEEDER"
    KITCHEN_SIMULATOR = "KITCHEN_SIMULATOR"


class Scopes(Enum):
    WRITE = "WRITE"
    READ = "READ"
    READ_WRITE = "READ/WRITE"
