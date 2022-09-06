from src.utils import utils


class AbstractEntity:

    id = None  # integer
    entity_status = None  # enum
    created_date = None  # datetime
    created_by = None  # enum
    updated_date = None  # datetime
    updated_by = None  # enum

    def __eq__(self, other):
        return utils.equals(self, other)
