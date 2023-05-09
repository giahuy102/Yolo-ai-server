from flask import Flask, send_from_directory
from pathlib import Path

from ....pkg.config.config import config

HTTP_SERVER = config["server"]["http"]

app = Flask(__name__, static_folder=None)
folder_path = Path(__file__).parents[3] / 'static'
@app.route('/static/<path:path>')  
def send_file(path):
    return send_from_directory(folder_path, path)
    

class HttpServer:
    def __init__(self, flask_app=app):
        self.app = flask_app

    def start(self):
        self.app.run(host='0.0.0.0', port=HTTP_SERVER["port"])
