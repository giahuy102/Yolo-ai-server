
from ..event_detection.detection_utils import DetectionUtils

class EventDetected:
    def preprocess_frame(self, manager, detection_results, line_crossing_coords=None):

        obj_names = [result.name for result in detection_results.results]
        manager.event_input.tracker.update(detection_results.xywhs, detection_results.confss, obj_names, detection_results.img_frame)

        detection_utils = DetectionUtils()
        event_input = manager.event_input
        detection_utils.preprocess_frame(detection_results, event_input.iot_event_zone_coords, event_input.camera_event_zone_coords, manager.is_ai_event, line_crossing_coords)
