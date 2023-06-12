import logging
from .utils.video_event_manager import VideoEventManager
from ..object_detection.yolov7.object_detector import ObjectDetector
from .object_detected import ObjectDetected
from .crowd_gathering_detected import CrowdGatheringDetected
from .line_crossing_detected import LineCrossingDetected
from ....pkg.config.config import config

EVENT_CONFIG = config["event"]
IOT_EVENT_CONFIG = EVENT_CONFIG["iot"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]

class VideoEventProcessor:


    def preprocess_video_event(self, event_input):
        self.manager.process_path(event_input) \
                    .process_video(event_input) \
                    .process_directory() \
                    .process_download_general_video_file() \
                    .process_video_writer() \
                    .process_initial_event_data(event_input) \
                    .process_initial_detection_data()

    def postprocess_video_event(self):
        self.manager.process_save_images() \
                    .process_clear_file() \
                    .process_end_video() \
                    .process_event_output()


    def choose_event_callback(self):
        video_event_input = self.manager.event_input
        event_key = video_event_input.event_key
        if event_key in [IOT_EVENT_CONFIG["door_open"]["key"], IOT_EVENT_CONFIG["movement"]["key"]]:
            self.manager.set_callback_detection_result(ObjectDetected().execute)
        elif event_key == CAMERA_EVENT_CONFIG["crowd_gathering"]["key"]:
            self.manager.set_callback_detection_result(CrowdGatheringDetected().execute)
        elif event_key == CAMERA_EVENT_CONFIG["line_crossing"]["key"]:
            self.manager.set_callback_detection_result(LineCrossingDetected().execute)

        
    def execute_event_frame(self, detection_results):
        callback = self.manager.callback_detection_result
        callback(self.manager, detection_results)

    def execute(self, video_event_input, callback):
        
        try:
            print("Start to execute video event processor")
            self.manager = VideoEventManager()
            self.preprocess_video_event(video_event_input)
            self.choose_event_callback()
            detector = ObjectDetector()
            print("-------------Start to detect video-------------")
            detector.detect(self.manager.detection_video, self.execute_event_frame)
            self.postprocess_video_event()        
            event_output = self.manager.get_event_output()
            callback(event_output)
        except Exception as e:
            logging.error(e)

