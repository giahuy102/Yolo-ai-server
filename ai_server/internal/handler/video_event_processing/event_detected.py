
from ..event_detection.sort_detection_utils import DetectionUtils

class EventDetected:
    def preprocess_frame(self, manager, detection_results):
        detection_utils = DetectionUtils()
        event_input = manager.event_input
        detection_results = detection_utils.filter_results(detection_results, event_input.iot_event_zone_coords, event_input.camera_event_zone_coords, manager.is_ai_event)        
        detection_utils.preprocess_frame(detection_results, event_input.iot_event_zone_coords, event_input.camera_event_zone_coords, manager.is_ai_event, event_input.tracker)
