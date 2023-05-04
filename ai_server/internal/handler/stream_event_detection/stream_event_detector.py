from ..object_detection.yolov7.object_detector import ObjectDetector
from .utils.stream_event_manager import StreamEventManager
from .object_detected import ObjectDetected
from .crowd_gathering_detected import CrowdGatheringDetected
from .line_crossing_detected import LineCrossingDetected
from ....pkg.config.config import config

EVENT_CONFIG = config["event"]
IOT_EVENT_CONFIG = EVENT_CONFIG["iot"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]

class StreamEventDetector:

    def preprocess_stream(self, stream_event_input):
        self.manager.process_stream_loader(stream_event_input) \
                    .process_detection_stream() \
                    .process_directory()

    def execute_event_frame(self, detection_results):
        frame_info = detection_results.frame_info
        event_key = frame_info.event_key
        # if event_key in [IOT_EVENT_CONFIG["door_open"]["key"], IOT_EVENT_CONFIG["movement"]["key"]]:
        #     ObjectDetected().execute(self.manager, detection_results, self.manager.callback_output) 
        if event_key == CAMERA_EVENT_CONFIG["crowd_gathering"]["key"]:
            CrowdGatheringDetected().execute(self.manager, detection_results, self.manager.callback_output)
        elif event_key == CAMERA_EVENT_CONFIG["line_crossing"]["key"]:
            LineCrossingDetected().execute(self.manager, detection_results, self.manager.callback_output)

    def execute(self, stream_event_input, callback):
        self.manager = StreamEventManager()
        self.manager.set_callback_output(callback)
        self.preprocess_stream(stream_event_input)
        detector = ObjectDetector()
        detector.detect(self.manager.detection_stream, self.execute_event_frame)
