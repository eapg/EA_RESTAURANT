from enum import Enum


class EtlStatus(Enum):
    UNPROCESSED = "UNPROCESSED"
    PROCESSED = "PROCESSED"


class Service(Enum):
    UNASSIGNED = "UNASSIGNED"
    PYTHON_ETL = "PYTHON_ETL"
    JAVA_ETL = "JAVA_ETL"
