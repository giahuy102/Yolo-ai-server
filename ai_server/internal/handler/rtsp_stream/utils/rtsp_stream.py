import numpy as np

from .....pkg.config.config import config
from ...tracking.tracker import Tracker
from ...sort_tracking.tracker import SortTracker

TRACKING_CONFIG = config["tracking"]

class RTSPStream:
    def __init__(self, camera_id, rtsp_url, event_key, iot_event_zone_coords, camera_event_zone_coords, stream_id=None): 
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.event_key = event_key

        self.iot_event_zone_coords = iot_event_zone_coords
        self.camera_event_zone_coords = camera_event_zone_coords

        self.stream_id = stream_id if stream_id else self.camera_id
        self.line_coords = None # list of coordinate [x, y, x, y]
        self.line_crossing_vector = None # list of coordinate [x, y, x, y]

        # self.tracker = Tracker()

        self.tracker = SortTracker() if TRACKING_CONFIG["algorithm"] == TRACKING_CONFIG["sort"] else Tracker()
        
        self.cur_detection_frame = np.random.randint(255, size=(640, 640, 3), dtype=np.uint8)


    def set_line_coords(self, line_coords):
        self.line_coords = line_coords

    def set_line_crosssing_vector(self, line_crossing_vector):
        self.line_crossing_vector = line_crossing_vector

    def get_cur_detection_frame(self):
        return self.cur_detection_frame

    def set_cur_detection_frame(self, cur_detection_frame):
        self.cur_detection_frame = cur_detection_frame
    