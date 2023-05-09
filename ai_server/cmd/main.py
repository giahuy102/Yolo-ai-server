# from flask import Flask


from ai_server.internal.delivery.rabbitmq.consumers import Consumers
from ai_server.internal.delivery.stream_detector.stream_detector import StreamDetector
from ai_server.internal.delivery.grpc.grpc_server import GrpcServer
from ai_server.internal.delivery.http.http_server import HttpServer

from ai_server.pkg.logger.logger import set_logger

def main():

    set_logger()

    consumers = Consumers()
    consumers.start()

    grpc_server = GrpcServer()
    grpc_server.start()

    stream_detector = StreamDetector()
    stream_detector.start()

    http_server = HttpServer()
    http_server.start()

    # from datetime import datetime
    # import pytz
    # tz = pytz.timezone('Asia/Ho_Chi_Minh')
    # print(datetime.now(tz).isoformat())

    # app = Flask(__name__, static_folder=None)

    # from pathlib import Path
    # folder_path = Path(__file__).parents[1] / 'static'
    # print(folder_path)
    # from flask import send_from_directory
    # @app.route('/static/<path:path>')  
    # def send_file(path):
    #     print("send")
    #     return send_from_directory(folder_path, path)




    # app.run(host='0.0.0.0', port=5005)



main()
