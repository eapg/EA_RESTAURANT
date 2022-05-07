from enum import Enum


class OrderStatus(Enum):

    ORDER_PLACED = "order_placed"
    IN_PROCESS = "in_process"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
