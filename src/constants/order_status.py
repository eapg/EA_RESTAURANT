from enum import Enum

"""
Orders lifecycle:

When an order is create its first status is "new_order", after the order passed through all validations, like 
ingredient availability validation the order is passed to "order_placed" status,if the order don't passed any of
the validations the order will pass to "cancelled" status, after that an available chef take the order and change
its status to "in_process". When the order runs out of preparation time the chef puts the order in "complete"
status.
"""


class OrderStatus(Enum):
    NEW_ORDER = "new_order"
    ORDER_PLACED = "order_placed"
    IN_PROCESS = "in_process"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
