
from ..rtsp_stream.stream_loader import StreamLoader
from ..event_detection.detection_utils import DetectionUtils

class EventDetected:
    def preprocess_frame(self, manager, detection_results, line_crossing_coords=None):
        frame_info = detection_results.frame_info

        detection_utils = DetectionUtils()

        
        detection_results = detection_utils.filter_results(detection_results, frame_info.iot_event_zone_coords, frame_info.camera_event_zone_coords, True)

        obj_names = [result.name for result in detection_results.results]
        frame_info.tracker.update(detection_results.xywhs, detection_results.confss, obj_names, detection_results.img_frame)

        
        detection_utils.preprocess_frame(detection_results, frame_info.iot_event_zone_coords, frame_info.camera_event_zone_coords, True, line_crossing_coords)
        
        stream_loader = StreamLoader.get_instance()
        stream_info = stream_loader.get_stream_info_by_id(detection_results.frame_info.stream_id)
        if stream_info:
            stream_info.set_cur_detection_frame(detection_results.img_frame_with_box)

        
        
        if not manager.allow_detection(frame_info.event_key, detection_results.cur_time):
            return False
        return True
