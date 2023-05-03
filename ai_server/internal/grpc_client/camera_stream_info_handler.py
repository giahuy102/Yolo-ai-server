import grpc
from ...pkg.grpc import camera_stream_info_pb2_grpc
from ...pkg.grpc import camera_stream_info_pb2

from ...pkg.config.config import config

TARGET_GRPC_SERVER = config["api_server"]["grpc"]


class CameraStreamHandler:

    def get_all_camera_streams(self):
        channel = grpc.insecure_channel(f"{TARGET_GRPC_SERVER['host']}:{TARGET_GRPC_SERVER['port']}")
        stub = camera_stream_info_pb2_grpc.CameraStreamInfoServiceStub(channel)
        camera_streams = stub.GetAllCameraStreams(camera_stream_info_pb2.Empty()).camera_streams
        return camera_streams
