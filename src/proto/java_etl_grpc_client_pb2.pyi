from google.protobuf import wrappers_pb2 as _wrappers_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InsertMongoOrderStatusHistoriesResponse(_message.Message):
    __slots__ = ["uuids"]
    UUIDS_FIELD_NUMBER: _ClassVar[int]
    uuids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, uuids: _Optional[_Iterable[str]] = ...) -> None: ...

class MongoOrderStatusHistoriesFromPythonRequest(_message.Message):
    __slots__ = ["mongoOrderStatusHistory"]
    MONGOORDERSTATUSHISTORY_FIELD_NUMBER: _ClassVar[int]
    mongoOrderStatusHistory: _containers.RepeatedCompositeFieldContainer[MongoOrderStatusHistory]
    def __init__(self, mongoOrderStatusHistory: _Optional[_Iterable[_Union[MongoOrderStatusHistory, _Mapping]]] = ...) -> None: ...

class MongoOrderStatusHistory(_message.Message):
    __slots__ = ["createdBy", "createdDate", "entityStatus", "etlStatus", "fromStatus", "fromTime", "id", "orderId", "toStatus", "toTime", "updatedBy", "updatedDate"]
    CREATEDBY_FIELD_NUMBER: _ClassVar[int]
    CREATEDDATE_FIELD_NUMBER: _ClassVar[int]
    ENTITYSTATUS_FIELD_NUMBER: _ClassVar[int]
    ETLSTATUS_FIELD_NUMBER: _ClassVar[int]
    FROMSTATUS_FIELD_NUMBER: _ClassVar[int]
    FROMTIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    ORDERID_FIELD_NUMBER: _ClassVar[int]
    TOSTATUS_FIELD_NUMBER: _ClassVar[int]
    TOTIME_FIELD_NUMBER: _ClassVar[int]
    UPDATEDBY_FIELD_NUMBER: _ClassVar[int]
    UPDATEDDATE_FIELD_NUMBER: _ClassVar[int]
    createdBy: int
    createdDate: int
    entityStatus: str
    etlStatus: str
    fromStatus: str
    fromTime: int
    id: str
    orderId: int
    toStatus: _wrappers_pb2.StringValue
    toTime: _wrappers_pb2.Int64Value
    updatedBy: int
    updatedDate: int
    def __init__(self, id: _Optional[str] = ..., orderId: _Optional[int] = ..., fromTime: _Optional[int] = ..., toTime: _Optional[_Union[_wrappers_pb2.Int64Value, _Mapping]] = ..., fromStatus: _Optional[str] = ..., toStatus: _Optional[_Union[_wrappers_pb2.StringValue, _Mapping]] = ..., etlStatus: _Optional[str] = ..., entityStatus: _Optional[str] = ..., createdBy: _Optional[int] = ..., updatedBy: _Optional[int] = ..., createdDate: _Optional[int] = ..., updatedDate: _Optional[int] = ...) -> None: ...

class NotParametersRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Oauth2TokenResponse(_message.Message):
    __slots__ = ["accessToken", "clientName", "expiresIn", "refreshToken", "scopes"]
    ACCESSTOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENTNAME_FIELD_NUMBER: _ClassVar[int]
    EXPIRESIN_FIELD_NUMBER: _ClassVar[int]
    REFRESHTOKEN_FIELD_NUMBER: _ClassVar[int]
    SCOPES_FIELD_NUMBER: _ClassVar[int]
    accessToken: str
    clientName: str
    expiresIn: int
    refreshToken: str
    scopes: str
    def __init__(self, accessToken: _Optional[str] = ..., refreshToken: _Optional[str] = ..., expiresIn: _Optional[int] = ..., scopes: _Optional[str] = ..., clientName: _Optional[str] = ...) -> None: ...

class RefreshTokenRequest(_message.Message):
    __slots__ = ["accessToken", "clientId", "clientSecret", "refreshToken"]
    ACCESSTOKEN_FIELD_NUMBER: _ClassVar[int]
    CLIENTID_FIELD_NUMBER: _ClassVar[int]
    CLIENTSECRET_FIELD_NUMBER: _ClassVar[int]
    REFRESHTOKEN_FIELD_NUMBER: _ClassVar[int]
    accessToken: str
    clientId: str
    clientSecret: str
    refreshToken: str
    def __init__(self, refreshToken: _Optional[str] = ..., accessToken: _Optional[str] = ..., clientId: _Optional[str] = ..., clientSecret: _Optional[str] = ...) -> None: ...
