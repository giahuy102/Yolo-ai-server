from ....pkg.config.config import config
from ..object_detection.yolov7.utils.labels import Labels

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
CROWD_GATHERING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["crowd_gathering"]

class CrowdGatheringDetected:

    def execute(self, manager, detection_results):
        count = 0
        for res in detection_results.results:
            if res.class_id == Labels.PERSON:
                count += 1
        if count > CROWD_GATHERING_EVENT_CONFIG["crowd_threshold"]:
            manager.true_alarm = True
        manager.update_image_with_nearest_timestamp(detection_results)
