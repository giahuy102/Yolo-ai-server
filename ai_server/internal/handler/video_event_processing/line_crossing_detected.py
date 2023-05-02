import numpy as np
from numpy.linalg import norm
from ....pkg.config.config import config
from ..object_detection.yolov7.utils.labels import Labels

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
LINE_CROSSING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["line_crossing"]

class LineCrossingDetected:

    def execute(self, manager, detection_results):
        # Not like stream_event_processing, don't use detection_results.frame_info because that info is None
        [from_x, from_y, to_x, to_y] = manager.event_input.line_coords
        pline_from = np.array([from_x, from_y])
        pline_to = np.array([to_x, to_y])
        for res in detection_results.results:
            if res.class_id == Labels.PERSON:
                [center_x, center_y, w, h] = res.center_w_h
                p_center = np.array([center_x, center_y])
                distance = norm(np.cross(pline_to - pline_from, pline_from - p_center)) / norm(pline_to - pline_from)
                if distance <= LINE_CROSSING_EVENT_CONFIG["crossing_distance_threshold"]:
                    manager.true_alarm = True
                    break
        manager.update_image_with_nearest_timestamp(detection_results)
