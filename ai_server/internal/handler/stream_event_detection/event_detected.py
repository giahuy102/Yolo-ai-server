
# from ..rtsp_stream.stream_loader import StreamLoader
# from ..event_detection.detection_utils import DetectionUtils
from ..event_detection.sort_detection_utils import DetectionUtils

class EventDetected:
    def preprocess_frame(self, manager, detection_results):
        frame_info = detection_results.frame_info
        detection_utils = DetectionUtils()
        detection_results = detection_utils.filter_results(detection_results, frame_info.iot_event_zone_coords, frame_info.camera_event_zone_coords, True)        
        detection_utils.preprocess_frame(detection_results, frame_info.iot_event_zone_coords, frame_info.camera_event_zone_coords, True, frame_info.tracker)
        
        frame_info.set_cur_detection_frame(detection_results.img_frame_with_box)

        if not manager.allow_detection(frame_info.event_key, frame_info.stream_id, detection_results.cur_time):
            return False
        return True
