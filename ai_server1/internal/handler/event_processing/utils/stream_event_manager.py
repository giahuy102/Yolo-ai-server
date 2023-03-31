from pathlib import Path

from ...rtsp_stream.stream_loader import StreamLoader
from .....pkg.config.config import config
from ...object_detection.yolov7.utils.detection_stream import DetectionStream


ROOT_INDEX = 3
SERVER_CONFIG = config["server"]["http"]
STATIC_CONFIG = config["static"]
PATH_CONFIG = STATIC_CONFIG["path"]
ROOT_PATH = str(Path(__file__).parents[ROOT_INDEX])

class StreamEventManager:
    
    def process_stream_loader(self, event_input):
        self.stream_loader = StreamLoader(event_input.stream_infos)

    def process_detection_stream(self):
        self.detection_stream = DetectionStream(self.stream_loader)


    def save_image(self):


