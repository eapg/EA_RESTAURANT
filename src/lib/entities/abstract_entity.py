from src.utils.utils import equals


class AbstractEntity:

    id = None  # integer
    entity_status = None  # enum
    created_date = None  # datetime
    created_by = None  # enum
    updated_date = None  # datetime
    updated_by = None  # enum

    def __eq__(self, other):
        return equals(self, other)
