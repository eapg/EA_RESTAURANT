from enum import Enum


class EtlStatus(Enum):
    UNPROCESSED = "UNPROCESSED"
    PROCESSED = "PROCESSED"
