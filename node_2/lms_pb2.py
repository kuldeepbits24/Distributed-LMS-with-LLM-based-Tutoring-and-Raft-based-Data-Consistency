# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: lms.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tlms.proto\x12\x03lms\"G\n\x0fRegisterRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x10\n\x08userType\x18\x03 \x01(\t\"\x12\n\x10HeartbeatRequest\"$\n\x11HeartbeatResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"4\n\x10RegisterResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"2\n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"A\n\rLoginResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\r\n\x05token\x18\x02 \x01(\t\x12\x10\n\x08userType\x18\x03 \x01(\t\"$\n\x13GetLLMAnswerRequest\x12\r\n\x05query\x18\x01 \x01(\t\"7\n\x14GetLLMAnswerResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0e\n\x06\x61nswer\x18\x02 \x01(\t\"\x1e\n\rLogoutRequest\x12\r\n\x05token\x18\x01 \x01(\t\"!\n\x0eLogoutResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"A\n\x15PostAssignmentRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x19\n\x11\x61ssignmentContent\x18\x02 \x01(\t\")\n\x16PostAssignmentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"&\n\x15GetAssignmentsRequest\x12\r\n\x05token\x18\x01 \x01(\t\">\n\x16GetAssignmentsResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x13\n\x0b\x61ssignments\x18\x02 \x03(\t\"C\n\x17SubmitAssignmentRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x19\n\x11submissionContent\x18\x02 \x01(\t\"+\n\x18SubmitAssignmentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\"\"\n\x11ViewGradesRequest\x12\r\n\x05token\x18\x01 \x01(\t\"[\n\x12ViewGradesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1e\n\x06grades\x18\x02 \x03(\x0b\x32\x0e.lms.GradeInfo\x12\x14\n\x0c\x65rrorMessage\x18\x03 \x01(\t\"3\n\tGradeInfo\x12\x17\n\x0fstudentUsername\x18\x01 \x01(\t\x12\r\n\x05grade\x18\x02 \x01(\t\"7\n\x10PostQueryRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x14\n\x0cqueryContent\x18\x02 \x01(\t\"5\n\x11PostQueryResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"&\n\x15ViewAllQueriesRequest\x12\r\n\x05token\x18\x01 \x01(\t\":\n\x16ViewAllQueriesResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07queries\x18\x02 \x03(\t\"O\n\x16GradeAssignmentRequest\x12\r\n\x05token\x18\x01 \x01(\t\x12\x17\n\x0fstudentUsername\x18\x02 \x01(\t\x12\r\n\x05grade\x18\x03 \x01(\t\"@\n\x17GradeAssignmentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x14\n\x0c\x65rrorMessage\x18\x02 \x01(\t\"b\n\x12RequestVoteRequest\x12\x13\n\x0b\x63\x61ndidateId\x18\x01 \x01(\t\x12\x0c\n\x04term\x18\x02 \x01(\x05\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"8\n\x13RequestVoteResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0bvoteGranted\x18\x02 \x01(\x08\"\x97\x01\n\x14\x41ppendEntriesRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\t\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1e\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\r.lms.LogEntry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\"6\n\x15\x41ppendEntriesResponse\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\")\n\x08LogEntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07\x63ommand\x18\x02 \x01(\t2\xa7\x07\n\x03LMS\x12\x37\n\x08Register\x12\x14.lms.RegisterRequest\x1a\x15.lms.RegisterResponse\x12.\n\x05Login\x12\x11.lms.LoginRequest\x1a\x12.lms.LoginResponse\x12\x31\n\x06Logout\x12\x12.lms.LogoutRequest\x1a\x13.lms.LogoutResponse\x12I\n\x0ePostAssignment\x12\x1a.lms.PostAssignmentRequest\x1a\x1b.lms.PostAssignmentResponse\x12I\n\x0eGetAssignments\x12\x1a.lms.GetAssignmentsRequest\x1a\x1b.lms.GetAssignmentsResponse\x12O\n\x10SubmitAssignment\x12\x1c.lms.SubmitAssignmentRequest\x1a\x1d.lms.SubmitAssignmentResponse\x12=\n\nViewGrades\x12\x16.lms.ViewGradesRequest\x1a\x17.lms.ViewGradesResponse\x12:\n\tPostQuery\x12\x15.lms.PostQueryRequest\x1a\x16.lms.PostQueryResponse\x12I\n\x0eViewAllQueries\x12\x1a.lms.ViewAllQueriesRequest\x1a\x1b.lms.ViewAllQueriesResponse\x12L\n\x0fGradeAssignment\x12\x1b.lms.GradeAssignmentRequest\x1a\x1c.lms.GradeAssignmentResponse\x12\x46\n\rappendEntries\x12\x19.lms.AppendEntriesRequest\x1a\x1a.lms.AppendEntriesResponse\x12\x43\n\x0cGetLLMAnswer\x12\x18.lms.GetLLMAnswerRequest\x1a\x19.lms.GetLLMAnswerResponse\x12:\n\tHeartbeat\x12\x15.lms.HeartbeatRequest\x1a\x16.lms.HeartbeatResponse\x12@\n\x0brequestVote\x12\x17.lms.RequestVoteRequest\x1a\x18.lms.RequestVoteResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'lms_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_REGISTERREQUEST']._serialized_start=18
  _globals['_REGISTERREQUEST']._serialized_end=89
  _globals['_HEARTBEATREQUEST']._serialized_start=91
  _globals['_HEARTBEATREQUEST']._serialized_end=109
  _globals['_HEARTBEATRESPONSE']._serialized_start=111
  _globals['_HEARTBEATRESPONSE']._serialized_end=147
  _globals['_REGISTERRESPONSE']._serialized_start=149
  _globals['_REGISTERRESPONSE']._serialized_end=201
  _globals['_LOGINREQUEST']._serialized_start=203
  _globals['_LOGINREQUEST']._serialized_end=253
  _globals['_LOGINRESPONSE']._serialized_start=255
  _globals['_LOGINRESPONSE']._serialized_end=320
  _globals['_GETLLMANSWERREQUEST']._serialized_start=322
  _globals['_GETLLMANSWERREQUEST']._serialized_end=358
  _globals['_GETLLMANSWERRESPONSE']._serialized_start=360
  _globals['_GETLLMANSWERRESPONSE']._serialized_end=415
  _globals['_LOGOUTREQUEST']._serialized_start=417
  _globals['_LOGOUTREQUEST']._serialized_end=447
  _globals['_LOGOUTRESPONSE']._serialized_start=449
  _globals['_LOGOUTRESPONSE']._serialized_end=482
  _globals['_POSTASSIGNMENTREQUEST']._serialized_start=484
  _globals['_POSTASSIGNMENTREQUEST']._serialized_end=549
  _globals['_POSTASSIGNMENTRESPONSE']._serialized_start=551
  _globals['_POSTASSIGNMENTRESPONSE']._serialized_end=592
  _globals['_GETASSIGNMENTSREQUEST']._serialized_start=594
  _globals['_GETASSIGNMENTSREQUEST']._serialized_end=632
  _globals['_GETASSIGNMENTSRESPONSE']._serialized_start=634
  _globals['_GETASSIGNMENTSRESPONSE']._serialized_end=696
  _globals['_SUBMITASSIGNMENTREQUEST']._serialized_start=698
  _globals['_SUBMITASSIGNMENTREQUEST']._serialized_end=765
  _globals['_SUBMITASSIGNMENTRESPONSE']._serialized_start=767
  _globals['_SUBMITASSIGNMENTRESPONSE']._serialized_end=810
  _globals['_VIEWGRADESREQUEST']._serialized_start=812
  _globals['_VIEWGRADESREQUEST']._serialized_end=846
  _globals['_VIEWGRADESRESPONSE']._serialized_start=848
  _globals['_VIEWGRADESRESPONSE']._serialized_end=939
  _globals['_GRADEINFO']._serialized_start=941
  _globals['_GRADEINFO']._serialized_end=992
  _globals['_POSTQUERYREQUEST']._serialized_start=994
  _globals['_POSTQUERYREQUEST']._serialized_end=1049
  _globals['_POSTQUERYRESPONSE']._serialized_start=1051
  _globals['_POSTQUERYRESPONSE']._serialized_end=1104
  _globals['_VIEWALLQUERIESREQUEST']._serialized_start=1106
  _globals['_VIEWALLQUERIESREQUEST']._serialized_end=1144
  _globals['_VIEWALLQUERIESRESPONSE']._serialized_start=1146
  _globals['_VIEWALLQUERIESRESPONSE']._serialized_end=1204
  _globals['_GRADEASSIGNMENTREQUEST']._serialized_start=1206
  _globals['_GRADEASSIGNMENTREQUEST']._serialized_end=1285
  _globals['_GRADEASSIGNMENTRESPONSE']._serialized_start=1287
  _globals['_GRADEASSIGNMENTRESPONSE']._serialized_end=1351
  _globals['_REQUESTVOTEREQUEST']._serialized_start=1353
  _globals['_REQUESTVOTEREQUEST']._serialized_end=1451
  _globals['_REQUESTVOTERESPONSE']._serialized_start=1453
  _globals['_REQUESTVOTERESPONSE']._serialized_end=1509
  _globals['_APPENDENTRIESREQUEST']._serialized_start=1512
  _globals['_APPENDENTRIESREQUEST']._serialized_end=1663
  _globals['_APPENDENTRIESRESPONSE']._serialized_start=1665
  _globals['_APPENDENTRIESRESPONSE']._serialized_end=1719
  _globals['_LOGENTRY']._serialized_start=1721
  _globals['_LOGENTRY']._serialized_end=1762
  _globals['_LMS']._serialized_start=1765
  _globals['_LMS']._serialized_end=2700
# @@protoc_insertion_point(module_scope)
