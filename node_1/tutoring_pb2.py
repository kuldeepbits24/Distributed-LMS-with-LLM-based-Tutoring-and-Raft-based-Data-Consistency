# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tutoring.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0etutoring.proto\x12\x08tutoring\"$\n\x13GetLLMAnswerRequest\x12\r\n\x05query\x18\x01 \x01(\t\"7\n\x14GetLLMAnswerResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0e\n\x06\x61nswer\x18\x02 \x01(\t\"7\n\x10PostQueryRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x14\n\x0cqueryContent\x18\x02 \x01(\t\"5\n\x11PostQueryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\x9f\x01\n\x08Tutoring\x12M\n\x0cGetLLMAnswer\x12\x1d.tutoring.GetLLMAnswerRequest\x1a\x1e.tutoring.GetLLMAnswerResponse\x12\x44\n\tPostQuery\x12\x1a.tutoring.PostQueryRequest\x1a\x1b.tutoring.PostQueryResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tutoring_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_GETLLMANSWERREQUEST']._serialized_start=28
  _globals['_GETLLMANSWERREQUEST']._serialized_end=64
  _globals['_GETLLMANSWERRESPONSE']._serialized_start=66
  _globals['_GETLLMANSWERRESPONSE']._serialized_end=121
  _globals['_POSTQUERYREQUEST']._serialized_start=123
  _globals['_POSTQUERYREQUEST']._serialized_end=178
  _globals['_POSTQUERYRESPONSE']._serialized_start=180
  _globals['_POSTQUERYRESPONSE']._serialized_end=233
  _globals['_TUTORING']._serialized_start=236
  _globals['_TUTORING']._serialized_end=395
# @@protoc_insertion_point(module_scope)
