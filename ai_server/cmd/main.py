from flask import Flask


from ai_server.internal.delivery.rabbitmq.consumers import Consumers
from ai_server.internal.delivery.stream_detector.stream_detector import StreamDetector
from ai_server.internal.delivery.grpc.server import GrpcServer

def main():
    consumers = Consumers()
    consumers.start()

    grpc_server = GrpcServer()
    grpc_server.start()

    stream_detector = StreamDetector()
    stream_detector.start()
    app = Flask(__name__)
    app.run(host='0.0.0.0', port=5005)



main()
