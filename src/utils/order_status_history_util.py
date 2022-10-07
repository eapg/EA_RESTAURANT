from datetime import datetime
from functools import reduce


def _update_to_status_and_to_time(
    updated_last_status_histories,
    last_order_status_history,
    order_status_histories,
    updated_by,
):
    """
    This function update the to_status and to_time of the last order status history taking the from_status and from
    time of the new order status history of an order, using the order id.
    """
    order_status_history_filtered = list(
        filter(
            lambda order_status_history: last_order_status_history.order_id
            == order_status_history.order_id,
            order_status_histories,
        )
    )

    last_order_status_history.update_by = updated_by
    last_order_status_history.update_date = datetime.now()
    last_order_status_history.to_status = order_status_history_filtered[
        0
    ].from_status
    last_order_status_history.to_time = order_status_history_filtered[0].from_time
    updated_last_status_histories.append(last_order_status_history)

    return updated_last_status_histories


def update_last_order_status_history(
    last_order_status_histories, order_status_histories, updated_by
):

    updated_last_order_status_histories = reduce(
        lambda updated_last_status_histories, order_status_history: _update_to_status_and_to_time(
            updated_last_status_histories,
            order_status_history,
            order_status_histories,
            updated_by,
        ),
        last_order_status_histories,
        [],
    )
    return updated_last_order_status_histories
