# entity to manage order status history
from src.utils.utils import equals


class OrderStatusHistory:
    def __init__(self):
        self.id = None # integer
        self.order = None  # obj
        self.from_time = None  # time
        self.to_time = None  # time
        self.from_status = None  # Enum
        self.to_status = None  # Enum
        self.entity_status = None  # enum
        self.create_date = None  # date
        self.update_date = None  # date
        self.create_by = None  # obj
        self.update_by = None  # obj

    def __eq__(self, other):
        return equals(self, other)
