# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: src/proto/java_etl_grpc_client.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n$src/proto/java_etl_grpc_client.proto\"\x16\n\x14NotParametersRequest\"w\n\x13Oauth2TokenResponse\x12\x13\n\x0b\x61\x63\x63\x65ssToken\x18\x01 \x01(\t\x12\x14\n\x0crefreshToken\x18\x02 \x01(\t\x12\x11\n\texpiresIn\x18\x03 \x01(\x05\x12\x0e\n\x06scopes\x18\x04 \x01(\t\x12\x12\n\nclientName\x18\x05 \x01(\t\"h\n\x13RefreshTokenRequest\x12\x14\n\x0crefreshToken\x18\x01 \x01(\t\x12\x13\n\x0b\x61\x63\x63\x65ssToken\x18\x02 \x01(\t\x12\x10\n\x08\x63lientId\x18\x03 \x01(\t\x12\x14\n\x0c\x63lientSecret\x18\x04 \x01(\t\"8\n\'InsertMongoOrderStatusHistoriesResponse\x12\r\n\x05uuids\x18\x01 \x03(\t\"\xf7\x01\n\x17MongoOrderStatusHistory\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07orderId\x18\x02 \x01(\x03\x12\x10\n\x08\x66romTime\x18\x03 \x01(\x03\x12\x0e\n\x06toTime\x18\x04 \x01(\x03\x12\x12\n\nfromStatus\x18\x05 \x01(\t\x12\x10\n\x08toStatus\x18\x06 \x01(\t\x12\x11\n\tetlStatus\x18\x07 \x01(\t\x12\x14\n\x0c\x65ntityStatus\x18\x08 \x01(\t\x12\x11\n\tcreatedBy\x18\t \x01(\x03\x12\x11\n\tupdatedBy\x18\n \x01(\x03\x12\x13\n\x0b\x63reatedDate\x18\x0b \x01(\x03\x12\x13\n\x0bupdatedDate\x18\x0c \x01(\x03\"g\n*MongoOrderStatusHistoriesFromPythonRequest\x12\x39\n\x17mongoOrderStatusHistory\x18\x01 \x03(\x0b\x32\x18.MongoOrderStatusHistory2\x8b\x01\n\rOauth2Service\x12<\n\x0bloginClient\x12\x15.NotParametersRequest\x1a\x14.Oauth2TokenResponse\"\x00\x12<\n\x0crefreshToken\x12\x14.RefreshTokenRequest\x1a\x14.Oauth2TokenResponse\"\x00\x32\xa8\x01\n\x1eMongoOrderStatusHistoryService\x12\x85\x01\n,insertMongoOrderStatusHistoriesFromPythonEtl\x12+.MongoOrderStatusHistoriesFromPythonRequest\x1a(.InsertMongoOrderStatusHistoriesResponseb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'src.proto.java_etl_grpc_client_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NOTPARAMETERSREQUEST._serialized_start=40
  _NOTPARAMETERSREQUEST._serialized_end=62
  _OAUTH2TOKENRESPONSE._serialized_start=64
  _OAUTH2TOKENRESPONSE._serialized_end=183
  _REFRESHTOKENREQUEST._serialized_start=185
  _REFRESHTOKENREQUEST._serialized_end=289
  _INSERTMONGOORDERSTATUSHISTORIESRESPONSE._serialized_start=291
  _INSERTMONGOORDERSTATUSHISTORIESRESPONSE._serialized_end=347
  _MONGOORDERSTATUSHISTORY._serialized_start=350
  _MONGOORDERSTATUSHISTORY._serialized_end=597
  _MONGOORDERSTATUSHISTORIESFROMPYTHONREQUEST._serialized_start=599
  _MONGOORDERSTATUSHISTORIESFROMPYTHONREQUEST._serialized_end=702
  _OAUTH2SERVICE._serialized_start=705
  _OAUTH2SERVICE._serialized_end=844
  _MONGOORDERSTATUSHISTORYSERVICE._serialized_start=847
  _MONGOORDERSTATUSHISTORYSERVICE._serialized_end=1015
# @@protoc_insertion_point(module_scope)
