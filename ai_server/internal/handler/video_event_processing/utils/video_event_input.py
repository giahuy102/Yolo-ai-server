
from .....pkg.config.config import config
from ...tracking.tracker import Tracker
from ...sort_tracking.tracker import SortTracker

TRACKING_CONFIG = config["tracking"]

class VideoEventInput:
    def __init__(self, event_id, event_key, video_url, start_time, end_time, target_time, iot_event_zone_coords, camera_event_zone_coords, detection_image_url=None, image_url=None, line_coords=None, line_crossing_vector=None):
        self.event_id = event_id
        self.event_key = event_key
        self.video_url = video_url
        self.start_time = start_time
        self.end_time = end_time
        self.target_time = target_time

        self.iot_event_zone_coords = iot_event_zone_coords
        self.camera_event_zone_coords = camera_event_zone_coords

        self.detection_image_url = detection_image_url
        self.image_url = image_url
        self.line_coords = line_coords

        self.line_crossing_vector = line_crossing_vector

        self.tracker = SortTracker() if TRACKING_CONFIG["algorithm"] == TRACKING_CONFIG["sort"] else Tracker()
