from dataclasses import dataclass


@dataclass
class BaseEntityArgs:

    entity_status = None
    created_by = None
    created_date = None
    updated_by = None
    updated_date = None
