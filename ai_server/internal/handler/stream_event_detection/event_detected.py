
from ..event_detection.detection_utils import DetectionUtils

class EventDetected:
    def preprocess_frame(self, manager, detection_results, line_crossing_coords=None):
        frame_info = detection_results.frame_info
        if not manager.allow_detection(frame_info.event_key, detection_results.cur_time):
            return False
        detection_utils = DetectionUtils()
        detection_utils.preprocess_frame(detection_results, frame_info.iot_event_zone_coords, frame_info.camera_event_zone_coords, True, line_crossing_coords)
        return True
