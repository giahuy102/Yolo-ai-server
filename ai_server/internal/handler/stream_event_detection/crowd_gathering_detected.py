from multiprocessing import Event
from ....pkg.config.config import config
from ..object_detection.yolov7.utils.labels import Labels
from .event_detected import EventDetected

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
CROWD_GATHERING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["crowd_gathering"]

class CrowdGatheringDetected(EventDetected):

    def execute(self, manager, detection_results, callback):
        if not self.preprocess_frame(manager, detection_results):
            return False
        count = 0
        for res in detection_results.results:
            if res.class_id == Labels.PERSON:
                count += 1
        if count >= CROWD_GATHERING_EVENT_CONFIG["crowd_threshold"]:
            manager.process_event_output(detection_results, callback)
        # manager.process_event_output(detection_results, callback)
