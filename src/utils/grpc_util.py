import base64

from src.proto import java_etl_grpc_client_pb2
from src.utils.time_util import get_unix_time_stamp_milliseconds


def generate_basic_token_from_credentials(client_id, client_secret):
    credentials = f"{client_id}:{client_secret}"
    basic_token_encode = base64.b64encode(credentials.encode("utf-8"))
    basic_token_decode = basic_token_encode.decode("utf-8")
    basic_token = f"Basic {basic_token_decode}"
    return basic_token


def map_mongo_order_status_history_to_grpc_mongo_order_status_history(
    mongo_order_status_history,
):
    return java_etl_grpc_client_pb2.MongoOrderStatusHistory(
        id=str(mongo_order_status_history.id),
        orderId=mongo_order_status_history.order_id,
        fromTime=get_unix_time_stamp_milliseconds(mongo_order_status_history.from_time),
        toTime=get_unix_time_stamp_milliseconds(mongo_order_status_history.to_time),
        fromStatus=mongo_order_status_history.from_status,
        toStatus=mongo_order_status_history.to_status,
        etlStatus=mongo_order_status_history.etl_status,
        entityStatus=mongo_order_status_history.entity_status,
        createdBy=mongo_order_status_history.created_by,
        updatedBy=mongo_order_status_history.updated_by,
        createdDate=get_unix_time_stamp_milliseconds(
            mongo_order_status_history.created_date
        ),
        updatedDate=get_unix_time_stamp_milliseconds(
            mongo_order_status_history.updated_date
        ),
    )


def map_mongo_order_status_histories_to_grpc_mongo_order_status_histories(
    mongo_order_status_histories,
):
    return list(
        map(
            map_mongo_order_status_history_to_grpc_mongo_order_status_history,
            mongo_order_status_histories,
        )
    )


def generate_bearer_token_from_access_token(access_token):
    return f"Bearer {access_token}"
