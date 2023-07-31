from datetime import datetime

from src.constants.audit import Status
from src.constants.etl_status import EtlStatus
from src.constants.order_status import OrderStatus
from src.proto import java_etl_grpc_client_pb2_old
from src.utils.time_util import get_unix_time_stamp_milliseconds


def build_login_client_response():
    return java_etl_grpc_client_pb2.Oauth2TokenResponse(
        accessToken="test access token",
        refreshToken="test refresh token",
        expiresIn=10,
        scopes="READ",
        clientName="test client",
    )


def build_refresh_token_request():
    return java_etl_grpc_client_pb2.RefreshTokenRequest(
        refreshToken="test refresh token",
        accessToken="test access token",
        clientId="python_client_001",
        clientSecret="python_secret_001",
    )


def build_grpc_mongo_order_status_history(id=None):
    return java_etl_grpc_client_pb2.MongoOrderStatusHistory(
        id=id or "63656f20f2a8a6a247ae31cc",
        orderId=1,
        fromTime=int(get_unix_time_stamp_milliseconds(datetime.now())),
        toTime=int(get_unix_time_stamp_milliseconds(datetime.now())),
        fromStatus=OrderStatus.NEW_ORDER.value,
        toStatus=OrderStatus.IN_PROCESS.value,
        etlStatus=EtlStatus.UNPROCESSED.value,
        entityStatus=Status.ACTIVE.value,
        createdBy=1,
        updatedBy=1,
        createdDate=int(get_unix_time_stamp_milliseconds(datetime.now())),
        updatedDate=int(get_unix_time_stamp_milliseconds(datetime.now())),
    )


def build_uuids_response(uuids=None):
    return java_etl_grpc_client_pb2.InsertMongoOrderStatusHistoriesResponse(uuids=uuids)


def build_refresh_token_response():
    return java_etl_grpc_client_pb2.Oauth2TokenResponse(
        accessToken="test new access token",
        refreshToken="test same refresh token",
        expiresIn=10,
        scopes="READ",
        clientName="test client",
    )
