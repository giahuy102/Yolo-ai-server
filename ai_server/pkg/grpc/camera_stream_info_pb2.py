# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: camera_stream_info.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18\x63\x61mera_stream_info.proto\"\xde\x02\n\x12\x43\x61meraStreamDetail\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x17\n\x0frtsp_stream_url\x18\x02 \x01(\t\x12\x1b\n\x13sfu_rtsp_stream_url\x18\x03 \x01(\t\x12\x13\n\x0bis_set_line\x18\x04 \x01(\x08\x12\x11\n\tevent_key\x18\x05 \x01(\t\x12\x16\n\x0eoffset_x_begin\x18\x06 \x01(\x02\x12\x14\n\x0coffset_x_end\x18\x07 \x01(\x02\x12\x16\n\x0eoffset_y_begin\x18\x08 \x01(\x02\x12\x14\n\x0coffset_y_end\x18\t \x01(\x02\x12\x10\n\x08username\x18\n \x01(\t\x12\x10\n\x08password\x18\x0b \x01(\t\x12\x1d\n\x15iot_event_zone_coords\x18\x0c \x03(\x02\x12 \n\x18\x63\x61mera_event_zone_coords\x18\r \x03(\x02\x12\x1c\n\x14line_crossing_vector\x18\x0e \x03(\x02\"B\n\x14\x43\x61meraStreamResponse\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x0c\n\x04\x63ode\x18\x02 \x01(\t\x12\x0f\n\x07message\x18\x03 \x01(\t\"N\n\x19\x43reateCameraStreamRequest\x12\x31\n\x14\x63\x61mera_stream_detail\x18\x01 \x01(\x0b\x32\x13.CameraStreamDetail\"_\n\x1dUpdateCameraStreamByIdRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\x12\x31\n\x14\x63\x61mera_stream_detail\x18\x02 \x01(\x0b\x32\x13.CameraStreamDetail\",\n\x1d\x44\x65leteCameraStreamByIdRequest\x12\x0b\n\x03_id\x18\x01 \x01(\t\"i\n\x1bGetAllCameraStreamsResponse\x12+\n\x0e\x63\x61mera_streams\x18\x01 \x03(\x0b\x32\x13.CameraStreamDetail\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0c\n\x04\x63ode\x18\x03 \x01(\t\"\x07\n\x05\x45mpty2\xc9\x02\n\x17\x43\x61meraStreamInfoService\x12=\n\x13GetAllCameraStreams\x12\x06.Empty\x1a\x1c.GetAllCameraStreamsResponse\"\x00\x12I\n\x12\x43reateCameraStream\x12\x1a.CreateCameraStreamRequest\x1a\x15.CameraStreamResponse\"\x00\x12Q\n\x16UpdateCameraStreamById\x12\x1e.UpdateCameraStreamByIdRequest\x1a\x15.CameraStreamResponse\"\x00\x12Q\n\x16\x44\x65leteCameraStreamById\x12\x1e.DeleteCameraStreamByIdRequest\x1a\x15.CameraStreamResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'camera_stream_info_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CAMERASTREAMDETAIL._serialized_start=29
  _CAMERASTREAMDETAIL._serialized_end=379
  _CAMERASTREAMRESPONSE._serialized_start=381
  _CAMERASTREAMRESPONSE._serialized_end=447
  _CREATECAMERASTREAMREQUEST._serialized_start=449
  _CREATECAMERASTREAMREQUEST._serialized_end=527
  _UPDATECAMERASTREAMBYIDREQUEST._serialized_start=529
  _UPDATECAMERASTREAMBYIDREQUEST._serialized_end=624
  _DELETECAMERASTREAMBYIDREQUEST._serialized_start=626
  _DELETECAMERASTREAMBYIDREQUEST._serialized_end=670
  _GETALLCAMERASTREAMSRESPONSE._serialized_start=672
  _GETALLCAMERASTREAMSRESPONSE._serialized_end=777
  _EMPTY._serialized_start=779
  _EMPTY._serialized_end=786
  _CAMERASTREAMINFOSERVICE._serialized_start=789
  _CAMERASTREAMINFOSERVICE._serialized_end=1118
# @@protoc_insertion_point(module_scope)
