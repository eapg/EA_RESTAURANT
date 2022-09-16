def convert_mongo_order_status_history_to_postgres_order_status_history(
    mongo_order_status_history, postgres_order_status_history
):

    postgres_order_status_history.order_id = mongo_order_status_history.order_id
    postgres_order_status_history.from_time = mongo_order_status_history.from_time
    postgres_order_status_history.to_time = mongo_order_status_history.to_time
    postgres_order_status_history.from_status = mongo_order_status_history.from_status
    postgres_order_status_history.to_status = mongo_order_status_history.to_status
    postgres_order_status_history.entity_status = mongo_order_status_history.entity_status
    postgres_order_status_history.created_date = mongo_order_status_history.created_date
    postgres_order_status_history.created_by = mongo_order_status_history.created_by
    postgres_order_status_history.updated_date = mongo_order_status_history.updated_date
    postgres_order_status_history.updated_by = mongo_order_status_history.updated_by
    postgres_order_status_history.mongo_order_status_history_uuid = str(
        mongo_order_status_history.id
    )

    return postgres_order_status_history

