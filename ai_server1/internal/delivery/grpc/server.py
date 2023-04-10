import grpc
from concurrent import futures

from ....pkg.grpc import camera_stream_info_pb2_grpc
from .handler.camera_stream_info_handler import CameraStreamInfoHandler

class GrpcServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.init_service()

    def init_service(self):
        camera_stream_info_pb2_grpc.add_CameraStreamInfoServiceServicer_to_server(CameraStreamInfoHandler(), self.server)

    def start(self):
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        self.server.wait_for_termination()

