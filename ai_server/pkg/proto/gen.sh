#!/usr/bin/env
python3 -m grpc_tools.protoc --proto_path=. --python_out=../grpc --grpc_python_out=../grpc camera_stream_info.proto
