import numpy as np
from numpy.linalg import norm

from ....pkg.config.config import config
from ..object_detection.yolov7.utils.labels import Labels
from .event_detected import EventDetected
from ..event_detection.line_crossing_utils import LineCrossingUtils

EVENT_CONFIG = config["event"]
CAMERA_EVENT_CONFIG = EVENT_CONFIG["camera"]
LINE_CROSSING_EVENT_CONFIG = CAMERA_EVENT_CONFIG["line_crossing"]

class LineCrossingDetected(EventDetected):

    def execute(self, manager, detection_results):
        self.preprocess_frame(manager, detection_results)
        # Not like stream_event_processing, don't use detection_results.frame_info because that info is None


        # [from_x, from_y, to_x, to_y] = manager.event_input.line_coords
        # pline_from = np.array([from_x, from_y])
        # pline_to = np.array([to_x, to_y])
        # for res in detection_results.results:
        #     if res.class_id == Labels.PERSON:
        #         [center_x, center_y, w, h] = res.center_w_h
        #         p_center = np.array([center_x, center_y])
        #         distance = norm(np.cross(pline_to - pline_from, pline_from - p_center)) / norm(pline_to - pline_from)
        #         if distance <= LINE_CROSSING_EVENT_CONFIG["crossing_distance_threshold"]:
        #             manager.true_alarm = True
        #             break

        line_crossing_utils = LineCrossingUtils()
        event_input = manager.event_input

        line_crossing_utils.draw_event_utils(detection_results.img_frame_with_box, event_input.line_coords, event_input.line_crossing_vector)


        tracker = event_input.tracker
        if line_crossing_utils.exist_line_crossing_in_trajectories(tracker.get_current_frame_trajectories(), event_input.line_coords, event_input.line_crossing_vector):
            manager.true_alarm = True
        manager.update_image_with_nearest_timestamp(detection_results)
