import grpc
from concurrent import futures
import threading
import logging

from ....pkg.grpc import camera_stream_info_pb2_grpc
from .handler.camera_stream_info_handler import CameraStreamInfoHandler
from ....pkg.config.config import config

GRPC_SERVER = config["server"]["grpc"]

class GrpcServer:
    def __init__(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        self.init_service()

    def init_service(self):
        camera_stream_info_pb2_grpc.add_CameraStreamInfoServiceServicer_to_server(CameraStreamInfoHandler(), self.server)

    def start_grpc_server(self):
        self.server.add_insecure_port(f"[::]:{GRPC_SERVER['port']}")
        self.server.start()
        logging.info(f"Server started listening on port {GRPC_SERVER['port']}")
        self.server.wait_for_termination()


    def start(self):
        server_thread = threading.Thread(target=self.start_grpc_server)
        server_thread.start()
        return server_thread

