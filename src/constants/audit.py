from enum import Enum


class Status(Enum):
    ACTIVE = "ACTIVE"
    DELETED = "DELETE"


class InternalUsers(Enum):
    SEEDER = 1
    KITCHEN_SIMULATOR = 2
