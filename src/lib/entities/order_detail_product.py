from src.utils.utils import equals


class OrderDetailProduct:
    def __init__(self):
        self.id = None  # integer
        self.order_detail = None  # object
        self.product = None  # object
        self.quantity = None  # integer

    def __eq__(self, other):
        return equals(self, other)
