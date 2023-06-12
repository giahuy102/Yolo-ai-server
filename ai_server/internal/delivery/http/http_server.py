from flask import Flask, send_from_directory, Response, request
from pathlib import Path
import cv2

from ...handler.rtsp_stream.stream_loader import StreamLoader
from ....pkg.config.config import config

stream_loader = StreamLoader().get_instance()
HTTP_SERVER = config["server"]["http"]

app = Flask(__name__, static_folder=None)
folder_path = Path(__file__).parents[3] / 'static'
@app.route('/static/<path:path>')  
def send_file(path):
    return send_from_directory(folder_path, path)


def get_detection_frame(stream_id):
    while True:
        with stream_loader.access_detection_frame_condition:
            stream_loader.access_detection_frame_condition.wait()
        frame = stream_loader.get_cur_detection_frame_by_stream_id(stream_id)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        print("User access detection frame")
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/live')
def stream_detection_video():
    args = request.args
    stream_id = args.get('stream_id')
    return Response(get_detection_frame(stream_id), mimetype='multipart/x-mixed-replace; boundary=frame')
    

class HttpServer:
    def __init__(self, flask_app=app):
        self.app = flask_app

    def start(self):
        self.app.run(host='0.0.0.0', port=HTTP_SERVER["port"])
