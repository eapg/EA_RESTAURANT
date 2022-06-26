from src.utils.utils import equals


class AbstractEntity:
    id = None  # integer
    entity_status = None  # enum
    create_date = None  # datetime
    create_by = None  # enum
    update_date = None  # datetime
    update_by = None  # enum

    def __eq__(self, other):
        return equals(self, other)
