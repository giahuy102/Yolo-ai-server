from flask import Flask
app = Flask(__name__)


from .internal.delivery.rabbitmq.consumers import Consumers
from .internal.delivery.stream_detector.stream_detector import StreamDetector
from .internal.delivery.grpc.server import GrpcServer

def main():
    consumers = Consumers()
    consumers.start()

    grpc_server = GrpcServer()
    grpc_server.start()

    stream_detector = StreamDetector()
    stream_detector.start()



main()