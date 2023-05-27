import numpy as np


from ...tracking.tracker import Tracker


class RTSPStream:
    def __init__(self, camera_id, rtsp_url, event_key, iot_event_zone_coords, camera_event_zone_coords, stream_id=None): 
        self.camera_id = camera_id
        self.rtsp_url = rtsp_url
        self.event_key = event_key

        self.iot_event_zone_coords = iot_event_zone_coords
        self.camera_event_zone_coords = camera_event_zone_coords

        self.stream_id = stream_id if stream_id else self.camera_id
        self.line_coords = None # list of coordinate [x, y, x, y]


        self.tracker = Tracker()

        
        self.cur_detection_frame = np.random.randint(255, size=(640, 640, 3), dtype=np.uint8)


    def set_line_coords(self, line_coords):
        self.line_coords = line_coords

    def get_cur_detection_frame(self):
        return self.cur_detection_frame

    def set_cur_detection_frame(self, cur_detection_frame):
        self.cur_detection_frame = cur_detection_frame
    