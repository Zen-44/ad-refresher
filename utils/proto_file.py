# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto_file
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nproto_file\"-\n\x0eProtoAdBurnKey\x12\x0b\n\x03\x63id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\"I\n\rProtoAdTarget\x12\x10\n\x08language\x18\x01 \x01(\t\x12\x0b\n\x03\x61ge\x18\x02 \x01(\x05\x12\n\n\x02os\x18\x03 \x01(\t\x12\r\n\x05stake\x18\x04 \x01(\x05\"\x8a\x01\n\x0cProtoProfile\x12)\n\x03\x61\x64s\x18\x01 \x03(\x0b\x32\x1c.ProtoProfile.ProtoProfileAd\x1aO\n\x0eProtoProfileAd\x12\x0b\n\x03\x63id\x18\x01 \x01(\t\x12\x0e\n\x06target\x18\x02 \x01(\t\x12\x10\n\x08\x63ontract\x18\x03 \x01(\t\x12\x0e\n\x06\x61uthor\x18\x04 \x01(\t\"\"\n\x13ProtoBurnAttachment\x12\x0b\n\x03key\x18\x01 \x01(\t\"\x8e\x01\n\x07ProtoAd\x12\r\n\x05title\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x65sc\x18\x02 \x01(\t\x12\x0b\n\x03url\x18\x03 \x01(\t\x12\r\n\x05thumb\x18\x04 \x01(\x0c\x12\r\n\x05media\x18\x05 \x01(\x0c\x12\x0f\n\x07version\x18\x06 \x01(\r\x12*\n\x0cvotingParams\x18\x07 \x01(\x0b\x32\x14.ProtoAdVotingParams\"r\n\x13ProtoAdVotingParams\x12\x16\n\x0evotingDuration\x18\x01 \x01(\r\x12\x1c\n\x14publicVotingDuration\x18\x02 \x01(\r\x12\x0e\n\x06quorum\x18\x03 \x01(\r\x12\x15\n\rcommitteeSize\x18\x04 \x01(\r\"\xda\x01\n\x10ProtoTransaction\x12$\n\x04\x64\x61ta\x18\x01 \x01(\x0b\x32\x16.ProtoTransaction.Data\x12\x11\n\tsignature\x18\x02 \x01(\x0c\x12\x0e\n\x06useRlp\x18\x03 \x01(\x08\x1a}\n\x04\x44\x61ta\x12\r\n\x05nonce\x18\x01 \x01(\r\x12\r\n\x05\x65poch\x18\x02 \x01(\r\x12\x0c\n\x04type\x18\x03 \x01(\r\x12\n\n\x02to\x18\x04 \x01(\x0c\x12\x0e\n\x06\x61mount\x18\x05 \x01(\x0c\x12\x0e\n\x06maxFee\x18\x06 \x01(\x0c\x12\x0c\n\x04tips\x18\x07 \x01(\x0c\x12\x0f\n\x07payload\x18\x08 \x01(\x0c\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto_file_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_PROTOADBURNKEY']._serialized_start=14
  _globals['_PROTOADBURNKEY']._serialized_end=59
  _globals['_PROTOADTARGET']._serialized_start=61
  _globals['_PROTOADTARGET']._serialized_end=134
  _globals['_PROTOPROFILE']._serialized_start=137
  _globals['_PROTOPROFILE']._serialized_end=275
  _globals['_PROTOPROFILE_PROTOPROFILEAD']._serialized_start=196
  _globals['_PROTOPROFILE_PROTOPROFILEAD']._serialized_end=275
  _globals['_PROTOBURNATTACHMENT']._serialized_start=277
  _globals['_PROTOBURNATTACHMENT']._serialized_end=311
  _globals['_PROTOAD']._serialized_start=314
  _globals['_PROTOAD']._serialized_end=456
  _globals['_PROTOADVOTINGPARAMS']._serialized_start=458
  _globals['_PROTOADVOTINGPARAMS']._serialized_end=572
  _globals['_PROTOTRANSACTION']._serialized_start=575
  _globals['_PROTOTRANSACTION']._serialized_end=793
  _globals['_PROTOTRANSACTION_DATA']._serialized_start=668
  _globals['_PROTOTRANSACTION_DATA']._serialized_end=793
# @@protoc_insertion_point(module_scope)